from typing import Optional
from pydantic import BaseModel

class Review(BaseModel):
    order_id: int
    rating: int  # 1 a 5
    comment: Optional[str] = None

