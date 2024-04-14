from rest_framework import serializers
from .models import BusInfo


class BusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusInfo
        fields = [
            "BusID",
            "Info",
        ]
