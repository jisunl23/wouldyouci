from rest_framework import serializers
from .models import Cinema


class SimpleCinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ('id', 'name', 'type', 'img', 'address', 'tel', 'x', 'y', 'url')


class SearchCinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        fields = ('id', 'area', 'name', 'address', 'type', 'img', 'url')
