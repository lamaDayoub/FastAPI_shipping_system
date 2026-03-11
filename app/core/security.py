from typing_extensions import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from app.utils import decode_access_token

oauth2_scheme_seller= OAuth2PasswordBearer(tokenUrl = '/seller/token')
oauth2_scheme_partner= OAuth2PasswordBearer(tokenUrl = '/partner/token')




























# class AccessTokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         auth_credentials = request.headers.get("Authorization").split(" ")[1]
#         token = auth_credentials.credentials
#         token_data = decode_access_token(token)
#         if token_data is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='not authorized')
#         return token_data
        
    
# accesstokenbearer = AccessTokenBearer()
# Annotated[str,Depends(accesstokenbearer)]
    