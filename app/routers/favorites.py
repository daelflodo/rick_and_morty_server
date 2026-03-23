from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.favorite import FavoriteAdd, FavoriteOut
from app.services.favorites_service import add_favorite, get_user_favorites, remove_favorite

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=list[FavoriteOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_favorites(db, current_user.id)


@router.post("", response_model=FavoriteOut, status_code=201)
async def add_to_favorites(
    data: FavoriteAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_favorite(db, current_user.id, data.character_id)


@router.delete("/{character_id}", status_code=204)
def remove_from_favorites(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    remove_favorite(db, current_user.id, character_id)
