from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    number: str
    complement: Optional[str] = None
    city: str