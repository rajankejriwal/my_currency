from rest_framework import serializers

from exchange_rate.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer to serialize data."""

    class Meta:
        model = Currency
        fields = "__all__"
