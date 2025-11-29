"""Entidades de dominio del sistema de recomendación"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class UserState:
    """Estado completo de un usuario"""
    user_id: int
    music_engagement: float
    music_diversity: float
    music_intensity: float
    social_connectivity: float
    social_alignment: float
    semantic_activity: float
    semantic_diversity: float
    overall_sophistication: float


@dataclass
class Recommendation:
    """Recomendación generada por el agente"""
    artist_id: int
    artist_name: str
    strategy: str
    reason: str
    confidence: float
    timestamp: Optional[datetime] = None


@dataclass
class DecisionInfo:
    """Información sobre la decisión del agente"""
    timestamp: datetime
    user_id: int
    strategy: str
    action_type: str
    user_state: Dict
    recommendation: Recommendation
    agent_confidence: float


@dataclass
class LearningInfo:
    """Información sobre el aprendizaje del agente"""
    timestamp: datetime
    user_id: int
    feedback_type: str
    feedback_value: Optional[float]
    outcome: str
    reward: float
    reward_components: Dict
    strategy: str


@dataclass
class AgentStatistics:
    """Estadísticas del agente"""
    total_users: int
    total_recommendations: int
    average_reward: float
    active_sessions: int
    strategy_performance: Dict
    user_profiles: Dict

