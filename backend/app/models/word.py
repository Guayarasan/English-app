"""Catálogo de vocabulario. Es contenido global, no por usuario."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.mixins import TimestampMixin


class Word(Base, TimestampMixin):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    text_en = Column(String, nullable=False, index=True)
    text_es = Column(String, nullable=False)
    category = Column(String, index=True, nullable=True)  # ej: "food", "travel"
    difficulty = Column(Integer, default=1, nullable=False)  # 1-5
    example_sentence_en = Column(String, nullable=True)
    example_sentence_es = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)

    user_words = relationship("UserWord", back_populates="word")
