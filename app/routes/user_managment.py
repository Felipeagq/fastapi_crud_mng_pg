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
    token = Depends(Security.get_current_user)
)-> str :
    users = db.query(UserModel).all()
    users_list = []
    for user in users:
        users_list.append({
            "id":user.id,
            "email":user.email,
            "username":user.username
        })
    return scheme.GeneralResponse(
        msg="ok",
        status= status.HTTP_202_ACCEPTED,
        data= users_list
    )


@router.get("/users/{id}")
def get_user_by_id(
    id:int,
    db : Session = Depends(get_db),
    token = Depends(Security.get_current_user)
)-> str:
    user = db.query(UserModel).filter(UserModel.id ==id).first()
    to_response = {
        "user":user.username,
        "email":user.email,
        "id":user.id
    }
    return scheme.GeneralResponse(
        status= status.HTTP_202_ACCEPTED,
        msg="ok",
        data=to_response
    )