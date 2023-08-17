from django.urls import path
from .views import TextClassifierView

urlpatterns = [
    path('', TextClassifierView.as_view(), name='text_emotion'),
]
