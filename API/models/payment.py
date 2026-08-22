
from pydantic import BaseModel

class Payment(BaseModel):
    order_id: int
    method: str  # Pix, Cartão, Dinheiro
    amount: float

