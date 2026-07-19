"""
Sistema de logros.

Las condiciones se evalúan en código (no en SQL guardado) contra el
estado ya cargado del usuario + un conteo de palabras aprendidas, para
mantener el catálogo fácil de leer y extender. check_and_unlock corre
después de cada respuesta y de la actualización de racha/XP, así que
lee valores ya frescos.
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_word import UserWord
from app.models.achievement import Achievement, UserAchievement

# code -> (título, descripción, condición, xp_reward)
ACHIEVEMENT_CATALOG = [
    dict(code="streak_3", title="Viajero constante", description="Alcanza 3 días de racha",
         xp_reward=15, check=lambda u, learned: u.current_streak >= 3),
    dict(code="streak_7", title="Una semana de viaje", description="Alcanza 7 días de racha",
         xp_reward=40, check=lambda u, learned: u.current_streak >= 7),
    dict(code="streak_30", title="Viajero frecuente", description="Alcanza 30 días de racha",
         xp_reward=150, check=lambda u, learned: u.current_streak >= 30),
    dict(code="level_5", title="Nivel 5: hablante inicial", description="Llega al nivel 5",
         xp_reward=30, check=lambda u, learned: u.level >= 5),
    dict(code="level_10", title="Nivel 10: viajero experto", description="Llega al nivel 10",
         xp_reward=60, check=lambda u, learned: u.level >= 10),
    dict(code="words_10", title="Primeras postales", description="Aprende 10 palabras",
         xp_reward=20, check=lambda u, learned: learned >= 10),
    dict(code="words_50", title="Vocabulario de viaje", description="Aprende 50 palabras",
         xp_reward=80, check=lambda u, learned: learned >= 50),
    dict(code="words_200", title="Políglota en formación", description="Aprende 200 palabras",
         xp_reward=250, check=lambda u, learned: learned >= 200),
]


def ensure_catalog_seeded(db: Session) -> None:
    existing_codes = {a.code for a in db.query(Achievement.code).all()}
    for item in ACHIEVEMENT_CATALOG:
        if item["code"] not in existing_codes:
            db.add(Achievement(
                code=item["code"],
                title=item["title"],
                description=item["description"],
                xp_reward=item["xp_reward"],
            ))
    db.commit()


def count_learned_words(db: Session, user_id: int) -> int:
    return (
        db.query(UserWord)
        .filter(UserWord.user_id == user_id, UserWord.is_learned == 1)
        .count()
    )


def check_and_unlock(db: Session, user: User) -> list[Achievement]:
    """Revisa el catálogo y desbloquea lo que ya se cumple. Devuelve los nuevos."""
    learned = count_learned_words(db, user.id)

    already_unlocked = {
        ua.achievement_id
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    }
    catalog_by_code = {a.code: a for a in db.query(Achievement).all()}

    newly_unlocked = []
    for item in ACHIEVEMENT_CATALOG:
        achievement = catalog_by_code.get(item["code"])
        if not achievement or achievement.id in already_unlocked:
            continue
        if item["check"](user, learned):
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id,
                unlocked_at=datetime.now(timezone.utc),
            )
            db.add(user_achievement)
            user.xp += achievement.xp_reward
            newly_unlocked.append(achievement)

    return newly_unlocked
