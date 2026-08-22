from pydantic import BaseModel

class Coupon(BaseModel):
    code: str
    discount_percentage: float
    active: bool = True
