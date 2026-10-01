"""
Endpoints del motor de repaso inteligente.

GET  /api/review/due     -> qué palabras tocan hoy (nuevas + falladas + vencidas)
POST /api/review/answer  -> registra un intento, actualiza SRS, XP, nivel,
                             racha, progreso de desafíos diarios y logros

Todo el estado se actualiza en una sola transacción por respuesta.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.word import Word
from app.models.attempt import Attempt
from app.schemas.review import (
    AnswerSubmit,
    AnswerResult,
    DueWordsOut,
    AchievementUnlocked,
    ChallengeCompleted,
)
from app.services import (
    srs_service,
    gamification_service,
    daily_challenge_service,
    achievement_service,
    exercise_service,
)

router = APIRouter(prefix="/api/review", tags=["review"])

EXERCISE_TYPES = {"flashcard", "translation", "fill_blank", "writing"}


def _resolve_is_correct(payload: AnswerSubmit, word: Word) -> bool:
    """
    'flashcard' confía en la autoevaluación del usuario (no hay nada
    objetivo que validar ahí). El resto se valida en el servidor para
    que el XP y el SRS no dependan de lo que mande el cliente.
    """
    if payload.exercise_type == "flashcard":
        if payload.is_correct is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="flashcard requiere is_correct",
            )
        return payload.is_correct
    if payload.exercise_type == "translation":
        return exercise_service.check_translation(word, payload.user_answer, payload.direction)
    if payload.exercise_type == "fill_blank":
        return exercise_service.check_fill_blank(word, payload.user_answer)
    if payload.exercise_type == "writing":
        return exercise_service.check_writing(word, payload.user_answer)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de ejercicio inválido")


@router.get("/due", response_model=DueWordsOut)
def get_due_words(
    limit: int = Query(default=15, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    words = srs_service.get_due_words(db, current_user.id, limit=limit)
    return DueWordsOut(words=words, count=len(words))


@router.post("/answer", response_model=AnswerResult)
def submit_answer(
    payload: AnswerSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.exercise_type not in EXERCISE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de ejercicio inválido")

    word = db.query(Word).filter(Word.id == payload.word_id).first()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Palabra no encontrada")

    is_correct = _resolve_is_correct(payload, word)

    user_word = srs_service.get_or_create_user_word(db, current_user.id, word.id)
    is_new_word = (user_word.success_count + user_word.fail_count) == 0

    srs_service.apply_review_result(user_word, is_correct)

    xp_earned = gamification_service.award_xp(current_user, is_correct)
    gamification_service.register_daily_activity(current_user)

    completed_challenges = daily_challenge_service.register_review_event(
        db, current_user, is_correct=is_correct, is_new_word=is_new_word
    )
    unlocked_achievements = achievement_service.check_and_unlock(db, current_user)
    # Los desafíos y logros suman XP extra: el nivel se recalcula al final
    # para que no quede desfasado respecto al XP total.
    current_user.level = gamification_service.level_from_xp(current_user.xp)

    attempt = Attempt(
        user_id=current_user.id,
        word_id=word.id,
        exercise_type=payload.exercise_type,
        is_correct=is_correct,
        user_answer=payload.user_answer,
        xp_earned=xp_earned,
    )
    db.add(attempt)
    db.commit()
    db.refresh(current_user)

    return AnswerResult(
        is_correct=is_correct,
        correct_answer=exercise_service.get_correct_answer(word, payload.exercise_type, payload.direction),
        xp_earned=xp_earned,
        total_xp=current_user.xp,
        level=current_user.level,
        current_streak=current_user.current_streak,
        next_review_at=user_word.next_review_at.isoformat() if user_word.next_review_at else None,
        achievements_unlocked=[
            AchievementUnlocked(
                code=a.code, title=a.title, description=a.description, xp_reward=a.xp_reward
            )
            for a in unlocked_achievements
        ],
        challenges_completed=[
            ChallengeCompleted(
                code=p.challenge.code, title=p.challenge.title, xp_reward=p.challenge.xp_reward
            )
            for p in completed_challenges
        ],
    )
