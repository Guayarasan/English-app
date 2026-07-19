from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.review import ChallengeProgressOut
from app.services import daily_challenge_service

router = APIRouter(prefix="/api/challenges", tags=["challenges"])


@router.get("/today", response_model=list[ChallengeProgressOut])
def get_today_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    progresses = daily_challenge_service.get_today_progress(db, current_user.id)
    db.commit()  # persiste filas de progreso recién creadas en 0

    return [
        ChallengeProgressOut(
            code=p.challenge.code,
            title=p.challenge.title,
            description=p.challenge.description,
            target_count=p.challenge.target_count,
            progress=p.progress,
            completed=p.completed,
            xp_reward=p.challenge.xp_reward,
        )
        for p in progresses
    ]
