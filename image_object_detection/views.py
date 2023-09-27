from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ObjectDetectionSerializer
from PIL import Image
from transformers import pipeline

class ObjectDetectionView(APIView):
    serializer_class = ObjectDetectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ObjectDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = Image.open(serializer.validated_data['image'])
        pipe = pipeline("object-detection", model="hustvl/yolos-tiny")
        result = pipe(image)
        return Response({'result': result})
