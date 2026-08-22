

from pydantic import BaseModel

class Category(BaseModel):
    name: str
    active: bool = True

