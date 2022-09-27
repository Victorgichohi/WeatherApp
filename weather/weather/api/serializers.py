from rest_framework import serializers


class ForecastSerializer(serializers.Serializer):
    maximum = serializers.FloatField()
    minimum = serializers.FloatField()
    average = serializers.FloatField()
    median = serializers.FloatField()

    class Meta:
        fields = '__all__'
