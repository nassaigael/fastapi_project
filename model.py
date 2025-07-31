from pydantic import BaseModel

class Player(BaseModel):
    Number: int
    Name: str