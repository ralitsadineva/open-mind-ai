from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageClassifierSerializer
from PIL import Image
from transformers import pipeline

class ImageClassifierView(APIView):
    serializer_class = ImageClassifierSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ImageClassifierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = Image.open(serializer.validated_data['image'])
        pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
        result = pipe(image)
        return Response({'result': result})
