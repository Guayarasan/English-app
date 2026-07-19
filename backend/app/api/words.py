"""
Endpoints de vocabulario.

Nota: la selección "inteligente" de qué palabras mostrar para repaso
(UserWord.next_review_at, fail_count) vive en app/api/review.py, que se
construye en la Fase 3. Este módulo solo expone el catálogo crudo:
listar y crear palabras.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.word import Word
from app.schemas.word import WordOut, WordCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/words", tags=["words"])


@router.get("", response_model=list[WordOut])
def list_words(
    category: str | None = Query(default=None),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Word)
    if category:
        query = query.filter(Word.category == category)
    return query.limit(limit).all()


@router.post("", response_model=WordOut, status_code=201)
def create_word(
    word_in: WordCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    word = Word(**word_in.model_dump())
    db.add(word)
    db.commit()
    db.refresh(word)
    return word
