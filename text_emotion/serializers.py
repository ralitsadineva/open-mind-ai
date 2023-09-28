from rest_framework import serializers

class TextClassifierSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
