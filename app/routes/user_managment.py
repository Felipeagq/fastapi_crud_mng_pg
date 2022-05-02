import email
from fastapi import APIRouter, Depends, status, HTTPException

from app.database.postgres.database import get_db
from app.models.models import UserModel
from sqlalchemy.orm import Session

from app.scheme import scheme

from app.security.security import Security

router = APIRouter(tags=["User Managment"])

@router.post(
    "/create",
    status_code= status.HTTP_202_ACCEPTED
)
async def create_user(
    request: scheme.UserRequestScheme,
    db: Session = Depends(get_db),
)-> str :
    new_user = UserModel(
        username = request.username,
        email = request.email,
        password = Security.get_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return scheme.GeneralResponse(
        msg="ok",
        status= status.HTTP_201_CREATED,
        data=new_user
    ).dict(exclude_none=None)



@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    request = Depends(Security.get_current_user)
)-> str :
    users = db.query(UserModel).all()
    return scheme.GeneralResponse(
        msg="ok",
        status= status.HTTP_202_ACCEPTED,
        data= users
    )