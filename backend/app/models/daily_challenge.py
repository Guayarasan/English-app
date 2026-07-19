"""
DailyChallenge: catálogo fijo de tipos de desafío (no rotan por ahora,
los 3 se ofrecen todos los días — mantiene el sistema simple y
predecible para el usuario).

UserChallengeProgress: el avance de un usuario en un desafío para una
fecha concreta. Se resetea solo porque la fecha cambia, no hay job de
limpieza: una fila nueva se crea la primera vez que hay progreso ese día.

metric determina qué evento del review lo hace avanzar:
- words_reviewed: cada respuesta cuenta (correcta o no)
- correct_answers: solo respuestas correctas
- new_words: solo la primera vez que se repasa una palabra (word nueva)
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.mixins import TimestampMixin


class DailyChallenge(Base, TimestampMixin):
    __tablename__ = "daily_challenges"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    metric = Column(String, nullable=False)  # words_reviewed | correct_answers | new_words
    target_count = Column(Integer, nullable=False)
    xp_reward = Column(Integer, default=0, nullable=False)


class UserChallengeProgress(Base, TimestampMixin):
    __tablename__ = "user_challenge_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", "date", name="uq_user_challenge_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("daily_challenges.id"), nullable=False)
    date = Column(Date, nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    challenge = relationship("DailyChallenge")
