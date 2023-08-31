from django.utils.deprecation import MiddlewareMixin
import time
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
                logging.warning(f"Token: {token}, Elapsed Time: {request.end_time - request.start_time}")
            else:
                logging.warning("Invalid token format")
        return response
