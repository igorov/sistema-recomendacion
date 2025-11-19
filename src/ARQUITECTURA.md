# 🏗️ Arquitectura del Sistema de Recomendación Inteligente

## 📂 Estructura del Proyecto

```
src/
├── 📁 backend/                      # API REST con FastAPI
│   ├── 📁 api/                     # Capa de Presentación
│   │   └── 📁 routes/             
│   │       └── recommendations.py  # Endpoints de la API
│   │
│   ├── 📁 services/                # Capa de Lógica de Negocio
│   │   ├── agent_service.py       # Agente Inteligente Principal
│   │   ├── perception_service.py  # Módulo de Percepción Multimodal
│   │   ├── reward_service.py      # Sistema de Recompensas
│   │   └── bandit_service.py      # Algoritmo UCB Multi-Armed Bandit
│   │
│   ├── 📁 repositories/            # Capa de Acceso a Datos
│   │   └── data_repository.py     # Repositorio de datos Last.FM
│   │
│   ├── 📁 models/                  # Capa de Modelos
│   │   ├── entities.py            # Entidades de dominio
│   │   └── schemas.py             # Esquemas Pydantic (DTOs)
│   │
│   ├── 📁 core/                    # Configuración Central
│   │   ├── config.py              # Configuración de la aplicación
│   │   └── dependencies.py        # Inyección de dependencias
│   │
│   ├── main.py                     # Punto de entrada FastAPI
│   └── requirements.txt            # Dependencias Python
│
├── 📁 app/                          # Frontend con Flask
│   ├── 📁 templates/               # Plantillas HTML
│   │   └── index.html             # Interfaz principal
│   │
│   ├── 📁 static/                  # Recursos estáticos
│   │   ├── 📁 css/
│   │   │   └── style.css          # Estilos de la aplicación
│   │   └── 📁 js/
│   │       └── main.js            # Lógica del cliente
│   │
│   ├── app.py                      # Aplicación Flask
│   └── requirements.txt            # Dependencias Python
│
├── 📄 README.md                     # Documentación principal
├── 📄 QUICKSTART.md                 # Guía de inicio rápido
├── 📄 ARQUITECTURA.md               # Este archivo
├── 🔧 start_backend.sh              # Script para iniciar backend
├── 🔧 start_frontend.sh             # Script para iniciar frontend
├── 🔧 start_all.sh                  # Script para iniciar todo
└── 🧪 test_system.py                # Script de prueba del sistema
```

## 🔄 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                      USUARIO (Navegador)                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (Flask) - Puerto 5000              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Templates HTML                                     │   │
│  │  • CSS Styling                                        │   │
│  │  • JavaScript Client Logic                           │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI) - Puerto 8000                 │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │        CAPA DE PRESENTACIÓN (API Routes)           │     │
│  │  • /api/users                                      │     │
│  │  • /api/recommend                                  │     │
│  │  • /api/feedback                                   │     │
│  │  • /api/statistics                                 │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│  ┌──────────────────▼─────────────────────────────────┐     │
│  │       CAPA DE LÓGICA DE NEGOCIO (Services)         │     │
│  │                                                     │     │
│  │  ┌───────────────────────────────────────────┐     │     │
│  │  │  IntelligentRecommendationAgent           │     │     │
│  │  │  • recommend()                            │     │     │
│  │  │  • learn_from_feedback()                  │     │     │
│  │  └───────────────┬───────────────────────────┘     │     │
│  │                  │                                  │     │
│  │  ┌───────────────▼───────────┐  ┌──────────────┐   │     │
│  │  │  PerceptionModule         │  │  UCBBandit   │   │     │
│  │  │  • get_user_state()       │  │  • select()  │   │     │
│  │  └───────────────────────────┘  └──────────────┘   │     │
│  │                                                     │     │
│  │  ┌────────────────────────────────────────┐        │     │
│  │  │  MultimodalRewardSystem                │        │     │
│  │  │  • calculate_reward()                  │        │     │
│  │  └────────────────────────────────────────┘        │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│  ┌──────────────────▼─────────────────────────────────┐     │
│  │     CAPA DE ACCESO A DATOS (Repositories)          │     │
│  │  • DataRepository                                  │     │
│  │  • Load datasets                                   │     │
│  │  • Query data                                      │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Last.FM Data │
                    │  (*.dat files)│
                    └───────────────┘
