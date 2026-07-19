"""
UserWord: relación N:M entre User y Word, y estado del algoritmo SRS.

Este es el núcleo del "repaso inteligente". Cada fila representa el
progreso de UN usuario con UNA palabra:
- ease_factor: qué tan "fácil" es la palabra para este usuario (SM-2 simplificado)
- interval_days: cada cuánto se vuelve a mostrar
- next_review_at: fecha exacta del próximo repaso
- fail_count / success_count: usados para priorizar en la cola de repaso
  (más fallos => aparece con más frecuencia, independientemente del interval)
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.mixins import TimestampMixin


class UserWord(Base, TimestampMixin):
    __tablename__ = "user_words"
    __table_args__ = (UniqueConstraint("user_id", "word_id", name="uq_user_word"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    ease_factor = Column(Float, default=2.5, nullable=False)
    interval_days = Column(Integer, default=1, nullable=False)
    next_review_at = Column(DateTime(timezone=True), nullable=True)

    fail_count = Column(Integer, default=0, nullable=False)
    success_count = Column(Integer, default=0, nullable=False)
    is_learned = Column(Integer, default=0, nullable=False)  # 0/1, se marca al pasar cierto umbral

    user = relationship("User", back_populates="user_words")
    word = relationship("Word", back_populates="user_words")
