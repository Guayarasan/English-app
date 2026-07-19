"""
Punto de entrada de la API.

Nota sobre esquema/migraciones:
- En desarrollo, create_all() crea las tablas directo en SQLite (rápido,
  sin pasos manuales).
- En producción, el esquema lo crean las migraciones de Alembic
  (`alembic upgrade head`, ver docker-compose.yml), por eso create_all()
  solo corre si ENV == "development".
- El sembrado de catálogos (logros y desafíos diarios) es distinto:
  siempre corre al arrancar, en cualquier ENV, porque es idempotente
  (ensure_catalog_seeded no duplica filas) y las migraciones de Alembic
  solo crean la tabla vacía, no sus datos base.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine, SessionLocal
from app import models  # noqa: F401  (necesario para registrar los modelos)
from app.api import auth, words, review, achievements, challenges, stats
from app.services import achievement_service, daily_challenge_service

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(words.router)
app.include_router(review.router)
app.include_router(achievements.router)
app.include_router(challenges.router)
app.include_router(stats.router)

if settings.ENV == "development":
    Base.metadata.create_all(bind=engine)

_db = SessionLocal()
try:
    achievement_service.ensure_catalog_seeded(_db)
    daily_challenge_service.ensure_catalog_seeded(_db)
finally:
    _db.close()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
