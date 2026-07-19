"""
Motor y sesión de SQLAlchemy.
`connect_args` con check_same_thread solo aplica a SQLite; en Postgres
se ignora automáticamente al no pasarse (ver get_engine_kwargs).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


def get_engine_kwargs():
    if settings.DATABASE_URL.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {}


engine = create_engine(settings.DATABASE_URL, **get_engine_kwargs())
# expire_on_commit=False: varios endpoints (ej. POST /api/review/answer)
# siguen leyendo atributos y relaciones de los objetos justo después de
# hacer commit, para armar la respuesta. Con el comportamiento por
# defecto (expire_on_commit=True) esos accesos disparan un SELECT nuevo
# por cada atributo expirado; desactivarlo evita esas queries extra sin
# perder consistencia, porque igual llamamos a refresh() donde
# necesitamos ver cambios hechos fuera de la sesión.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesión y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
