
from pydantic import BaseModel

class Table(BaseModel):
    number: int
    capacity: int
    status: str = "Livre"  # Livre, Ocupada, Reservada


