from fastapi import APIRouter, Depends, status, HTTPException

from app.database.mongo.mongo_crud import BookCRUDMongo
from app.scheme import scheme

from app.security.security import Security


router = APIRouter(tags=["Book Managament"])

@router.get("/")
async def get_books():
    _bookList = await BookCRUDMongo.read_all()
    return scheme.GeneralResponse(
        status= status.HTTP_202_ACCEPTED,
        msg="ok",
        data= _bookList
    )

@router.post("/")
async def create_book(
    book: scheme.BookRequestScheme,
    token = Depends(Security.get_current_user)
) -> str:
    _book = await BookCRUDMongo.create(
        book=book,
        token_id=token.id
    )
    return scheme.GeneralResponse(
        status= status.HTTP_202_ACCEPTED,
        msg="Created",
        data= _book
    )