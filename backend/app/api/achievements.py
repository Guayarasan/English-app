from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement
from app.schemas.achievement import AchievementOut

router = APIRouter(prefix="/api/achievements", tags=["achievements"])


@router.get("", response_model=list[AchievementOut])
def list_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    unlocked_map = {
        ua.achievement_id: ua.unlocked_at
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    }
    all_achievements = db.query(Achievement).all()

    return [
        AchievementOut(
            code=a.code,
            title=a.title,
            description=a.description,
            xp_reward=a.xp_reward,
            unlocked=a.id in unlocked_map,
            unlocked_at=unlocked_map.get(a.id),
        )
        for a in all_achievements
    ]
