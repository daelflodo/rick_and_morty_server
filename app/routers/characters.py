from typing import Optional

from fastapi import APIRouter, Query

from app.services.character_service import (
    fetch_character_by_id,
    fetch_random_characters,
    filter_characters,
)

router = APIRouter(prefix="/api/characters", tags=["characters"])


@router.get("/random")
async def get_random_characters(count: int = 10):
    return await fetch_random_characters(count)


@router.get("/search")
async def search_characters(
    name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    species: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    sort: Optional[str] = Query(None, pattern="^(asc|desc)$"),
):
    return await filter_characters(
        name=name, char_status=status, species=species, gender=gender, sort=sort
    )


@router.get("/{character_id}")
async def get_character(character_id: int):
    return await fetch_character_by_id(character_id)
