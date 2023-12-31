from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import TextClassifierSerializer
from transformers import pipeline

class TextClassifierView(APIView):
    serializer_class = TextClassifierSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TextClassifierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        pipe = pipeline('text-classification', model='SamLowe/roberta-base-go_emotions', top_k=None)
        result = pipe(text)
        return Response({'result': result})
