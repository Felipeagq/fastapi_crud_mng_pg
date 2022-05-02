from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.database.postgres.database import get_db

from app.scheme import scheme
from app.security.security import Security

router = APIRouter(tags=["Blog Managment"])

@router.post("/")
def create_blog(
    request: scheme.BlogRequestScheme,
    db: Session = Depends(get_db),
    token = Depends(Security.get_current_user)
):
    return {
        "request":request,
        "token":token
    }