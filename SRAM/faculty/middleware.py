# myproject/middleware.py

from django.http import HttpResponseForbidden
from SRAM.utils import decode_jwt_token

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('auth_token')

        if token:
            decoded_payload = decode_jwt_token(token)
            if decoded_payload:
                # Set user details from the JWT payload
                request.user = {
                    'username': decoded_payload['username'],
                    'auth_level': decoded_payload['auth_level'],
                }
            else:
                return HttpResponseForbidden('Invalid token')

        response = self.get_response(request)
        return response
