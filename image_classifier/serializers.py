from rest_framework import serializers

class ImageClassifierSerializer(serializers.Serializer):
    image = serializers.ImageField()
