from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

class JwtToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class RequestTime(models.Model):
    token = models.ForeignKey(JwtToken, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    elapsed_time = models.FloatField()

    class Meta:
        unique_together = ('token', 'month', 'year')
