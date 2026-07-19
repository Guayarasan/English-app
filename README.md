# Passport — Plataforma para aprender inglés

Web app de aprendizaje de inglés con identidad propia ("pasaporte de idioma"): XP, rachas, logros, desafíos diarios y un motor de repaso espaciado que prioriza las palabras que más fallas.

## Stack

- **Backend**: FastAPI + SQLAlchemy + Alembic. SQLite en desarrollo, PostgreSQL en producción.
- **Frontend**: React (Vite) + TailwindCSS + Framer Motion + Recharts.
- **Auth**: JWT (access + refresh token).

## Estructura

```
english-app/
├── backend/     # API FastAPI
├── frontend/    # SPA React
├── docker-compose.yml
└── .env.example
```

Ver `backend/app/` y `frontend/src/` para el detalle de cada módulo — cada archivo tiene un docstring explicando su responsabilidad.

## Correr en desarrollo (sin Docker)

**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.db.seed      # vocabulario de ejemplo
uvicorn app.main:app --reload
```
API en `http://localhost:8000`, docs interactivas en `/docs`.

**Frontend**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
App en `http://localhost:5173`.

## Correr todo con Docker

```bash
cp .env.example .env   # y editar SECRET_KEY, contraseñas, etc.
docker compose up --build
```
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`

Ver `DEPLOYMENT.md` para desplegar en producción real (VPS o servicios gestionados).

## Módulos principales

| Área | Ubicación | Qué hace |
|---|---|---|
| Auth | `backend/app/api/auth.py` | Registro, login, JWT |
| Repaso inteligente (SRS) | `backend/app/services/srs_service.py` | Algoritmo tipo SM-2, prioriza palabras falladas |
| Ejercicios | `backend/app/services/exercise_service.py` | Validación server-side de traducción/completar/escritura |
| Gamificación | `backend/app/services/gamification_service.py` | XP, nivel, rachas |
| Logros y desafíos | `backend/app/services/achievement_service.py`, `daily_challenge_service.py` | Desbloqueo automático tras cada respuesta |
| Estadísticas | `backend/app/services/stats_service.py` | Historial, precisión por categoría, palabras difíciles |
