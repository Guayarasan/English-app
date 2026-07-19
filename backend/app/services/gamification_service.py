"""
Lógica de gamificación reutilizable.

XP_PER_CORRECT_ANSWER es la base; el nivel se deriva del XP total con
una curva simple (cada nivel pide un poco más que el anterior) en vez
de una tabla fija, para no tener que mantenerla a mano al agregar
niveles.

La racha se actualiza a la primera actividad del día:
- Si la última actividad fue ayer -> +1 racha.
- Si la última actividad fue hoy -> no cambia (ya contaba hoy).
- Si hay un hueco de más de un día -> la racha se rompe y vuelve a 1,
  salvo que el usuario tenga streak_freezes disponibles (se consume uno
  y la racha se mantiene).
"""
from datetime import date, timedelta

from app.models.user import User

XP_PER_CORRECT_ANSWER = 10
XP_PER_INCORRECT_ANSWER = 2  # XP de consolación por intentar


def xp_for_level(level: int) -> int:
    """XP acumulado necesario para alcanzar `level`."""
    return int(50 * level * (level + 1) / 2)


def level_from_xp(xp: int) -> int:
    level = 1
    while xp_for_level(level + 1) <= xp:
        level += 1
    return level


def award_xp(user: User, is_correct: bool) -> int:
    earned = XP_PER_CORRECT_ANSWER if is_correct else XP_PER_INCORRECT_ANSWER
    user.xp += earned
    user.level = level_from_xp(user.xp)
    return earned


def register_daily_activity(user: User) -> None:
    today = date.today()

    if user.last_activity_date == today:
        return  # ya contaba hoy

    if user.last_activity_date == today - timedelta(days=1):
        user.current_streak += 1
    elif user.last_activity_date is None:
        user.current_streak = 1
    else:
        gap_days = (today - user.last_activity_date).days
        if gap_days > 1 and user.streak_freezes > 0:
            user.streak_freezes -= 1  # perdona el hueco, la racha sigue
            user.current_streak += 1
        else:
            user.current_streak = 1  # racha rota, se reinicia

    user.longest_streak = max(user.longest_streak, user.current_streak)
    user.last_activity_date = today
