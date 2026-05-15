from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.database import create_db_and_tables

from app.blog import router as blog_router

app = FastAPI()

@app.on_event("startup")
def on_startup():

    create_db_and_tables()

# Serve uploads folder
app.mount(
    "/app/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads"
)

app.include_router(blog_router)