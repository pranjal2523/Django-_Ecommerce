from django.shortcuts import render
import rest_framework

from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from api import models, serializers
import json

# Create your views here.
#Function based API views
#@api_view()
#def article(request):
#    article = models.Article.objects.all()
#    response = serializers.ArtiicleSerializer(article, many= True)
#    return Response(response.data)
#
#
#@api_view(['POST'])
def create(request):
    pass
#    body = json.loads(request.body)
#    response = serializers.ArtiicleSerializer(data = body)
#    if response.is_valid():
#        instan = response.save()
#        response = serializers.ArtiicleSerializer(instan)
#        return Response(response.data)
#    return Response(response.errors)


# Class based API views
#listView
#only make get request
class articleLV(ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArtiicleSerializer

#only make get request
#class articleDV(RetrieveAPIView):
#    queryset = models.Article.objects.all()
#    serializer_class = serializers.ArtiicleSerializer


#you can make get and patch request using RetrieveUpdateAPIView.You can update data using this
class articleDV(RetrieveUpdateAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArtiicleSerializer


#another is ListUpdateAPIView that return all data that make get request to fetch all data and patch request to update data