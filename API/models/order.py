from pydantic import BaseModel
from typing import List


class Order(BaseModel):
    user_id: int
    items: List[dict]
    total: float
    status: str = "Pendente"  # Pendente, Em Preparo, A Caminho, Concluído

