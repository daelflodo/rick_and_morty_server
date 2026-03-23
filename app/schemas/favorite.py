from pydantic import BaseModel


class FavoriteAdd(BaseModel):
    character_id: int


class FavoriteOut(BaseModel):
    id: int
    character_id: int
    character_name: str
    character_status: str
    character_species: str
    character_gender: str
    character_origin: str
    character_image: str
    model_config = {"from_attributes": True}
