from django import forms
from .models import HeartPrediction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Shown in the hover tooltip next to a field label, in plain language for
# patients who have never seen these terms. Fields the user already knows the
# answer to (age, sex) are left out on purpose.
FIELD_TOOLTIPS = {
    'chest_pain_type': {
        'what': 'What kind of chest pain do you get? '
                'No pain at all - pick "Asymptomatic". '
                'Pain or pressure when you walk fast or climb stairs, and it stops when you rest - pick "Typical Angina". '
                'Pain that feels a little like that, but not exactly - pick "Atypical Angina". '
                'Pain from gas, acidity or a pulled muscle - pick "Non-Anginal Pain".',
        'normal': 'Not sure? Pick the one that sounds most like you, or ask your doctor.',
        'where': 'From how you feel, or from what your doctor told you.',
    },
    'resting_bp': {
        'what': 'Your blood pressure (BP), checked while sitting calmly. '
                'BP has two numbers, like 120/80. Type only the first, bigger number (120).',
        'normal': 'Good: below 120. High: 140 or more.',
        'where': 'A BP machine at home, a chemist shop, or a doctor\'s clinic.',
    },
    'cholesterol': {
        'what': 'How much fat (cholesterol) is in your blood.',
        'normal': 'Good: below 200. High: 240 or more.',
        'where': 'A blood test report called "Lipid Profile". Look for the line "Total Cholesterol".',
    },
    'fasting_bs': {
        'what': 'Your blood sugar, tested in the morning before eating anything.',
        'normal': 'If the number is above 120, pick "Yes". If it is 120 or less, pick "No".',
        'where': 'A blood test report called "Fasting Blood Sugar" or "FBS".',
    },
    'resting_ecg': {
        'what': 'An ECG is a simple test where stickers are put on your chest to check your heartbeat.',
        'normal': 'Most people get "Normal". Pick "ST" or "LVH" only if those words are written on your report.',
        'where': 'Your ECG report, in the doctor\'s comments. Never had an ECG? Pick "Normal" and ask your doctor about it.',
    },
    'max_hr': {
        'what': 'The fastest your heart beat (beats per minute) while walking or running on a treadmill test.',
        'normal': 'Roughly 220 minus your age. For example, at age 50 it is about 170.',
        'where': 'A treadmill test report (also called "TMT" or "stress test"). Look for "Max HR".',
    },
    'exercise_angina': {
        'what': 'Do you get chest pain while exercising, walking fast or climbing stairs?',
        'normal': 'Most healthy people pick "No".',
        'where': 'From how you feel, or from your treadmill test report.',
    },
    'oldpeak': {
        'what': 'A number from the treadmill test that shows how much your heart is stressed during exercise.',
        'normal': 'Good: 0 to 1. Worrying: 2 or more. If your report does not show it, type 0.',
        'where': 'A treadmill test report (TMT), written as "ST depression".',
    },
    'st_slope': {
        'what': 'A result from the treadmill test that shows how your heart reacts to exercise.',
        'normal': 'Healthy hearts usually show "Up". "Flat" or "Down" can be a warning sign.',
        'where': 'A treadmill test report (TMT), in the doctor\'s comments. Not sure? Ask your doctor.',
    },
}


class HeartForm(forms.ModelForm):
    class Meta:
        model = HeartPrediction 
        fields = [
            'age',
            'sex',
            'chest_pain_type',
            'resting_bp',
            'cholesterol',
            'fasting_bs',
            'resting_ecg',
            'max_hr',
            'exercise_angina',
            'oldpeak',
            'st_slope',
        ]
        
        help_texts = {
            'age': 'Enter your age in years.',
            'sex': 'Select your biological sex.',
            'chest_pain_type': 'Select the type of chest pain you experience.',
            'resting_bp': 'Enter your systolic blood pressure while resting (mmHg).',
            'cholesterol': 'Enter your total blood cholesterol level (mg/dL).',
            'fasting_bs': 'Blood sugar level measured on an empty stomach.',
            'resting_ecg': 'Select the result of your resting ECG (heart electrical activity test).',
            'max_hr': 'Enter the highest heart rate reached during exercise (beats per minute).',
            'exercise_angina': 'Select whether you experience chest pain during exercise.',
            'oldpeak': 'ST depression measured during an ECG exercise test. '
                       'This value is usually provided by an ECG/stress test report.',
            'st_slope': 'Select the slope of the ST segment during exercise.',
        }

        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter your age'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'chest_pain_type': forms.Select(attrs={'class': 'form-select'}),
            'resting_bp': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter resting systolic BP (90-200 mmHg)'}),
            'cholesterol': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter total cholesterol (100-600 mg/dL)'}),
            'fasting_bs': forms.Select(attrs={'class': 'form-select'}),
            'resting_ecg': forms.Select(attrs={'class': 'form-select'}),
            'max_hr': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter maximum heart rate achieved (60-220 bpm)'}),
            'exercise_angina': forms.Select(attrs={'class': 'form-select'}),
            'oldpeak': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter a value between 0.0 and 6.2'}),
            'st_slope': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reachable in the template as field.field.tooltip
        for name, tooltip in FIELD_TOOLTIPS.items():
            if name in self.fields:
                self.fields[name].tooltip = tooltip


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','password1','password2')
