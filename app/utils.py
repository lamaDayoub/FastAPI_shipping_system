from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from itsdangerous import BadSignature, Serializer, SignatureExpired, URLSafeTimedSerializer

from app.config import security_settings
import jwt

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET_KEY)


def generate_access_token(
    data:dict,
    expiry: timedelta = timedelta(days =1 )
)-> str:
    return jwt.encode(
        payload={
            **data ,
            'jti':str(uuid4()),
            "exp": datetime.now(timezone.utc)+expiry 
            },
            algorithm =security_settings.JWT_ALGORITHM,
            key = security_settings.JWT_SECRET_KEY
            
        )
    

def decode_access_token(token) -> dict | None :
    try:
        return jwt.decode(
            jwt = token,
            key = security_settings.JWT_SECRET_KEY,
            algorithms = [security_settings.JWT_ALGORITHM]
        )
        
    except jwt.PyJWTError :
        return None
        
        
APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR/"templates"

def generate_url_safe_token(data:dict)->str:
    return _serializer.dumps(data)

def decode_url_safe_token(token : str, expiry: timedelta |None =None)->dict |None:
    try:
        return _serializer.loads(
        token,
        max_age=expiry if expiry else None
        )
    except(BadSignature, SignatureExpired):
        return None
        
        