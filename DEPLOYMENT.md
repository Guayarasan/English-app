# Guía de despliegue

## Antes de desplegar: generar la primera migración

El proyecto usa Alembic para versionar el esquema en producción (en desarrollo,
`create_all()` crea las tablas automáticamente en SQLite, pero eso no corre
en producción). Generar la migración inicial localmente, con las
dependencias instaladas:

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "esquema inicial"
```

Esto crea un archivo en `backend/migrations/versions/`. Commitealo — es lo
que corre `alembic upgrade head` en producción antes de levantar la API.

---

## Opción A — Todo en un VPS con Docker (más simple y barato)

Sirve en cualquier VPS con Docker (DigitalOcean, Hetzner, un EC2 free tier, etc.)

1. Cloná el repo en el servidor.
2. `cp .env.example .env` y completá `SECRET_KEY` (un string largo y
   aleatorio) y las credenciales de Postgres.
3. Ajustá `VITE_API_URL` y `FRONTEND_ORIGIN` al dominio/IP real del servidor.
4. `docker compose up --build -d`

Eso levanta Postgres, corre las migraciones, y sirve backend (puerto 8000)
y frontend (puerto 8080). Para HTTPS, poné un reverse proxy delante
(Caddy o nginx con Let's Encrypt) apuntando a esos dos puertos.

---

## Opción B — Servicios gestionados con capa gratuita

Backend en **Render** o **Railway**, frontend en **Vercel** o **Netlify**,
base de datos en el Postgres gestionado que ofrezca el mismo proveedor del
backend.

### Backend (Render, como ejemplo)
1. New → Web Service → conectar el repo, root directory `backend/`.
2. Build command: `pip install -r requirements.txt && alembic upgrade head`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Variables de entorno: `ENV=production`, `DATABASE_URL` (la que da el
   Postgres gestionado), `SECRET_KEY`, `FRONTEND_ORIGIN` (la URL de Vercel,
   se completa después del paso siguiente).

### Frontend (Vercel, como ejemplo)
1. New Project → conectar el repo, root directory `frontend/`.
2. Framework preset: Vite.
3. Variable de entorno: `VITE_API_URL` = URL pública del backend de Render.
4. Deploy. Volver al backend y actualizar `FRONTEND_ORIGIN` con la URL que
   asignó Vercel (para que CORS no bloquee las requests).

---

## Checklist antes de ir a producción

- [ ] `SECRET_KEY` es un valor random largo, no el placeholder del `.env.example`.
- [ ] `DATABASE_URL` apunta a PostgreSQL, no a SQLite.
- [ ] `ENV=production` (desactiva el `create_all()` automático).
- [ ] Migración inicial de Alembic generada y commiteada.
- [ ] `FRONTEND_ORIGIN` coincide exactamente con la URL pública del frontend (con https, sin barra final).
- [ ] Correr `python -m app.db.seed` una vez contra la base de producción, o cargar vocabulario propio.
