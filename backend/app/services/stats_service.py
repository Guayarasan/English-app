"""
Agregaciones para la sección de estadísticas.

Todo se calcula al vuelo con GROUP BY sobre Attempt/UserWord en vez de
mantener contadores desnormalizados — el volumen por usuario es bajo
(cientos/miles de intentos) así que no vale la pena la complejidad de
cachear, y evita que las estadísticas se desincronicen del historial
real de intentos.
"""
from datetime import date, timedelta

from sqlalchemy import func, Integer
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.user_word import UserWord
from app.models.word import Word


def get_summary(db: Session, user_id: int) -> dict:
    total_attempts = db.query(Attempt).filter(Attempt.user_id == user_id).count()
    correct_attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user_id, Attempt.is_correct.is_(True))
        .count()
    )
    words_learned = (
        db.query(UserWord)
        .filter(UserWord.user_id == user_id, UserWord.is_learned == 1)
        .count()
    )
    words_in_progress = (
        db.query(UserWord)
        .filter(UserWord.user_id == user_id, UserWord.is_learned == 0)
        .count()
    )
    accuracy = round(100 * correct_attempts / total_attempts, 1) if total_attempts else 0.0

    return {
        "total_attempts": total_attempts,
        "correct_attempts": correct_attempts,
        "accuracy": accuracy,
        "words_learned": words_learned,
        "words_in_progress": words_in_progress,
    }


def get_daily_history(db: Session, user_id: int, days: int = 30) -> list[dict]:
    since = date.today() - timedelta(days=days - 1)

    rows = (
        db.query(
            func.date(Attempt.created_at).label("day"),
            func.count(Attempt.id).label("total"),
            func.sum(func.cast(Attempt.is_correct, Integer)).label("correct"),
        )
        .filter(Attempt.user_id == user_id, func.date(Attempt.created_at) >= since)
        .group_by(func.date(Attempt.created_at))
        .order_by(func.date(Attempt.created_at))
        .all()
    )

    by_day = {}
    for row in rows:
        day_str = str(row.day)
        total = row.total or 0
        correct = row.correct or 0
        by_day[day_str] = {
            "date": day_str,
            "attempts": total,
            "accuracy": round(100 * correct / total, 1) if total else 0.0,
        }

    # Rellena los días sin actividad con 0, para que el gráfico no tenga huecos
    result = []
    for i in range(days):
        day = since + timedelta(days=i)
        day_str = str(day)
        result.append(by_day.get(day_str, {"date": day_str, "attempts": 0, "accuracy": 0.0}))
    return result


def get_category_accuracy(db: Session, user_id: int) -> list[dict]:
    rows = (
        db.query(
            Word.category,
            func.count(Attempt.id).label("total"),
            func.sum(func.cast(Attempt.is_correct, Integer)).label("correct"),
        )
        .join(Attempt, Attempt.word_id == Word.id)
        .filter(Attempt.user_id == user_id, Word.category.isnot(None))
        .group_by(Word.category)
        .all()
    )
    return [
        {
            "category": row.category,
            "attempts": row.total,
            "accuracy": round(100 * (row.correct or 0) / row.total, 1) if row.total else 0.0,
        }
        for row in rows
    ]


def get_hardest_words(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    rows = (
        db.query(UserWord, Word)
        .join(Word, Word.id == UserWord.word_id)
        .filter(UserWord.user_id == user_id, UserWord.fail_count > 0)
        .order_by(UserWord.fail_count.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "text_en": word.text_en,
            "text_es": word.text_es,
            "fail_count": uw.fail_count,
            "success_count": uw.success_count,
        }
        for uw, word in rows
    ]
