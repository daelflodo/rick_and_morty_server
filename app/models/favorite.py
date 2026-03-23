from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("rick_and_morty.users.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(Integer, nullable=False)
    character_name = Column(String(200), nullable=False)
    character_status = Column(String(50), nullable=False)
    character_species = Column(String(100), nullable=False)
    character_gender = Column(String(50), nullable=False)
    character_origin = Column(String(200), nullable=False)
    character_image = Column(String(500), nullable=False)
    user = relationship("User", back_populates="favorites")
    __table_args__ = (UniqueConstraint("user_id", "character_id", name="uq_user_character"),)
