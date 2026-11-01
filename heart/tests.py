from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import HeartPrediction

# One valid set of the 11 clinical values, usable both for the form and the model.
SAMPLE = {
    'age': 54,
    'sex': 'M',
    'chest_pain_type': 'ASY',
    'resting_bp': 140,
    'cholesterol': 239,
    'fasting_bs': 0,
    'resting_ecg': 'Normal',
    'max_hr': 160,
    'exercise_angina': 'N',
    'oldpeak': 1.2,
    'st_slope': 'Flat',
}


class DownloadReportAccessTests(TestCase):
    """A PDF report may only be downloaded by the person who created it."""

    def setUp(self):
        self.alice = User.objects.create_user('alice', password='pass12345')
        self.bob = User.objects.create_user('bob', password='pass12345')
        self.alice_report = HeartPrediction.objects.create(user=self.alice, result=0, **SAMPLE)

    def report_url(self, pk):
        return reverse('download_report', args=[pk])

    def test_owner_can_download_own_report(self):
        self.client.login(username='alice', password='pass12345')
        response = self.client.get(self.report_url(self.alice_report.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('heart_report_alice.pdf', response['Content-Disposition'])

    def test_other_user_cannot_download_report(self):
        self.client.login(username='bob', password='pass12345')
        response = self.client.get(self.report_url(self.alice_report.pk))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_cannot_download_user_report(self):
        response = self.client.get(self.report_url(self.alice_report.pk))
        self.assertEqual(response.status_code, 404)

    def test_missing_report_looks_the_same_as_forbidden(self):
        self.client.login(username='bob', password='pass12345')
        response = self.client.get(self.report_url(999999))
        self.assertEqual(response.status_code, 404)

    def test_guest_can_download_report_from_own_session(self):
        response = self.client.post(reverse('all_heart_view'), SAMPLE)
        self.assertEqual(response.status_code, 200)
        guest_report = HeartPrediction.objects.get(user=None)

        response = self.client.get(self.report_url(guest_report.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn('heart_report_guest.pdf', response['Content-Disposition'])

    def test_guest_report_hidden_from_other_sessions(self):
        guest_report = HeartPrediction.objects.create(user=None, result=0, **SAMPLE)

        # A different guest browser (fresh session).
        response = self.client.get(self.report_url(guest_report.pk))
        self.assertEqual(response.status_code, 404)

        # A logged-in user who didn't create it.
        self.client.login(username='bob', password='pass12345')
        response = self.client.get(self.report_url(guest_report.pk))
        self.assertEqual(response.status_code, 404)


class HistoryPageTests(TestCase):
    """My History lists only the logged-in user's own predictions."""

    def setUp(self):
        self.alice = User.objects.create_user('alice', password='pass12345')
        self.bob = User.objects.create_user('bob', password='pass12345')
        self.url = reverse('history')

    def add_predictions(self, user, count, **overrides):
        for _ in range(count):
            HeartPrediction.objects.create(user=user, result=0, **{**SAMPLE, **overrides})

    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response['Location'])

    def test_empty_state_without_predictions(self):
        self.client.force_login(self.alice)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No predictions yet')
        self.assertNotContains(response, 'history-data')

    def test_shows_only_own_predictions(self):
        self.add_predictions(self.alice, 1, cholesterol=211)
        self.add_predictions(self.bob, 1, cholesterol=377)
        self.client.force_login(self.alice)
        response = self.client.get(self.url)
        self.assertContains(response, '211')
        self.assertNotContains(response, '377')
        self.assertEqual(response.context['total'], 1)

    def test_risk_count_and_latest(self):
        self.add_predictions(self.alice, 2)
        HeartPrediction.objects.create(user=self.alice, result=1, **SAMPLE)
        self.client.force_login(self.alice)
        response = self.client.get(self.url)
        self.assertEqual(response.context['risk_count'], 1)
        self.assertEqual(response.context['latest'].result, 1)

    def test_pagination_ten_per_page(self):
        self.add_predictions(self.alice, 12)
        self.client.force_login(self.alice)
        first = self.client.get(self.url)
        second = self.client.get(self.url, {'page': 2})
        self.assertEqual(len(first.context['page'].object_list), 10)
        self.assertEqual(len(second.context['page'].object_list), 2)
        self.assertContains(first, 'Page 1 of 2')

    def test_charts_need_at_least_two_predictions(self):
        self.add_predictions(self.alice, 1)
        self.client.force_login(self.alice)
        self.assertNotContains(self.client.get(self.url), 'id="history-data"')

        self.add_predictions(self.alice, 1)
        response = self.client.get(self.url)
        self.assertContains(response, 'id="history-data"')
        self.assertEqual(len(response.context['chart_rows']), 2)
