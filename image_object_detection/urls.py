from django.urls import path
from .views import ObjectDetectionView

urlpatterns = [
    path('api/object_detection/image', ObjectDetectionView.as_view(), name='object_detection'),
]
