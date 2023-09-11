from registration.models import RequestTime, JwtToken
from django.utils.deprecation import MiddlewareMixin
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

                request_entry, created = RequestTime.objects.get_or_create(
                    token=token_object,
                    month=month,
                    year=year,
                    defaults={'elapsed_time': elapsed_time}
                )
                logging.warning(f"Request Entry: {request_entry}, Created: {created}")

                if not created:
                    request_entry.elapsed_time += elapsed_time
                    request_entry.save()
            else:
                # logging.warning("Invalid token format")
                pass
        return response
