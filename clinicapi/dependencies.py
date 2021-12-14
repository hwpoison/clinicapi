from typing import Generator
from .config.database import db_session
import jwt
import os
from .utils.exception import Exceptional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from dataclasses import dataclass, field
# move to auth
JWT_SECRET_KEY = "UnaVezIbaCaminandoHastaQueMeTropezeYhdshja\
hjkadhjlh981931o23950234095209905905904593290239"

# TODO: make hasheable for tests
class UserTokenAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserTokenAuth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if os.environ.get('test_mode'): return 'test-mode'
        credentials: HTTPAuthorizationCredentials = await super(UserTokenAuth, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> str:
        try:
            payload = jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['username']
        except:
            raise Exceptional('Invalid token!', 403)

def get_db() -> Generator:
    db = db_session()
    try:
        yield db
    finally:
        db.close()


