from rest_framework import serializers
from .models import Object, ObjTr, Avvik, Customer, Month, Slokketype, Extinguishant


class ObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        extra_fields = ['url']


class ObjTrSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ObjTr
        fields = '__all__'
        extra_fields = ['url']


class AvvikSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Avvik
        fields = '__all__'
        extra_fields = ['url']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_fields = ['url']


class MonthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'
        extra_fields = ['url']


class SlokketypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Slokketype
        fields = '__all__'
        extra_fields = ['url']


class ExtinguishantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Extinguishant
        fields = '__all__'
        extra_fields = ['url']
