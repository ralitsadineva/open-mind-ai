from django.urls import path
from .views import ImageClassifierView

urlpatterns = [
    path('api/classifier/image', ImageClassifierView.as_view(), name='image_classifier'),
]
