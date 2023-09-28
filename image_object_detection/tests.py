from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from registration.models import JwtToken
from django.urls import reverse
from constants.constants import TEST_CACHE_SETTINGS

@override_settings(CACHES=TEST_CACHE_SETTINGS)
class MyApiTests(TestCase):
    def test_object_detection(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(user)
        token = JwtToken.objects.create(user=user, token=str(refresh.access_token))

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")
        image = {'image': open('image_object_detection/test_images/savanna.jpg', 'rb')}
        response = client.post(reverse('object_detection'), image, format='multipart')
        self.assertEqual(response.status_code, 200)
