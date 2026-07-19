"""
Desafíos diarios. El catálogo es fijo (3 desafíos, siempre los mismos)
para que el usuario aprenda a reconocerlos; lo que cambia día a día es
solo el progreso, guardado en UserChallengeProgress con la fecha.
"""
from datetime import date

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.daily_challenge import DailyChallenge, UserChallengeProgress

CHALLENGE_CATALOG = [
    dict(code="review_10", title="Diez sellos", description="Repasa 10 palabras hoy",
         metric="words_reviewed", target_count=10, xp_reward=20),
    dict(code="correct_5", title="Buena puntería", description="Acierta 5 palabras hoy",
         metric="correct_answers", target_count=5, xp_reward=15),
    dict(code="new_3", title="Nuevo destino", description="Aprende 3 palabras nuevas hoy",
         metric="new_words", target_count=3, xp_reward=25),
]


def ensure_catalog_seeded(db: Session) -> None:
    existing_codes = {c.code for c in db.query(DailyChallenge.code).all()}
    for item in CHALLENGE_CATALOG:
        if item["code"] not in existing_codes:
            db.add(DailyChallenge(**item))
    db.commit()


def get_today_progress(db: Session, user_id: int) -> list[UserChallengeProgress]:
    today = date.today()
    challenges = db.query(DailyChallenge).all()
    results = []
    for challenge in challenges:
        progress = (
            db.query(UserChallengeProgress)
            .filter(
                UserChallengeProgress.user_id == user_id,
                UserChallengeProgress.challenge_id == challenge.id,
                UserChallengeProgress.date == today,
            )
            .first()
        )
        if progress is None:
            progress = UserChallengeProgress(
                user_id=user_id, challenge_id=challenge.id, date=today, progress=0
            )
            db.add(progress)
            db.flush()
        results.append(progress)
    return results


def register_review_event(
    db: Session, user: User, *, is_correct: bool, is_new_word: bool
) -> list[UserChallengeProgress]:
    """Avanza el progreso de los desafíos de hoy según el intento recién hecho."""
    progresses = get_today_progress(db, user.id)
    newly_completed = []

    for progress in progresses:
        metric = progress.challenge.metric
        matches = (
            metric == "words_reviewed"
            or (metric == "correct_answers" and is_correct)
            or (metric == "new_words" and is_new_word)
        )
        if not matches or progress.completed:
            continue

        progress.progress += 1
        if progress.progress >= progress.challenge.target_count:
            progress.completed = True
            user.xp += progress.challenge.xp_reward
            newly_completed.append(progress)

    return newly_completed
