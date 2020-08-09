from rest_framework import serializers

from .models import Betting

class BettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Betting
        fields = '__all__'