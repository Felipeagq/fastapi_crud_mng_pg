from fastapi import APIRouter, Depends, status, HTTPException


from sqlalchemy.orm import Session
from app.database.postgres.database import get_db
from datetime import datetime

from app.scheme import scheme
from app.security.security import Security

from app.models.models import BlogModel

router = APIRouter(tags=["Blog Managment"])

@router.post("/")
def create_blog(
    request: scheme.BlogRequestScheme,
    db: Session = Depends(get_db),
    token = Depends(Security.get_current_user)
):
    user_id = token
    print(str(user_id))
    new_blog = BlogModel(
        title = request.title,
        body = request.body,
        user_id = token.id,
        date = datetime.utcnow()
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return scheme.GeneralResponse(
        msg="created",
        status= status.HTTP_201_CREATED,
        data= new_blog
    )


@router.get("/")
def get_blogs(
    db:Session = Depends(get_db)
) -> str:
    blogs = db.query(BlogModel).all()
    blogs_list = []
    for blog in blogs:
        print(blog.creator)
        blog_objec= {
        "body": blog.body,
        "title":blog.title,
        "date": blog.date,
        "user_id": blog.user_id,
        "id": blog.id,
        "creator": {
            "id": blog.creator.id,
            "email": blog.creator.email,
            "username": blog.creator.username
            }
        }
        blogs_list.append(blog_objec)
    # return blogs
    return scheme.GeneralResponse(
        msg="ok",
        status= status.HTTP_202_ACCEPTED,
        data= blogs_list
    )


@router.delete("/{id}")
def delete_blog(
    id:int,
    db: Session = Depends(get_db),
    token = Depends(Security.get_current_user)
) -> str :
    blog = db.query(BlogModel).filter(BlogModel.id == id)
    blog_geted = blog.first()
    if not blog_geted:
        return scheme.GeneralResponse(
            msg="bad",
            status= status.HTTP_404_NOT_FOUND,
            data= HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Id not found"
            )
        )
    blog.delete()
    db.commit()
    return scheme.GeneralResponse(
        msg="ok",
        status= status.HTTP_202_ACCEPTED,
        data = blog_geted
    )
