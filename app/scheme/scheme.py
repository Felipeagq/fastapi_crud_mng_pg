from pydantic import BaseModel
from typing import Type, TypeVar, Optional

T = TypeVar("T")


class GeneralResponse(BaseModel):
    msg:str
    status:str
    data: Optional[T] = None


class TokenID(BaseModel):
    id: str = None


class LoginScheme(BaseModel):
    username: str
    password: str


class UserRequestScheme(BaseModel):
    username: str
    password: str
    email: str


class BlogRequestScheme(BaseModel):
    title: str
    body: str


class BookRequestScheme(BaseModel):
    title: str
    description: str


