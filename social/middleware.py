from rest_framework_simplejwt import authentication, exceptions
from django.http import JsonResponse
from rest_framework import status


class UserActivityMiddleware(object):
    """
    check if user authenticated if True, saves request.path as user.last_action
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            is_authenticate = authentication.JWTAuthentication().authenticate(request)

            if is_authenticate is not None:
                request.user = is_authenticate[0]

        except exceptions.InvalidToken:
            return JsonResponse({'error': 'token has already expired'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_authenticated:
            request.user.last_action = request.path
            request.user.save()
