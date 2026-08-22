from pydantic import BaseModel

class OptionGroup(BaseModel):
    name: str
    min_options: int
    max_options: int

