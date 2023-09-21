from django.urls import path
from .views import TextClassifierView

urlpatterns = [
    path('api/classifier/text', TextClassifierView.as_view(), name='text_emotion'),
]
