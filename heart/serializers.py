from rest_framework import serializers
from .models import HeartPrediction


class HeartPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartPrediction
        fields = "__all__"
        # Filled in by the server, never by the API client.
        read_only_fields = ("user", "result", "risk_reasons", "created_at")
