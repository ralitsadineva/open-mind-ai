from django.urls import path
from .views import ImageToTextView

urlpatterns = [
    path('api/image_to_text', ImageToTextView.as_view(), name='image_to_text'),
]
