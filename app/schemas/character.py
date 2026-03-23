from pydantic import BaseModel


class CharacterOrigin(BaseModel):
    name: str
    url: str


class CharacterOut(BaseModel):
    id: int
    name: str
    status: str
    species: str
    gender: str
    origin: CharacterOrigin
    image: str
