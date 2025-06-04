from rest_framework import serializers, viewsets
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pymongo import MongoClient
from bson.objectid import ObjectId
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['localTourist']
collection = db['tourist_attractions']

# Serializer for validation and representation
class TouristAttractionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField()
    image_url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    category = serializers.ChoiceField(choices=[
        ('natural', 'Natural Spot'),
        ('religious', 'Religious Site'),
        ('historical', 'Historical Site'),
        ('wildlife', 'Wildlife/Nature'),
        ('cultural', 'Cultural Site'),
    ])
    distance_from_karad_km = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)

class TouristAttractionViewSet(viewsets.ViewSet):
    def list(self, request):
        attractions = list(collection.find())
        for attr in attractions:
            attr['id'] = str(attr['_id'])
            del attr['_id']
        serializer = TouristAttractionSerializer(attractions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            attr = collection.find_one({'_id': ObjectId(pk)})
            if not attr:
                return Response(status=status.HTTP_404_NOT_FOUND)
            attr['id'] = str(attr['_id'])
            del attr['_id']
            serializer = TouristAttractionSerializer(attr)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = TouristAttractionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = collection.insert_one(data)
            data['id'] = str(result.inserted_id)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = TouristAttractionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                result = collection.update_one({'_id': ObjectId(pk)}, {'$set': data})
                if result.matched_count == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                data['id'] = pk
                return Response(data)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            result = collection.delete_one({'_id': ObjectId(pk)})
            if result.deleted_count == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

router = DefaultRouter()
router.register(r'attractions', TouristAttractionViewSet, basename='attraction')

karad_explorer_urls = [
    path('', include(router.urls)),
]
