from django.http import HttpResponseForbidden
from SRAM.constants import AUTHORIZATION_LEVELS
from django.http import HttpResponseForbidden
from SRAM.utils import decode_jwt_token

def auth(request,authLevel, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token :
            return False,None

        if token:
            decoded_payload = decode_jwt_token(token)
            print(decoded_payload)
            if decoded_payload:
                # Set user details from the JWT payload
                request.tokenData = decoded_payload
            else:
                return False,None
        if not request.tokenData or request.tokenData.get('authorizationLevel') < AUTHORIZATION_LEVELS[authLevel]:
            return HttpResponseForbidden('You are not authorized to access this page.')
        return True,request