"""
Achievement: catálogo global de logros disponibles (ej: "7 días de racha").
UserAchievement: cuáles ha desbloqueado cada usuario y cuándo.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint

from app.db.database import Base
from app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Achievement(Base, TimestampMixin):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)  # ej: "streak_7"
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    xp_reward = Column(Integer, default=0, nullable=False)

    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base, TimestampMixin):
    __tablename__ = "user_achievements"
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
