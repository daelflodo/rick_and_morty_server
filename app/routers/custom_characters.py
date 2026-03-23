from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.custom_character import CustomCharacterCreate, CustomCharacterOut, CustomCharacterUpdate
from app.services.custom_character_service import (
    create_custom_character,
    delete_custom_character,
    get_custom_character,
    get_custom_characters,
    update_custom_character,
)

router = APIRouter(prefix="/api/custom-characters", tags=["custom-characters"])


@router.get("", response_model=list[CustomCharacterOut])
def list_custom_characters(
    name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    species: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    sort: Optional[str] = Query(None, pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_custom_characters(
        db, current_user.id, name=name, char_status=status, species=species, gender=gender, sort=sort
    )


@router.post("", response_model=CustomCharacterOut, status_code=201)
def create(
    data: CustomCharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_custom_character(db, current_user.id, data)


@router.get("/{character_id}", response_model=CustomCharacterOut)
def get_one(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_custom_character(db, current_user.id, character_id)


@router.put("/{character_id}", response_model=CustomCharacterOut)
def update(
    character_id: int,
    data: CustomCharacterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_custom_character(db, current_user.id, character_id, data)


@router.delete("/{character_id}", status_code=204)
def delete(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_custom_character(db, current_user.id, character_id)
