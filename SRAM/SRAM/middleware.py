# myproject/middleware.py

from django.http import HttpResponseForbidden
from SRAM.utils import decode_jwt_token

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if not auth_header :
            return HttpResponseForbidden('Unauthorized')

        if token:
            decoded_payload = decode_jwt_token(token)
            if decoded_payload:
                # Set user details from the JWT payload
                request.token = token
            else:
                return HttpResponseForbidden('Invalid token')

        response = self.get_response(request)
        return response
