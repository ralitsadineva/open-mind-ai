from django.test import TestCase
from rest_framework.test import APIClient

class MyApiTests(TestCase):
    def test_text_emotion(self):
        client = APIClient()
        response = client.post('', {'text': 'I am very happy today!'}, format='json')
        self.assertEqual(response.status_code, 200)
