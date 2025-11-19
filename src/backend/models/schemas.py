"""Esquemas de datos para la API (DTOs)"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class UserStateResponse(BaseModel):
    """Respuesta con el estado del usuario"""
    user_id: int
    music_engagement: float = Field(ge=0, le=1)
    music_diversity: float = Field(ge=0, le=1)
    music_intensity: float = Field(ge=0, le=1)
    social_connectivity: float = Field(ge=0, le=1)
    social_alignment: float = Field(ge=0, le=1)
    semantic_activity: float = Field(ge=0, le=1)
    semantic_diversity: float = Field(ge=0, le=1)
    overall_sophistication: float = Field(ge=0, le=1)


class RecommendationRequest(BaseModel):
    """Petición de recomendación"""
    user_id: int = Field(gt=0, description="ID del usuario")
    context: Optional[Dict] = Field(default=None, description="Contexto adicional")


class RecommendationResponse(BaseModel):
    """Respuesta con recomendación"""
    artist_id: int
    artist_name: str
    strategy: str
    reason: str
    confidence: float = Field(ge=0, le=1)
    timestamp: datetime
    decision_info: Dict


class FeedbackRequest(BaseModel):
    """Petición de feedback del usuario"""
    user_id: int = Field(gt=0)
    artist_id: int
    feedback_type: str = Field(
        description="Tipo de feedback: 'explicit_rating', 'implicit_behavior', 'positive', 'neutral', 'negative'"
    )
    feedback_value: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Valor del feedback (0-1) para tipos cuantitativos"
    )


class FeedbackResponse(BaseModel):
    """Respuesta del procesamiento de feedback"""
    user_id: int
    outcome: str
    reward: float
    reward_components: Dict
    strategy: str
    message: str


class AgentStatisticsResponse(BaseModel):
    """Respuesta con estadísticas del agente"""
    total_users: int
    total_recommendations: int
    average_reward: float
    active_sessions: int
    strategy_performance: Dict
    top_users: List[Dict]


class UserProfileResponse(BaseModel):
    """Respuesta con perfil de usuario"""
    user_id: int
    total_interactions: int
    preferred_strategy: str
    agent_confidence: float
    user_sophistication: float
    interaction_history: List[Dict]


class HealthResponse(BaseModel):
    """Respuesta de salud del servicio"""
    status: str
    timestamp: datetime
    version: str
    users_loaded: int
    artists_loaded: int


class AvailableUsersResponse(BaseModel):
    """Respuesta con usuarios disponibles"""
    total_users: int
    users: List[int]
    sample_user: Optional[int] = None

