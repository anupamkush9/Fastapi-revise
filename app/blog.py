import os
import shutil
from fastapi import (
    APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
)
from sqlmodel import Session
from app.database import get_session
from app.models import Blog
from app.schemas import BlogResponse
from app.crud import (
    create_blog, get_all_blogs, get_single_blog, delete_blog
)

router = APIRouter(prefix="/blogs", tags=["Blogs"])


# CREATE BLOG
@router.post("/", response_model=BlogResponse)
def create_blog_api(
    request: Request, title: str = Form(...), description: str = Form(...),
    image: UploadFile = File(...), session: Session = Depends(get_session)
):

    os.makedirs("app/uploads", exist_ok=True)
    file_location = f"app/uploads/{image.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    image_path = f"uploads/{image.filename}"
    blog = Blog(title=title, description=description, image=image_path)
    blog = create_blog(session, blog)
    if blog.image:
        blog.image = f"{request.base_url}{blog.image}"
    return blog


# GET ALL BLOGS
@router.get("/", response_model=list[BlogResponse])
def get_blogs(request: Request, session: Session = Depends(get_session)):

    blogs = get_all_blogs(session)
    for blog in blogs:
        if blog.image:
            blog.image = f"{request.base_url}{blog.image}"
    return blogs


# GET SINGLE BLOG
@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, request: Request, session: Session = Depends(get_session)):

    blog = get_single_blog(session, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.image:
        blog.image = f"{request.base_url}{blog.image}"
    return blog


# DELETE BLOG
@router.delete("/{blog_id}")
def delete_blog_api(blog_id: int, session: Session = Depends(get_session)):

    result = delete_blog(session, blog_id)
    if not result:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}