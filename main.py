from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Response, HTTPException, status, Request
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from typing import List, Dict, Union
app = FastAPI()

# Class model
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime



app = FastAPI()

# Variable globale pour stocker les posts en mémoire
posts_db: List[Post] = []


#GET/ping Q1
@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    return Response("pong")

@app.get("/ping/auth")
async def auth_user_pswd(user: str, password: str):
    if user == "admin" and password == "123456":
        return PlainTextResponse("test", status_code=status.HTTP_200_OK)
    else:
        return HTMLResponse("wrong password or user is not admin", status_code=status.HTTP_403_FORBIDDEN)


#GET/home Q2
@app.get("/home", status_code=status.HTTP_200_OK)
def home():
    html_content = "<!DOCTYPE html><html><head><title>Home</title></head><body><h1>Welcome home!</h1></body></html>"
    return HTMLResponse(html_content)

#404 NOT FOUND Q3
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    html_content = "<!DOCTYPE html><html><head><title>Not found</title></head><body><h1>404 page not found</h1></body></html>"
    return HTMLResponse(content=html_content, media_type="text/html", status_code=status.HTTP_404_NOT_FOUND)


#POST/posts Q4
@app.post("/posts", response_model=List[Post], status_code=status.HTTP_201_CREATED)
async def create_posts(posts: List[Post]):
    posts_db.extend(posts)
    return posts_db

#GET/posts Q5
@app.get("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
async def get_all_posts():
    return posts_db

#PUT/posts Q6
@app.put("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
async def upsert_post(post: Post):
    found = False
    for i, existing_post in enumerate(posts_db):
        if existing_post.title == post.title:
            posts_db[i] = post
            found = True
            break
    if not found:
        posts_db.append(post)
    return posts_db


