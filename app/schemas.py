from datetime import datetime
from pydantic import BaseModel

# why schemas - separate request/response validation from DB models
class BlogCreate(BaseModel):
    title: str
    description: str

class BlogResponse(BaseModel):
    id: int
    title: str
    description: str
    image: str | None
    created_at: datetime
