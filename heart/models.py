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
        ('ATA', 'ATA'),
        ('NAP', 'NAP'),
        ('ASY', 'ASY'),
        ('TA', 'TA'),
    ] 
    help_text="Select your chest pain type"
    chest_pain_type = models.CharField(max_length=3, choices=CHEST_CHOICES)

    resting_bp = models.IntegerField()
    cholesterol = models.IntegerField()

    FASTING_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    fasting_bs = models.IntegerField(choices=FASTING_CHOICES)

    ECG_CHOICES = [
        ('Normal', 'Normal'),
        ('ST', 'ST'),
        ('LVH', 'LVH'),
    ]
    resting_ecg = models.CharField(max_length=10, choices=ECG_CHOICES)

    max_hr = models.IntegerField()

    ANGINA_CHOICES = [
        ('N', 'No'),
        ('Y', 'Yes'),
    ]
    exercise_angina = models.CharField(max_length=1, choices=ANGINA_CHOICES)

    oldpeak = models.FloatField()

    SLOPE_CHOICES = [
        ('Up', 'Up'),
        ('Flat', 'Flat'),
        ('Down', 'Down'),
    ]
    st_slope = models.CharField(max_length=10, choices=SLOPE_CHOICES)
    

    def __str__(self):
        return f"{self.user}"
