import random
from typing import Optional

import httpx
from fastapi import HTTPException, status

from app.config import get_settings

settings = get_settings()


async def fetch_character_by_id(character_id: int) -> dict:
    url = f"{settings.RICK_AND_MORTY_API_URL}/character/{character_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    response.raise_for_status()
    return response.json()


async def fetch_characters_by_ids(ids: list) -> list:
    if not ids:
        return []
    ids_str = ",".join(str(i) for i in ids)
    url = f"{settings.RICK_AND_MORTY_API_URL}/character/{ids_str}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else [data]


async def filter_characters(
    name: Optional[str] = None,
    char_status: Optional[str] = None,
    species: Optional[str] = None,
    gender: Optional[str] = None,
    sort: Optional[str] = None,
) -> list:
    params: dict = {}
    if name:
        params["name"] = name
    if char_status:
        params["status"] = char_status
    if species:
        params["species"] = species
    if gender:
        params["gender"] = gender

    url = f"{settings.RICK_AND_MORTY_API_URL}/character/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code == 404:
        return []
    response.raise_for_status()
    characters: list = response.json().get("results", [])

    if sort:
        characters = sorted(characters, key=lambda c: c["name"].lower(), reverse=(sort == "desc"))

    return characters


async def fetch_random_characters(count: int = 10) -> list:
    ids = random.sample(range(1, 827), min(count, 826))
    return await fetch_characters_by_ids(ids)