```

## 🧠 Arquitectura del Agente Inteligente

```
┌──────────────────────────────────────────────────────────────┐
│            INTELLIGENT RECOMMENDATION AGENT                   │
│                                                               │
│  ┌────────────────────────────────────────────────────┐      │
│  │  PASO 1: PERCEPCIÓN                                │      │
│  │  ───────────────────────────────────────────────   │      │
│  │  • Analiza estado del usuario                      │      │
│  │  • Señales musicales (engagement, diversidad)      │      │
│  │  • Señales sociales (amigos, alineación)           │      │
│  │  • Señales semánticas (tags, actividad)            │      │
│  └────────────────────┬───────────────────────────────┘      │
│                       │                                       │
│  ┌────────────────────▼───────────────────────────────┐      │
│  │  PASO 2: RAZONAMIENTO                              │      │
│  │  ───────────────────────────────────────────────   │      │
│  │  • UCB Multi-Armed Bandit                          │      │
│  │  • Selecciona estrategia óptima                    │      │
│  │  • Balance exploration/exploitation                │      │
│  │  • Personalización por usuario                     │      │
│  └────────────────────┬───────────────────────────────┘      │
│                       │                                       │
│  ┌────────────────────▼───────────────────────────────┐      │
│  │  PASO 3: ACCIÓN                                    │      │
│  │  ───────────────────────────────────────────────   │      │
│  │  • Genera recomendación específica                 │      │
│  │  • Estrategias:                                    │      │
│  │    - Social Influence                              │      │
│  │    - Semantic Coherence                            │      │
│  │    - Exploration                                   │      │
│  │    - Traditional CF                                │      │
│  └────────────────────┬───────────────────────────────┘      │
│                       │                                       │
│  ┌────────────────────▼───────────────────────────────┐      │
│  │  PASO 4: APRENDIZAJE                               │      │
│  │  ───────────────────────────────────────────────   │      │
│  │  • Recibe feedback del usuario                     │      │
│  │  • Calcula recompensa multimodal                   │      │
│  │  • Actualiza agente bandit                         │      │
│  │  • Mejora continua adaptativa                      │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## 🎯 Patrones de Diseño Implementados

### 1. **Arquitectura en Capas (Layered Architecture)**
- **Presentación**: API endpoints (FastAPI routes)
- **Negocio**: Services con lógica del agente
- **Datos**: Repositories para acceso a datos
- **Modelos**: Entities y Schemas

### 2. **Dependency Injection**
- Gestión centralizada de dependencias en `core/dependencies.py`
- Singleton pattern para servicios compartidos
- Facilita testing y mantenimiento

### 3. **Repository Pattern**
- Abstracción del acceso a datos
- `DataRepository` encapsula toda la lógica de datos
- Facilita cambio de fuente de datos

### 4. **Strategy Pattern**
- Múltiples estrategias de recomendación
- Selección dinámica basada en contexto
- Fácil extensión con nuevas estrategias

### 5. **Observer Pattern** (Implícito)
- Sistema de feedback y aprendizaje
- El agente observa y reacciona al comportamiento del usuario

## 🔐 Separación de Responsabilidades

### Backend (FastAPI)
**Responsabilidades:**
- Lógica de negocio del agente inteligente
- Procesamiento de datos
- Aprendizaje y adaptación
- Almacenamiento del estado
- API REST documentada

### Frontend (Flask)
**Responsabilidades:**
- Presentación de datos
- Interacción con usuario
- Visualización de estadísticas
- Experiencia de usuario
- Proxy hacia backend API

## 📊 Flujo de una Recomendación

```
1. Usuario solicita recomendación
        │
        ▼
2. Frontend envía POST /api/recommend
        │
        ▼
3. API Route valida request
        │
        ▼
4. AgentService.recommend()
        │
        ├──► PerceptionModule: Analiza usuario
        │
        ├──► UCBBandit: Selecciona estrategia
        │
        └──► Genera recomendación específica
        │
        ▼
5. Respuesta al frontend
        │
        ▼
6. Usuario ve recomendación
        │
        ▼
7. Usuario da feedback
        │
        ▼
8. Frontend envía POST /api/feedback
        │
        ▼
9. AgentService.learn_from_feedback()
        │
        ├──► RewardSystem: Calcula recompensa
        │
        └──► UCBBandit: Actualiza estadísticas
        │
        ▼
10. Agente aprende y se adapta
```

## 🚀 Tecnologías y Librerías

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos
- **Pandas**: Manipulación de datos
- **NumPy**: Computación numérica
- **Scikit-learn**: Machine learning

### Frontend
- **Flask**: Framework web Python
- **HTML5/CSS3**: Interfaz moderna
- **JavaScript**: Interactividad del cliente
- **Fetch API**: Comunicación con backend

## 📈 Escalabilidad y Extensibilidad

### Fácil de Extender
1. **Nuevas estrategias**: Agregar en `agent_service.py`
2. **Nuevas métricas**: Modificar `perception_service.py`
3. **Nuevos endpoints**: Agregar en `api/routes/`
4. **Nuevas fuentes de datos**: Crear nuevo repository

### Preparado para Producción
- Arquitectura modular y mantenible
- Logging integrado
- Manejo de errores robusto
- Validación de datos estricta
- Documentación automática (OpenAPI)
- Fácil containerización (Docker)

## 🔄 Ciclo de Mejora Continua

El sistema implementa un ciclo de mejora continua:

1. **Recopilación**: Datos de interacciones
2. **Análisis**: Estado y preferencias del usuario
3. **Decisión**: Selección de estrategia óptima
4. **Acción**: Generación de recomendación
5. **Feedback**: Evaluación del usuario
6. **Aprendizaje**: Actualización del modelo
7. **Adaptación**: Mejora de futuras recomendaciones

Este ciclo se repite continuamente, permitiendo que el agente evolucione y mejore con cada interacción.

