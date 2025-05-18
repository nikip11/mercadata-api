# MercaData API 📊

![Deploy on Local Cloud](https://github.com/YOUR_USERNAME/mercadata-api/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.113+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Descripción

MercaData API es un servicio backend para procesar, analizar y almacenar datos de tickets de compra de Mercadona. La API extrae información de los PDFs de tickets de compra para proporcionar análisis de gastos, tendencias de precios y gestión de inventario.

## ✨ Características

- 📃 Extracción automática de datos desde PDFs de tickets
- 💾 Almacenamiento estructurado en MongoDB
- 🔍 Búsqueda y filtrado avanzado de gastos
- 📊 Análisis de tendencias de precios y patrones de compra
- 🔒 API RESTful segura con FastAPI
- 🐳 Completamente dockerizado para fácil despliegue

## 🛠️ Tecnologías

- **Backend**: FastAPI
- **Base de datos**: MongoDB
- **Procesamiento PDF**: PyPDF2
- **Contenedores**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## 📋 Requisitos previos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)
- MongoDB (gestionado mediante Docker)

## 🚀 Instalación y Despliegue

### Usando Docker (recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/YOUR_USERNAME/mercadata-api.git
cd mercadata-api

# Crear archivo .env con las variables necesarias
echo "DB_URL_MERCADATA=mongodb://mongodb/mercadata" > .env

# Iniciar servicios con Docker Compose
docker-compose up -d
```

### Desarrollo local

```bash
# Clonar el repositorio
git clone https://github.com/YOUR_USERNAME/mercadata-api.git
cd mercadata-api

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DB_URL_MERCADATA=mongodb://localhost/mercadata

# Iniciar la API
cd app
uvicorn main:app --reload
```

## 📚 API Endpoints

La documentación de la API está disponible en:

- Swagger UI: http://localhost:9999/docs
- ReDoc: http://localhost:9999/redoc

### Principales endpoints:

- `GET /invoices`: Lista todos los tickets
- `POST /invoices/upload`: Sube y procesa un nuevo ticket
- `GET /invoices/{id}`: Obtiene detalles de un ticket específico
- `GET /stats`: Obtiene estadísticas generales de gastos

## 🧪 Pruebas

```bash
# Ejecutar tests
pytest
```

## 🔄 CI/CD

El proyecto utiliza GitHub Actions para CI/CD. Cada push a la rama master desencadena:

1. Construcción y pruebas del código
2. Construcción de la imagen Docker
3. Despliegue automático en el servidor

## 📂 Estructura del proyecto

```
mercadata-api/
│
├── app/                    # Código fuente de la API
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── database.py        # Configuración de la base de datos
│   ├── models/            # Modelos y schemas
│   └── utils/             # Utilidades (procesamiento PDF, etc)
│
├── docker-compose.yaml     # Configuración Docker para desarrollo
├── docker-compose.prod.yaml # Configuración Docker para producción
├── Dockerfile              # Definición para construir la imagen
└── requirements.txt        # Dependencias Python
```

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, siente libre de:

1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## 📞 Contacto

Para cualquier consulta, por favor abre un issue en el repositorio o contacta con el equipo de desarrollo.

---

⭐️ **MercaData API** - Análisis inteligente de gastos en Mercadona ⭐️