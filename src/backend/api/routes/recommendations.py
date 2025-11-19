"""Rutas de la API para el sistema de recomendación"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import logging

from models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    FeedbackRequest,
    FeedbackResponse,
    AgentStatisticsResponse,
    UserProfileResponse,
    UserStateResponse,
    AvailableUsersResponse
)
from core.dependencies import get_agent_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/users", response_model=AvailableUsersResponse)
async def get_available_users(limit: int = 100, agent_service = Depends(get_agent_service)):
    """Obtener lista de usuarios disponibles"""
    try:
        users = agent_service.data_repository.get_available_users(limit=limit)
        return AvailableUsersResponse(
            total_users=len(users),
            users=users,
            sample_user=users[0] if users else None
        )
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/state", response_model=UserStateResponse)
async def get_user_state(user_id: int, agent_service = Depends(get_agent_service)):
    """Obtener estado actual de un usuario"""
    try:
        if not agent_service.data_repository.get_user_exists(user_id):
            raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
        
        user_state = agent_service.perception.get_user_state(user_id)
        return UserStateResponse(**user_state)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo estado del usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest, agent_service = Depends(get_agent_service)):
    """Obtener recomendación para un usuario"""
    try:
        if not agent_service.data_repository.get_user_exists(request.user_id):
            raise HTTPException(
                status_code=404,
                detail=f"Usuario {request.user_id} no encontrado"
            )
        
        # Generar recomendación
        recommendation, decision_info = agent_service.recommend(
            request.user_id,
            request.context
        )
        
        # Preparar respuesta
        return RecommendationResponse(
            artist_id=recommendation.artist_id,
            artist_name=recommendation.artist_name,
            strategy=recommendation.strategy,
            reason=recommendation.reason,
            confidence=recommendation.confidence,
            timestamp=recommendation.timestamp,
            decision_info={
                'action_type': decision_info.action_type,
                'agent_confidence': decision_info.agent_confidence,
                'user_sophistication': decision_info.user_state['overall_sophistication']
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando recomendación: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest, agent_service = Depends(get_agent_service)):
    """Enviar feedback sobre una recomendación"""
    try:
        if not agent_service.data_repository.get_user_exists(request.user_id):
            raise HTTPException(
                status_code=404,
                detail=f"Usuario {request.user_id} no encontrado"
            )
        
        # Crear objeto de recomendación para el feedback
        from models.entities import Recommendation
        from datetime import datetime
        
        # Buscar la última recomendación para este usuario/artista
        recommendation = None
        if request.user_id in agent_service.interaction_memory:
            recent_interactions = agent_service.interaction_memory[request.user_id]
            for interaction in reversed(recent_interactions):
                if interaction['recommendation'].artist_id == request.artist_id:
                    recommendation = interaction['recommendation']
                    break
        
        # Si no se encuentra en el historial, crear una con estrategia por defecto válida
        if recommendation is None:
            recommendation = Recommendation(
                artist_id=request.artist_id,
                artist_name=agent_service.data_repository.get_artist_name(request.artist_id),
                strategy="Traditional CF",  # Estrategia por defecto válida
                reason="Feedback submission",
                confidence=0.5,
                timestamp=datetime.now()
            )
        
        # Procesar feedback
        learning_info = agent_service.learn_from_feedback(
            request.user_id,
            recommendation,
            request.feedback_type,
            request.feedback_value
        )
        
        return FeedbackResponse(
            user_id=request.user_id,
            outcome=learning_info.outcome,
            reward=learning_info.reward,
            reward_components=learning_info.reward_components,
            strategy=learning_info.strategy,
            message=f"Feedback procesado exitosamente. Recompensa: {learning_info.reward:.3f}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics", response_model=AgentStatisticsResponse)
async def get_statistics(agent_service = Depends(get_agent_service)):
    """Obtener estadísticas del agente"""
    try:
        stats = agent_service.get_agent_statistics()
        
        # Preparar top usuarios
        top_users = []
        sorted_users = sorted(
            stats.user_profiles.items(),
            key=lambda x: x[1]['total_interactions'],
            reverse=True
        )[:10]
        
        for user_id, profile in sorted_users:
            top_users.append({
                'user_id': user_id,
                **profile
            })
        
        return AgentStatisticsResponse(
            total_users=stats.total_users,
            total_recommendations=stats.total_recommendations,
            average_reward=stats.average_reward,
            active_sessions=stats.active_sessions,
            strategy_performance=stats.strategy_performance,
            top_users=top_users
        )
    
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(user_id: int, agent_service = Depends(get_agent_service)):
    """Obtener perfil detallado de un usuario"""
    try:
        profile = agent_service.get_user_profile(user_id)
        
        if profile is None:
            # Usuario existe pero no ha interactuado con el agente
            if agent_service.data_repository.get_user_exists(user_id):
                user_state = agent_service.perception.get_user_state(user_id)
                return UserProfileResponse(
                    user_id=user_id,
                    total_interactions=0,
                    preferred_strategy="None",
                    agent_confidence=0.0,
                    user_sophistication=user_state['overall_sophistication'],
                    interaction_history=[]
                )
            else:
                raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
        
        # Preparar historial de interacciones
        interaction_history = []
        for interaction in profile['interaction_history']:
            rec = interaction['recommendation']
            learning = interaction['learning']
            interaction_history.append({
                'timestamp': rec.timestamp.isoformat(),
                'artist_id': rec.artist_id,
                'artist_name': rec.artist_name,
                'strategy': rec.strategy,
                'reward': learning.reward,
                'outcome': learning.outcome
            })
        
        return UserProfileResponse(
            user_id=profile['user_id'],
            total_interactions=profile['total_interactions'],
            preferred_strategy=profile['preferred_strategy'],
            agent_confidence=profile['agent_confidence'],
            user_sophistication=profile['user_sophistication'],
            interaction_history=interaction_history
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo perfil del usuario {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

