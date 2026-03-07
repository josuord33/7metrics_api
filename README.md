# 7metrics Handball Statistics API 🤾‍♂️

API REST de alto rendimiento diseñada para la gestión y análisis estadístico en tiempo real de partidos de balonmano. Construida con **FastAPI**, **MongoDB Atlas** y siguiendo una **Arquitectura Hexagonal (Puertos y Adaptadores)** para máxima escalabilidad y testabilidad.

## 🚀 Características Principales

- **Gestión de Partidos**: Control total sobre el estado del partido (Setup, In Progress, Paused, Finished).
- **Registro de Eventos**: Captura de acciones detalladas (Goles, Paradas, Pérdidas, Exclusiones, etc.).
- **Actualización Automática**: El marcador se actualiza en tiempo real basándose en los eventos registrados.
- **Estadísticas Avanzadas**: Cálculos de eficiencia, efectividad de porteros y control de posesión.
- **Exportación de Datos**: Generación dinámica de reportes en formato CSV.
- **Arquitectura Hexagonal**: Desacoplamiento total entre la lógica de negocio y la infraestructura.

## 🛠️ Tecnologías

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13+)
- **Base de Datos**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- **ODM**: [Beanie](https://beanie-odm.dev/) (basado en Motor y Pydantic v2)
- **Testing**: [Pytest](https://docs.pytest.org/) con `pytest-asyncio`
- **Contenedores**: Docker Ready

---

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/josuord33/7metrics_api.git
cd 7metrics_api
```

### 2. Configurar el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto basándote en el archivo `.env.example`:

```env
MONGODB_URL=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=handball_statistics
API_TITLE=7metrics Handball Statistics API
API_VERSION=1.0.0
DEBUG=true
```

---

## 🚀 Ejecución

Arranca el servidor de desarrollo con recarga automática:

```bash
./venv/bin/uvicorn src.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

### 📖 Documentación Interactiva
FastAPI genera automáticamente documentación detallada:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue un diseño de **Arquitectura Hexagonal**:

```text
src/
├── core/                # Capa de Dominio (Pura, sin dependencias externas)
│   ├── domain/          # Entidades (Match, Player, Event) y Enums
│   └── ports/           # Interfaces de repositorios (Protocolos)
├── application/         # Capa de Aplicación (Lógica de Negocio)
│   └── use_cases/       # Casos de uso (Orquestación de la lógica)
├── infrastructure/      # Capa de Infraestructura (Implementaciones externas)
│   ├── persistence/     # MongoDB Repositories y Modelos Beanie
│   ├── api/             # Routers de FastAPI y Controladores
│   └── config/          # Configuración de Settings/Pydantic
└── main.py              # Punto de entrada (Composición de la app)
```

---

## 🧪 Testing

Para ejecutar la suite de pruebas (Unitarias e Integración):

```bash
python3 -m pytest tests -v
```

Las pruebas de integración utilizan una base de datos de prueba independiente (`test_handball_statistics`) para garantizar la integridad de los datos de producción.

---

## 📊 Endpoints Principales

- **Partidos**: `GET /matches`, `POST /matches`, `POST /matches/{id}/start`
- **Jugadores**: `POST /matches/{id}/players/bulk`, `GET /matches/{match_id}/players`
- **Eventos**: `POST /events`, `GET /events/{match_id}`, `DELETE /events/last/{match_id}`
- **Estadísticas**: `GET /matches/{id}/statistics`, `GET /matches/{id}/statistics/export/csv`

---

## 📝 Licencia
Desarrollado para 7metrics. Todos los derechos reservados.
