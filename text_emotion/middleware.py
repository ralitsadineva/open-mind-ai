from registration.models import RequestTime, JwtToken
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
import time
import datetime
import logging

class RequestTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            request.end_time = time.time()

            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Bearer'):
                token = authorization_header.split(' ')[1]
                # logging.warning(f"Token: {token}, Elapsed Time: {request.end_time - request.start_time}")
                token_object = JwtToken.objects.get(token=token)
                date = datetime.date.today()
                month = date.month
                year = date.year
                elapsed_time = request.end_time - request.start_time

                cache_key = f'request_time:{token_object.id}:{year}:{month}'
                cached_data = cache.get(cache_key)
                # logging.warning(f"Cache Key: {cache_key}, Cached Data: {cached_data}")

                if cached_data is None:
                    request_entry, created = RequestTime.objects.get_or_create(
                        token=token_object,
                        month=month,
                        year=year,
                        defaults={'elapsed_time': elapsed_time}
                    )
                    # logging.warning(f"Request Entry: {request_entry}, Created: {created}")

                    if not created:
                        request_entry.elapsed_time += elapsed_time
                        request_entry.save()
                        cache.set(cache_key, request_entry.elapsed_time, 60 * 60 * 24)
                    else:
                        cache.set(cache_key, elapsed_time, 60 * 60 * 24)
                else:
                    cached_data += elapsed_time
                    cache.set(cache_key, cached_data, 60 * 60 * 24)
                    RequestTime.objects.filter(token=token_object, month=month, year=year).update(elapsed_time=cached_data)
            # else:
            #     # logging.warning("Invalid token format")
            #     pass
        return response
