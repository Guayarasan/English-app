"""
Attempt: registro de cada intento de ejercicio que hace un usuario.
Es la fuente de verdad para el historial de progreso y las estadísticas
detalladas (precisión por categoría, evolución en el tiempo, etc.).
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.mixins import TimestampMixin


class Attempt(Base, TimestampMixin):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    exercise_type = Column(String, nullable=False)  # translation | fill_blank | writing | flashcard
    is_correct = Column(Boolean, nullable=False)
    user_answer = Column(String, nullable=True)
    xp_earned = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="attempts")
