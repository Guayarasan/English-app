# Imagen liviana: slim en vez de la imagen completa de Python, y
# --no-cache-dir para no arrastrar el cache de pip en la capa final.
FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2 (driver de PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# En producción ENV=production desactiva el create_all() automático
# (ver app/main.py) — las migraciones corren aparte con alembic.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
