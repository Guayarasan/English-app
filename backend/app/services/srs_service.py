"""
Motor de repaso espaciado (SRS).

Algoritmo: variante simplificada de SM-2.
- Acierto: el intervalo crece multiplicado por ease_factor; ease_factor
  sube ligeramente (tope 3.0).
- Fallo: el intervalo vuelve a 1 día; ease_factor baja (piso 1.3);
  fail_count sube, lo que la hace más prioritaria en la cola aunque su
  next_review_at todavía no haya llegado.

Selección de palabras "debidas hoy" (get_due_words):
1. Palabras nuevas para el usuario (sin UserWord todavía) — introduce
   vocabulario nuevo.
2. Palabras con next_review_at <= ahora, ordenadas primero por
   fail_count descendente (las más falladas se repiten más) y luego
   por next_review_at ascendente (las más atrasadas primero).
"""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.word import Word
from app.models.user_word import UserWord

EASE_MIN = 1.3
EASE_MAX = 3.0
LEARNED_THRESHOLD_INTERVAL_DAYS = 21


def get_or_create_user_word(db: Session, user_id: int, word_id: int) -> UserWord:
    user_word = (
        db.query(UserWord)
        .filter(UserWord.user_id == user_id, UserWord.word_id == word_id)
        .first()
    )
    if user_word is None:
        user_word = UserWord(user_id=user_id, word_id=word_id)
        db.add(user_word)
        db.flush()
    return user_word


def apply_review_result(user_word: UserWord, is_correct: bool) -> UserWord:
    now = datetime.now(timezone.utc)

    if is_correct:
        user_word.success_count += 1
        user_word.interval_days = max(1, round(user_word.interval_days * user_word.ease_factor))
        user_word.ease_factor = min(EASE_MAX, user_word.ease_factor + 0.1)
        if user_word.interval_days >= LEARNED_THRESHOLD_INTERVAL_DAYS:
            user_word.is_learned = 1
    else:
        user_word.fail_count += 1
        user_word.interval_days = 1
        user_word.ease_factor = max(EASE_MIN, user_word.ease_factor - 0.3)
        user_word.is_learned = 0

    user_word.next_review_at = now + timedelta(days=user_word.interval_days)
    return user_word


def get_due_words(db: Session, user_id: int, limit: int = 15) -> list[Word]:
    now = datetime.now(timezone.utc)

    # Palabras ya en repaso, debidas ahora, priorizadas por fallos
    due_user_words = (
        db.query(UserWord)
        .filter(
            UserWord.user_id == user_id,
            UserWord.next_review_at <= now,
            UserWord.is_learned == 0,
        )
        .order_by(UserWord.fail_count.desc(), UserWord.next_review_at.asc())
        .limit(limit)
        .all()
    )
    due_words = [uw.word for uw in due_user_words]

    remaining = limit - len(due_words)
    if remaining <= 0:
        return due_words

    # Completa con palabras nuevas que el usuario nunca ha visto
    seen_word_ids = (
        db.query(UserWord.word_id).filter(UserWord.user_id == user_id).subquery()
    )
    new_words = (
        db.query(Word)
        .filter(~Word.id.in_(seen_word_ids))
        .order_by(Word.difficulty.asc())
        .limit(remaining)
        .all()
    )
    return due_words + new_words
