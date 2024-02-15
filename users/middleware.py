from django.http import HttpResponseForbidden
from django.contrib.auth.middleware import get_user

class BlockUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = get_user(request)
        if user.is_authenticated and user.is_blocked and not user.is_superuser:
            return HttpResponseForbidden('Вас заблокировали. Доступ запрещен.')

        response = self.get_response(request)
        return response