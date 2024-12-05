import jwt
from datetime import datetime, timezone
from config.main.config import Config

def create_access_token(username, expires_delta, role = None, refresh = False):
    payload = {'sub': username, 'role' : role}
    payload['refresh'] = refresh
    payload.update({'exp' : datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm= Config.JWT_ALGORITHM)

def decode_token(token : str) -> dict:
    try:
        token_data = jwt.decode(jwt= token, key = Config.JWT_SECRET_KEY, algorithms= [Config.JWT_ALGORITHM])
        return token_data
    except Exception as e:
        return None    