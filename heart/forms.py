from django import forms 
from .models import HeartPrediction 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

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
            'oldpeak': forms.NumberInput(attrs={'class': 'form-control','placeholder': "Enter the ST depression value from your ECG test (0.0-7.0)."}),
            'st_slope': forms.Select(attrs={'class': 'form-select'}),
        }
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','password1','password2')
