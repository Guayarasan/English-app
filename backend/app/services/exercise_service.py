"""
Validación de respuestas en el servidor (no se confía en el cliente,
salvo para 'flashcard' que es autoevaluación explícita del usuario).

check_writing es deliberadamente permisivo: sin un motor de gramática
no podemos validar una oración en inglés con certeza, así que solo
verificamos que la palabra objetivo aparezca y que haya una oración
mínimamente real (3+ palabras). Es preferible un falso positivo
ocasional a frustrar a alguien que escribió una oración correcta que
no calzó con un regex estricto.
"""
import re

from app.models.word import Word


def _normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text)


def check_translation(word: Word, user_answer: str, direction: str) -> bool:
    if not user_answer:
        return False
    target = word.text_es if direction == "en_to_es" else word.text_en
    return _normalize(user_answer) == _normalize(target)


def check_fill_blank(word: Word, user_answer: str) -> bool:
    if not user_answer:
        return False
    return _normalize(user_answer) == _normalize(word.text_en)


def check_writing(word: Word, user_sentence: str) -> bool:
    if not user_sentence or len(user_sentence.strip().split()) < 3:
        return False
    return _normalize(word.text_en) in _normalize(user_sentence)


def get_correct_answer(word: Word, exercise_type: str, direction: str | None) -> str:
    if exercise_type == "translation":
        return word.text_es if direction == "en_to_es" else word.text_en
    return word.text_en
