from msilib import schema
from app.security.security import Security
from fastapi import APIRouter, Depends, status, HTTPException

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from app.database.postgres.database import get_db
from app.models.models import UserModel
from app.scheme import scheme


router = APIRouter(tags=["Login Managment"])

@router.post("/")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
)-> str:
    user = db.query(UserModel).filter(
        UserModel.username == request.username
    ).first()
    print(user)
    
    if not user:
        return scheme.GeneralResponse(
            msg="bad",
            status= status.HTTP_401_UNAUTHORIZED,
            data= HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        )
    
    if not Security.is_valid(
        request.password,
        user.password
    ):
        return scheme.GeneralResponse(
            msg="bad",
            status= status.HTTP_401_UNAUTHORIZED,
            data= HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Credential dont match"
            )
        )
    
    subject = {
        "username": user.username,
        "id": user.id
    }

    access_token = Security.access_token(
        sub=user.id
    )
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }