import logging
import sys

from django.conf import settings


class UnauthorizedUsersLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def __call__(self, request):
        response = self.get_response(request)

        if settings.LOG_UNREGISTERED_USER_ACTIVITY and not request.user.is_authenticated:
            ip_address = self.__get_client_ip(request)

            full_url = request.build_absolute_uri()

            self.logger.info(
                f"Unregistered user IP: {ip_address} URL: {full_url} Type {request.method}"
            )

        return response

    def __get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
