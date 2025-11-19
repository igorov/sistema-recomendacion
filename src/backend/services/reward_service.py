"""Servicio de Recompensas - Sistema de recompensas multimodales"""
import numpy as np
from typing import Dict, Tuple
import logging

from services.perception_service import PerceptionModule

logger = logging.getLogger(__name__)


class MultimodalRewardSystem:
    """Sistema de recompensas multimodales para el agente"""
    
    def __init__(self, perception_module: PerceptionModule):
        """
        Inicializar sistema de recompensas
        
        Args:
            perception_module: Módulo de percepción para obtener estado del usuario
        """
        self.perception = perception_module
        
        # Pesos por tipo de recompensa
        self.reward_weights = {
            'satisfaction': 0.4,
            'discovery': 0.3,
            'social_alignment': 0.2,
            'engagement': 0.1
        }
        
        logger.info("MultimodalRewardSystem inicializado")
    
    def calculate_reward(self, user_id: int, strategy: str, outcome: str = 'positive',
                        user_state: Dict = None) -> Tuple[float, Dict]:
        """
        Calcular recompensa multimodal
        
        Args:
            user_id: ID del usuario
            strategy: Estrategia de recomendación utilizada
            outcome: Resultado del feedback ('positive', 'neutral', 'negative')
            user_state: Estado del usuario (opcional, se calculará si no se proporciona)
            
        Returns:
            Tupla (recompensa final, componentes de recompensa)
        """
        if user_state is None:
            user_state = self.perception.get_user_state(user_id)
        
        # Base reward según outcome
        base_rewards = {
            'positive': 0.8,
            'neutral': 0.5,
            'negative': 0.2
        }
        base_reward = base_rewards.get(outcome, 0.5)
        
        # Componentes de recompensa
        components = {}
        
        # Satisfaction: Basado en engagement musical del usuario
        components['satisfaction'] = base_reward * (0.7 + 0.3 * user_state['music_engagement'])
        
        # Discovery: Bonificado si el usuario es explorador
        if strategy == 'Exploration':
            discovery_bonus = 0.8 + 0.2 * user_state['music_diversity']
        else:
            discovery_bonus = 0.6 + 0.2 * user_state['music_diversity']
        components['discovery'] = base_reward * discovery_bonus
        
        # Social Alignment: Bonificado para estrategias sociales
        if strategy == 'Social Influence':
            social_bonus = 0.7 + 0.3 * user_state['social_connectivity']
        else:
            social_bonus = 0.5 + 0.2 * user_state['social_connectivity']
        components['social_alignment'] = base_reward * social_bonus
        
        # Engagement: Basado en actividad general
        components['engagement'] = base_reward * (0.6 + 0.4 * user_state['overall_sophistication'])
        
        # Calcular recompensa final ponderada
        final_reward = sum(components[comp] * self.reward_weights[comp] for comp in components)
        
        # Añadir ruido realista
        noise = np.random.normal(0, 0.05)
        final_reward = max(0, min(1, final_reward + noise))
        
        logger.debug(f"Recompensa calculada para usuario {user_id}: {final_reward:.3f} (outcome={outcome})")
        
        return final_reward, components

