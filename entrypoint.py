from ensurepip import version
from imp import reload
from turtle import title
from fastapi import FastAPI
import uvicorn
from app.settings import settings
from starlette.middleware.cors import CORSMiddleware

from app.routes import user_managment, login_managment, blog_managment

app = FastAPI(
    title= settings.PROJECT_NAME,
    version= settings.PROJECT_VERSION,
    use_colors=True
)

@app.get("/")
def hello_check():
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "PROJECT_VERSION": settings.PROJECT_VERSION
    }


app.include_router(user_managment.router, prefix=f"{settings.API_V1_STR}/user")
app.include_router(login_managment.router, prefix=f"{settings.API_V1_STR}/login")
app.include_router(blog_managment.router, prefix=f"{settings.API_V1_STR}/blog")



app.add_middleware(
    CORSMiddleware,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_origins = ["*"],
    allow_credentials = True
)

if __name__ == "__main__":
    uvicorn.run(
        "entrypoint:app",
        host="0.0.0.0",
        port=5000,
        workers=1,
        reload=True,
        log_level="info",
        use_colors=True
    )