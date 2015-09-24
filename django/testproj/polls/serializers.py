from models import roadcar
from rest_framework import serializers


class RoadcarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = roadcar
        fields = ('car_time',)
