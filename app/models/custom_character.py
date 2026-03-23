from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class CustomCharacter(Base):
    __tablename__ = "custom_characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("rick_and_morty.users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    species = Column(String(100), nullable=False)
    gender = Column(String(50), nullable=False)
    origin = Column(String(200), nullable=False)
    image = Column(String(500), nullable=False)

    user = relationship("User", back_populates="custom_characters")
