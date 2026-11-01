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
