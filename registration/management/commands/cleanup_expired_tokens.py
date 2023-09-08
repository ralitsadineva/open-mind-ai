from django.core.management.base import BaseCommand
from django.utils import timezone
from registration.models import JwtToken
import jwt

class Command(BaseCommand):
    help = 'Deletes JWT tokens expired more than 2 months ago from the database'

    def handle(self, *args, **options):
        tokens = JwtToken.objects.all()
        tokens_to_delete = []
        for token in tokens:
            try:
                payload = jwt.decode(token.token, options={"verify_signature": False})
                if payload.get('exp', 0) < (timezone.now() - timezone.timedelta(days=60)).timestamp():
                    tokens_to_delete.append(token.id)
            except (jwt.ExpiredSignatureError, jwt.DecodeError):
                tokens_to_delete.append(token.id)
        JwtToken.objects.filter(id__in=tokens_to_delete).delete()
        self.stdout.write(self.style.SUCCESS('Expired tokens deleted successfully'))
