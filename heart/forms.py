from django import forms 
from .models import HeartPrediction 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from cProfile import label

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

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','password1','password2')
