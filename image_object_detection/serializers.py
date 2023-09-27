from rest_framework import serializers

class ObjectDetectionSerializer(serializers.Serializer):
    image = serializers.ImageField()
