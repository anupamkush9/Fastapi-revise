from sqlmodel import Session, select
from .models import Blog

def create_blog(session: Session, blog_data: Blog):
    session.add(blog_data)
    session.commit()
    session.refresh(blog_data)
    return blog_data


def get_all_blogs(
    session: Session,
    page: int = 1,
    page_size: int = 10,
    order: str = "desc",
):
    offset = (page - 1) * page_size
    statement = select(Blog)

    if order == "asc":
        statement = statement.order_by(Blog.id.asc())
    else:
        statement = statement.order_by(Blog.id.desc())

    statement = (statement.offset(offset).limit(page_size))
    blogs = session.exec(statement).all()
    total_count = len(session.exec(select(Blog)).all())

    return {
        "pagination": {
            "count": total_count,
            "page": page,
            "page_size": page_size,
        },
        "results": blogs,
    }

def get_single_blog(session: Session, blog_id: int):
    return session.get(Blog, blog_id)

def update_blog( session: Session, blog_id: int, title: str, description: str, image_path: str | None = None):
    blog = session.get(Blog, blog_id)
    if not blog:
        return None

    blog.title = title
    blog.description = description
    # Update image only if new image uploaded
    if image_path:
        blog.image = image_path

    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

def delete_blog(session: Session, blog_id: int):
    blog = session.get(Blog, blog_id)
    if not blog:
        return None
    session.delete(blog)
    session.commit()
    return True