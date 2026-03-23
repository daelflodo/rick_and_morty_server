from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.custom_character import CustomCharacter
from app.schemas.custom_character import CustomCharacterCreate, CustomCharacterUpdate


def get_custom_characters(
    db: Session,
    user_id: int,
    name: Optional[str] = None,
    char_status: Optional[str] = None,
    species: Optional[str] = None,
    gender: Optional[str] = None,
    sort: Optional[str] = None,
) -> list[CustomCharacter]:
    query = db.query(CustomCharacter).filter(CustomCharacter.user_id == user_id)

    if name:
        query = query.filter(CustomCharacter.name.ilike(f"%{name}%"))
    if char_status:
        query = query.filter(CustomCharacter.status == char_status)
    if species:
        query = query.filter(CustomCharacter.species.ilike(f"%{species}%"))
    if gender:
        query = query.filter(CustomCharacter.gender == gender)

    order = desc(CustomCharacter.name) if sort == "desc" else asc(CustomCharacter.name)
    return query.order_by(order).all()


def get_custom_character(db: Session, user_id: int, character_id: int) -> CustomCharacter:
    character = (
        db.query(CustomCharacter)
        .filter(CustomCharacter.id == character_id, CustomCharacter.user_id == user_id)
        .first()
    )
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return character


def create_custom_character(
    db: Session, user_id: int, data: CustomCharacterCreate
) -> CustomCharacter:
    character = CustomCharacter(user_id=user_id, **data.model_dump())
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


def update_custom_character(
    db: Session, user_id: int, character_id: int, data: CustomCharacterUpdate
) -> CustomCharacter:
    character = get_custom_character(db, user_id, character_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return character


def delete_custom_character(db: Session, user_id: int, character_id: int) -> None:
    character = get_custom_character(db, user_id, character_id)
    db.delete(character)
    db.commit()
