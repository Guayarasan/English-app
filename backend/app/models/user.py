"""
Modelo de Usuario.

Los campos de gamificación (xp, level, streak) viven aquí en vez de en una
tabla aparte porque se leen en casi cada request (header/dashboard) y no
justifican un join extra. current_streak/last_activity_date son la fuente
de verdad para calcular si la racha sigue viva o se rompió.
"""
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Gamificación
    xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_activity_date = Column(Date, nullable=True)
    streak_freezes = Column(Integer, default=0, nullable=False)  # "perdón" por faltar un día

    # Relaciones
    user_words = relationship("UserWord", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    user_achievements = relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
    )
