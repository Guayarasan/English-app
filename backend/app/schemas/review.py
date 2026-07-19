from pydantic import BaseModel
from app.schemas.word import WordOut


class AnswerSubmit(BaseModel):
    word_id: int
    exercise_type: str  # translation | fill_blank | writing | flashcard
    is_correct: bool | None = None  # solo para flashcard (autoevaluación)
    user_answer: str | None = None  # requerido para translation/fill_blank/writing
    direction: str = "en_to_es"  # en_to_es | es_to_en, solo aplica a translation


class AchievementUnlocked(BaseModel):
    code: str
    title: str
    description: str
    xp_reward: int


class ChallengeCompleted(BaseModel):
    code: str
    title: str
    xp_reward: int


class AnswerResult(BaseModel):
    is_correct: bool
    correct_answer: str
    xp_earned: int
    total_xp: int
    level: int
    current_streak: int
    next_review_at: str | None = None
    achievements_unlocked: list[AchievementUnlocked] = []
    challenges_completed: list[ChallengeCompleted] = []


class ChallengeProgressOut(BaseModel):
    code: str
    title: str
    description: str
    target_count: int
    progress: int
    completed: bool
    xp_reward: int


class DueWordsOut(BaseModel):
    words: list[WordOut]
    count: int
