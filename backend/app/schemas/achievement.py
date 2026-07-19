from datetime import datetime
from pydantic import BaseModel


class AchievementOut(BaseModel):
    code: str
    title: str
    description: str
    xp_reward: int
    unlocked: bool
    unlocked_at: datetime | None = None
