from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.scheme import scheme

from typing import Optional,Any, Union

from datetime import datetime, timedelta
from app.settings import settings

from fastapi import Depends, HTTPException, status

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer( tokenUrl= f"{settings.API_V1_STR}/login")

class Security:

    @staticmethod
    def access_token(
        sub: Union[str,Any],
        expire_delta: timedelta = None
    ) -> str:
        if expire_delta:
            expire = datetime.utcnow() + expire_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub" : str(sub),
            "exp": expire
        }
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm= settings.ALGORITHM
        )



    @staticmethod
    def is_valid(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return password_context.verify(
            plain_password,
            hashed_password
        )
    

    @staticmethod
    def get_password(
        password:str
    ) -> str:
        return password_context.hash(
            password
        )

## dadsadasdsadasda Eat Pr FWLIPW
    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme)
    ):
        credentials_exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )

        try: 
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            subject = payload.get("sub")
            token_data = scheme.TokenID(id=subject)
        except Exception as e:
            print(e)
            return credentials_exception
        
        return token_data