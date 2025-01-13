import jwt
import datetime
from app.config import SECRET_KEY
import logging


def encode_auth_token(user_id):
    try:
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        payload = {
            'exp': expiration_time,
            'sub': str(user_id)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)


def decode_auth_token(token):
    try:
        logging.debug(f"Token received: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logging.debug(f"Decoded payload: {payload}")
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError as e:
        logging.error(f"Error decoding token: {str(e)}")
        return f"Invalid token. Please log in again. Error details: {str(e)}"
