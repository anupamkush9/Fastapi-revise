import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlmodel import Session

from app.database import get_session

from app.models import Blog

from app.crud import (
    create_blog,
    get_all_blogs,
    get_single_blog,
    delete_blog
)


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


# CREATE BLOG
@router.post("/")
def create_blog_api(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_session)
):

    # Create uploads folder
    os.makedirs("app/uploads", exist_ok=True)

    # Save image
    image_path = f"app/uploads/{image.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Create DB object
    blog = Blog(
        title=title,
        description=description,
        image=image_path
    )

    return create_blog(session, blog)


# GET ALL BLOGS
@router.get("/")
def get_blogs(
    session: Session = Depends(get_session)
):

    return get_all_blogs(session)


# GET SINGLE BLOG
@router.get("/{blog_id}")
def get_blog(
    blog_id: int,
    session: Session = Depends(get_session)
):

    blog = get_single_blog(session, blog_id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return blog


# DELETE BLOG
@router.delete("/{blog_id}")
def delete_blog_api(
    blog_id: int,
    session: Session = Depends(get_session)
):

    result = delete_blog(session, blog_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return {"message": "Blog deleted successfully"}
