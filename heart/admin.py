from django.contrib import admin
from .models import HeartPrediction


@admin.register(HeartPrediction)
class HeartPredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "result", "age", "sex", "created_at")
    list_filter = ("result", "sex")
