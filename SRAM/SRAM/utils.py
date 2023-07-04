# authentication/utils.py

import jwt
from settings import env

def generate_jwt_token(payload):
    token = jwt.encode(payload, env(JWT_SECRET_KEY), algorithm='HS256')
    return token.decode('utf-8')

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, env(JWT_SECRET_KEY), algorithms=['HS256'])
        return decoded_payload
    except jwt.DecodeError:
        return None
