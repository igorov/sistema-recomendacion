"""Aplicación principal de FastAPI"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from core.config import settings
from core.dependencies import get_data_repository, get_agent_service
from api.routes import recommendations
from models.schemas import HealthResponse

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(recommendations.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    logger.info("🚀 Iniciando Sistema de Recomendación Inteligente...")
    logger.info(f"   Versión: {settings.API_VERSION}")
    logger.info(f"   Data Path: {settings.DATA_PATH}")
    
    # Inicializar servicios
    try:
        data_repo = get_data_repository()
        agent = get_agent_service()
        logger.info("✅ Todos los servicios inicializados correctamente")
    except Exception as e:
        logger.error(f"❌ Error inicializando servicios: {e}")
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint raíz - Health check"""
    data_repo = get_data_repository()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.API_VERSION,
        users_loaded=len(data_repo.user_artists['userID'].unique()),
        artists_loaded=len(data_repo.artists)
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    data_repo = get_data_repository()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.API_VERSION,
        users_loaded=len(data_repo.user_artists['userID'].unique()),
        artists_loaded=len(data_repo.artists)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

