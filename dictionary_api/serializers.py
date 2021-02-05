from rest_framework import serializers

from .models import Dictionary, Element


class DictionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictionary
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Element
        fields = ('element_code', 'value')
