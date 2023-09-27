from rest_framework import serializers

class ImageToTextSerializer(serializers.Serializer):
    image = serializers.ImageField()
