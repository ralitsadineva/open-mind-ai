from django.urls import path
from .views import user_registration_view, user_login_view, user_tokens_view, generate_token_view

urlpatterns = [
    path('register/', user_registration_view, name='user-registration'),
    path('login/', user_login_view, name='user-login'),
    path('tokens/', user_tokens_view, name='user-tokens'),
    path('generate-token/', generate_token_view, name='generate-token'),
]
