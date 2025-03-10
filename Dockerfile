FROM python:3.11

WORKDIR /app

# Variables de entorno para mejorar el rendimiento de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Instalar dependencias del sistema necesarias para compilar paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Asegurar que pip, setuptools y wheel estén actualizados
RUN pip install --upgrade pip setuptools wheel

# Copiar y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app .

# Comando para ejecutar FastAPI con Uvicorn
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port"]
