"""
Seed de vocabulario inicial para desarrollo/demo.
Uso: python -m app.db.seed  (desde la carpeta backend, con el venv activo)
"""
from app.db.database import SessionLocal, Base, engine
from app.models.word import Word
from app import models  # noqa: F401

SAMPLE_WORDS = [
    dict(text_en="house", text_es="casa", category="home", difficulty=1,
         example_sentence_en="This is my house.", example_sentence_es="Esta es mi casa."),
    dict(text_en="water", text_es="agua", category="food", difficulty=1,
         example_sentence_en="I drink water every day.", example_sentence_es="Bebo agua todos los días."),
    dict(text_en="friend", text_es="amigo", category="people", difficulty=1,
         example_sentence_en="She is my best friend.", example_sentence_es="Ella es mi mejor amiga."),
    dict(text_en="travel", text_es="viajar", category="travel", difficulty=2,
         example_sentence_en="I love to travel.", example_sentence_es="Me encanta viajar."),
    dict(text_en="airport", text_es="aeropuerto", category="travel", difficulty=2,
         example_sentence_en="The airport is far away.", example_sentence_es="El aeropuerto está lejos."),
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Word).count() > 0:
            print("Ya hay palabras en la base de datos, no se insertó nada.")
            return
        db.bulk_insert_mappings(Word, SAMPLE_WORDS)
        db.commit()
        print(f"Se insertaron {len(SAMPLE_WORDS)} palabras.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
