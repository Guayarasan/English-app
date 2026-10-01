from pydantic import BaseModel, ConfigDict, Field


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
    text_en: str = Field(min_length=1)
    text_es: str = Field(min_length=1)
    category: str | None = None
    difficulty: int = Field(default=1, ge=1, le=5)
    example_sentence_en: str | None = None
    example_sentence_es: str | None = None
