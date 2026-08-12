from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HeartPrediction(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    
    age = models.IntegerField()

    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    CHEST_CHOICES = [
        ('ATA', 'Atypical Angina (Chest pain that is not typical of heart disease)'),
        ('NAP', 'Non-Anginal Pain (Chest pain that is generally not related to heart disease)'),
        ('ASY', 'Asymptomatic (No chest pain or symptoms)'),
        ('TA', 'Typical Angina (Typical chest pain related to the heart)'),
    ]
    help_text="Select your chest pain type"
    chest_pain_type = models.CharField(max_length=3, choices=CHEST_CHOICES)

    resting_bp = models.IntegerField()
    cholesterol = models.IntegerField()

    FASTING_CHOICES = [
    (0, 'No (Fasting Blood Sugar is normal)'),
    (1, 'Yes (Fasting Blood Sugar is high)'),
    ]
    fasting_bs = models.IntegerField(choices=FASTING_CHOICES)

    ECG_CHOICES = [
        ('Normal', 'Normal — Normal ECG result'),
        ('ST', 'ST — ST-T wave abnormality'),
        ('LVH', 'LVH — Thickening of the left ventricle muscle'),
    ]
    resting_ecg = models.CharField(max_length=10, choices=ECG_CHOICES)

    max_hr = models.IntegerField()

    ANGINA_CHOICES = [
        ('N', 'No — No chest pain during exercise'),
        ('Y', 'Yes — Chest pain occurs during exercise'),
    ]
    exercise_angina = models.CharField(max_length=1, choices=ANGINA_CHOICES)

    oldpeak = models.FloatField()

    SLOPE_CHOICES = [
        ('Up', 'Up — ST segment rises upward'),
        ('Flat', 'Flat — ST segment remains relatively flat'),
        ('Down', 'Down — ST segment slopes downward'),
    ]
    st_slope = models.CharField(max_length=10, choices=SLOPE_CHOICES)
    

    def __str__(self):
        return f"{self.user}"
