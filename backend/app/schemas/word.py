from pydantic import BaseModel, ConfigDict


class WordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text_en: str
    text_es: str
    category: str | None = None
    difficulty: int
    example_sentence_en: str | None = None
    example_sentence_es: str | None = None
    audio_url: str | None = None


class WordCreate(BaseModel):
    text_en: str
    text_es: str
    category: str | None = None
    difficulty: int = 1
    example_sentence_en: str | None = None
    example_sentence_es: str | None = None
