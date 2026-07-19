from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.stats import StatsSummary, DailyStat, CategoryStat, HardWord
from app.services import stats_service

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/summary", response_model=StatsSummary)
def summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stats_service.get_summary(db, current_user.id)


@router.get("/history", response_model=list[DailyStat])
def history(
    days: int = Query(default=30, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stats_service.get_daily_history(db, current_user.id, days=days)


@router.get("/categories", response_model=list[CategoryStat])
def categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stats_service.get_category_accuracy(db, current_user.id)


@router.get("/hardest-words", response_model=list[HardWord])
def hardest_words(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stats_service.get_hardest_words(db, current_user.id, limit=limit)
