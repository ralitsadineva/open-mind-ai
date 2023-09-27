from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageToTextSerializer
from PIL import Image
from transformers import pipeline

class ImageToTextView(APIView):
    serializer_class = ImageToTextSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ImageToTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = Image.open(serializer.validated_data['image'])
        pipe = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        result = pipe(image)
        return Response({'result': result})
