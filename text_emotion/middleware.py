from registration.models import RequestTime, JwtToken
from constants.constants import TOKEN_OBJECT_EXPIRATION_TIME, REQUEST_TIME_EXPIRATION_TIME
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse
import time
import datetime

class RequestTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        
        if response.status_code == 401:
            return response
        
        if hasattr(request, 'start_time'):
            request.end_time = time.time()

            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Bearer'):
                token = authorization_header.split(' ')[1]
                cache_key_token = f'token_object:{token}'
                token_object = cache.get(cache_key_token)
                if token_object is None:
                    try:
                        token_object = JwtToken.objects.get(token=token)
                    except JwtToken.DoesNotExist:
                        message = 'Invalid token.'
                        return HttpResponse(message, status=401)
                    cache.set(cache_key_token, token_object, TOKEN_OBJECT_EXPIRATION_TIME)
                date = datetime.date.today()
                month = date.month
                year = date.year
                elapsed_time = request.end_time - request.start_time

                cache_key = f'request_time:{token_object.id}:{year}:{month}'
                cached_data = cache.get(cache_key)

                if cached_data is None:
                    request_entry, created = RequestTime.objects.get_or_create(
                        token=token_object,
                        month=month,
                        year=year,
                        defaults={'elapsed_time': elapsed_time}
                    )

                    if not created:
                        request_entry.elapsed_time += elapsed_time
                        request_entry.save()
                        cache.set(cache_key, request_entry.elapsed_time, REQUEST_TIME_EXPIRATION_TIME)
                    else:
                        cache.set(cache_key, elapsed_time, REQUEST_TIME_EXPIRATION_TIME)
                else:
                    cached_data += elapsed_time
                    cache.set(cache_key, cached_data, REQUEST_TIME_EXPIRATION_TIME)
                    RequestTime.objects.filter(token=token_object, month=month, year=year).update(elapsed_time=cached_data)
        return response
