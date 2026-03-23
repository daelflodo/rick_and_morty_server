from typing import Optional

from pydantic import BaseModel, Field


class CustomCharacterCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    status: str = Field(..., pattern="^(Alive|Dead|unknown)$")
    species: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., pattern="^(Female|Male|Genderless|unknown)$")
    origin: str = Field(..., min_length=1, max_length=200)
    image: str = Field(..., min_length=1, max_length=500)


class CustomCharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = Field(None, pattern="^(Alive|Dead|unknown)$")
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[str] = Field(None, pattern="^(Female|Male|Genderless|unknown)$")
    origin: Optional[str] = Field(None, min_length=1, max_length=200)
    image: Optional[str] = Field(None, min_length=1, max_length=500)


class CustomCharacterOut(BaseModel):
    id: int
    name: str
    status: str
    species: str
    gender: str
    origin: str
    image: str

    model_config = {"from_attributes": True}
