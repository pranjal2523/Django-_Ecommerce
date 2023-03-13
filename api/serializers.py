from rest_framework import serializers
from api import models


class Tagserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class ArtiicleSerializer(serializers.ModelSerializer):
    tagList = Tagserializer(many=True, read_only=True)
    
    class Meta:
        model = models.Article
        fields = '__all__' 