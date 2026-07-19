from pydantic import BaseModel


class StatsSummary(BaseModel):
    total_attempts: int
    correct_attempts: int
    accuracy: float
    words_learned: int
    words_in_progress: int


class DailyStat(BaseModel):
    date: str
    attempts: int
    accuracy: float


class CategoryStat(BaseModel):
    category: str
    attempts: int
    accuracy: float


class HardWord(BaseModel):
    text_en: str
    text_es: str
    fail_count: int
    success_count: int
