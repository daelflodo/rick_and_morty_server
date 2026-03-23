from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.services.character_service import fetch_character_by_id


def get_user_favorites(db: Session, user_id: int) -> list[Favorite]:
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


async def add_favorite(db: Session, user_id: int, character_id: int) -> Favorite:
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id, Favorite.character_id == character_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Character already in favorites")

    data = await fetch_character_by_id(character_id)
    origin = data.get("origin", {})
    origin_name = origin.get("name", "Unknown") if isinstance(origin, dict) else "Unknown"

    favorite = Favorite(
        user_id=user_id,
        character_id=character_id,
        character_name=data["name"],
        character_status=data["status"],
        character_species=data["species"],
        character_gender=data["gender"],
        character_origin=origin_name,
        character_image=data["image"],
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def remove_favorite(db: Session, user_id: int, character_id: int) -> None:
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id, Favorite.character_id == character_id
    ).first()
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
