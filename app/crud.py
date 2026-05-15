from sqlmodel import Session, select

from .models import Blog


def create_blog(session: Session, blog_data: Blog):

    session.add(blog_data)

    session.commit()

    session.refresh(blog_data)

    return blog_data


def get_all_blogs(session: Session):

    statement = select(Blog)

    return session.exec(statement).all()


def get_single_blog(session: Session, blog_id: int):

    return session.get(Blog, blog_id)


def delete_blog(session: Session, blog_id: int):

    blog = session.get(Blog, blog_id)

    if not blog:
        return None

    session.delete(blog)

    session.commit()

    return True