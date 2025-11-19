# Sistema de Recomendación Inteligente

Sistema de recomendación musical basado en agentes inteligentes con aprendizaje por refuerzo.

## 🏗️ Arquitectura

El proyecto está organizado en dos componentes principales:

```
src/
├── backend/          # API REST con FastAPI (Arquitectura en capas)
│   ├── api/         # Capa de presentación (endpoints)
│   ├── services/    # Capa de lógica de negocio
│   ├── repositories/# Capa de acceso a datos
│   ├── models/      # Modelos y esquemas
│   └── core/        # Configuración y dependencias
│
└── app/             # Frontend con Flask
    ├── templates/   # Plantillas HTML
    ├── static/      # CSS y JavaScript
    └── app.py       # Aplicación Flask
```

## 📋 Requisitos Previos

- Python 3.8+
- pip
- Datos de Last.FM en `notebooks/` (*.dat files)

## 🚀 Instalación y Ejecución

### Backend (FastAPI)

```bash
# Navegar al directorio del backend
cd src/backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python main.py
```

El backend estará disponible en: `http://localhost:8000`

Documentación API: `http://localhost:8000/docs`

### Frontend (Flask)

```bash
# Navegar al directorio del frontend
cd src/app

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example .env

# Ejecutar el servidor
python app.py
```

El frontend estará disponible en: `http://localhost:5000`

## 🎯 Características del Sistema

### Backend (FastAPI)

**Arquitectura en Capas:**

1. **Capa de Presentación (API)**
   - Endpoints RESTful
   - Validación con Pydantic
   - Documentación automática con OpenAPI

2. **Capa de Servicios**
   - `agent_service.py`: Agente inteligente principal
   - `perception_service.py`: Módulo de percepción multimodal
   - `reward_service.py`: Sistema de recompensas
   - `bandit_service.py`: Algoritmo UCB Multi-Armed Bandit

3. **Capa de Repositorios**
   - `data_repository.py`: Acceso a datos de Last.FM

4. **Capa de Modelos**
   - Entidades de dominio
   - Esquemas de validación (DTOs)

### API Endpoints

- `GET /`: Health check
- `GET /api/users`: Obtener usuarios disponibles
- `GET /api/users/{user_id}/state`: Estado del usuario
- `POST /api/recommend`: Generar recomendación
- `POST /api/feedback`: Enviar feedback
- `GET /api/statistics`: Estadísticas del agente
- `GET /api/users/{user_id}/profile`: Perfil del usuario

### Frontend (Flask)

**Interfaz Web Interactiva:**

- 👤 Selección de usuarios
- 📊 Visualización del estado del usuario (engagement, diversidad, conectividad social, etc.)
- 🎵 Generación de recomendaciones personalizadas
- 💭 Sistema de feedback (positivo/neutral/negativo)
- 📈 Estadísticas en tiempo real del agente
- 👥 Perfiles de usuario con historial de interacciones

## 🧠 Capacidades del Agente Inteligente

1. **Percepción Multimodal**: Analiza señales musicales, sociales y semánticas
2. **Aprendizaje Continuo**: Mejora automáticamente con cada interacción
3. **Personalización Dinámica**: Adapta estrategias a cada usuario
4. **Balanceo Exploration/Exploitation**: Optimiza descubrimiento vs satisfacción
5. **Recompensas Multimodales**: Integra múltiples componentes de feedback

## 🎵 Estrategias de Recomendación

1. **Social Influence**: Recomendaciones basadas en amigos
2. **Semantic Coherence**: Basadas en tags musicales
3. **Exploration**: Descubrimiento de nuevo contenido
4. **Traditional CF**: Filtrado colaborativo clásico

## 📊 Métricas del Sistema

- Engagement musical
- Diversidad de escucha
- Conectividad social
- Actividad semántica
- Sofisticación general del usuario
- Recompensa promedio
- Tasa de éxito por estrategia

## 🔧 Configuración

### Backend (`backend/core/config.py`)

- Rutas de datos
- Parámetros del agente (confidence levels)
- Estrategias de recomendación

### Frontend (`app/.env`)

- URL del backend API
- Configuración de Flask

## 📝 Uso del Sistema

1. **Iniciar Backend**: El sistema cargará los datos y inicializará el agente
2. **Iniciar Frontend**: Conectarse al backend
3. **Seleccionar Usuario**: Elegir de la lista o aleatorio
4. **Ver Estado**: Analizar perfil del usuario
5. **Obtener Recomendación**: El agente selecciona la mejor estrategia
6. **Dar Feedback**: El agente aprende y se adapta
7. **Monitorear Estadísticas**: Ver evolución del sistema

## 🎨 Tecnologías Utilizadas

### Backend
- FastAPI
- Pydantic
- Pandas
- NumPy
- Scikit-learn

### Frontend
- Flask
- HTML5/CSS3
- JavaScript (Vanilla)

## 📚 Basado en

Este sistema implementa la arquitectura del notebook `SR_Sesion5.ipynb` que integra:

- Sesión 1: Modelo tradicional SVD (baseline)
- Sesión 2: Arquitectura de agente modular
- Sesión 3: Funciones de recompensa multimodales
- Sesión 4: Multi-Armed Bandits adaptativos
- Sesión 5: Agente inteligente completo

## 🤝 Contribuciones

Este es un proyecto educativo que demuestra la aplicación de técnicas de IA avanzadas en sistemas de recomendación.

## 📄 Licencia

Proyecto educativo - Sistema de Recomendación con Agentes Inteligentes

