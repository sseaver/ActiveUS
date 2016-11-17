from rest_framework import serializers
from app.models import Location, Star_Rating


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star_Rating
        fields = ('rating',)
