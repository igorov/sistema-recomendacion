"""Inyección de dependencias para FastAPI"""
from functools import lru_cache
import logging

from core.config import settings
from repositories.data_repository import DataRepository
from services.perception_service import PerceptionModule
from services.reward_service import MultimodalRewardSystem
from services.agent_service import IntelligentRecommendationAgent

logger = logging.getLogger(__name__)

# Instancias globales (singleton pattern)
_data_repository = None
_perception_module = None
_reward_system = None
_agent_service = None


def get_data_repository() -> DataRepository:
    """Obtener instancia del repositorio de datos"""
    global _data_repository
    if _data_repository is None:
        logger.info("Inicializando DataRepository...")
        _data_repository = DataRepository(settings.DATA_PATH)
    return _data_repository


def get_perception_module() -> PerceptionModule:
    """Obtener instancia del módulo de percepción"""
    global _perception_module
    if _perception_module is None:
        logger.info("Inicializando PerceptionModule...")
        data_repo = get_data_repository()
        _perception_module = PerceptionModule(
            data_repo.user_artists,
            data_repo.user_friends,
            data_repo.user_tagged,
            data_repo.artists,
            data_repo.tags
        )
    return _perception_module


def get_reward_system() -> MultimodalRewardSystem:
    """Obtener instancia del sistema de recompensas"""
    global _reward_system
    if _reward_system is None:
        logger.info("Inicializando MultimodalRewardSystem...")
        perception = get_perception_module()
        _reward_system = MultimodalRewardSystem(perception)
    return _reward_system


def get_agent_service() -> IntelligentRecommendationAgent:
    """Obtener instancia del agente inteligente"""
    global _agent_service
    if _agent_service is None:
        logger.info("Inicializando IntelligentRecommendationAgent...")
        perception = get_perception_module()
        reward_system = get_reward_system()
        data_repo = get_data_repository()
        
        _agent_service = IntelligentRecommendationAgent(
            perception_module=perception,
            reward_system=reward_system,
            data_repository=data_repo,
            recommendation_strategies=settings.RECOMMENDATION_STRATEGIES,
            confidence_level_new_user=settings.CONFIDENCE_LEVEL_NEW_USER,
            confidence_level_experienced_user=settings.CONFIDENCE_LEVEL_EXPERIENCED_USER
        )
        logger.info("✅ Sistema de recomendación inicializado completamente")
    
    return _agent_service

