"""Servicio del Agente Inteligente - Lógica principal del agente de recomendación"""
import numpy as np
from datetime import datetime
from typing import Dict, Optional, Tuple
from collections import defaultdict, Counter
import logging

from services.perception_service import PerceptionModule
from services.reward_service import MultimodalRewardSystem
from services.bandit_service import UCBBandit
from repositories.data_repository import DataRepository
from models.entities import (
    Recommendation, DecisionInfo, LearningInfo, AgentStatistics, UserState
)

logger = logging.getLogger(__name__)


class IntelligentRecommendationAgent:
    """Agente inteligente que integra percepción, razonamiento, acción y aprendizaje"""
    
    def __init__(self, perception_module: PerceptionModule,
                 reward_system: MultimodalRewardSystem,
                 data_repository: DataRepository,
                 recommendation_strategies: list,
                 confidence_level_new_user: float = 2.0,
                 confidence_level_experienced_user: float = 1.2):
        """
        Inicializar agente inteligente
        
        Args:
            perception_module: Módulo de percepción
            reward_system: Sistema de recompensas
            data_repository: Repositorio de datos
            recommendation_strategies: Lista de estrategias disponibles
            confidence_level_new_user: Nivel de confianza para usuarios nuevos
            confidence_level_experienced_user: Nivel de confianza para usuarios experimentados
        """
        # Módulos core
        self.perception = perception_module
        self.reward_system = reward_system
        self.data_repository = data_repository
        self.strategies = recommendation_strategies
        
        # Estado del agente
        self.user_agents: Dict[int, UCBBandit] = {}
        self.global_statistics = {
            'total_recommendations': 0,
            'total_reward': 0,
            'user_sessions': defaultdict(list),
            'strategy_performance': defaultdict(list)
        }
        
        # Configuración adaptativa
        self.adaptation_config = {
            'min_interactions_for_personalization': 5,
            'confidence_level_new_user': confidence_level_new_user,
            'confidence_level_experienced_user': confidence_level_experienced_user,
            'reward_history_window': 50
        }
        
        # Memoria de interacciones
        self.interaction_memory = defaultdict(list)
        
        logger.info(f"IntelligentRecommendationAgent inicializado con {len(self.strategies)} estrategias")
    
    def get_user_agent(self, user_id: int) -> UCBBandit:
        """
        Obtener o crear agente bandit personalizado para usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Agente UCBBandit del usuario
        """
        if user_id not in self.user_agents:
            # Determinar configuración inicial basada en perfil del usuario
            user_state = self.perception.get_user_state(user_id)
            
            # Usuarios más sofisticados obtienen configuración más conservadora
            if user_state['overall_sophistication'] > 0.7:
                confidence_level = self.adaptation_config['confidence_level_experienced_user']
            else:
                confidence_level = self.adaptation_config['confidence_level_new_user']
            
            # Crear agente bandit personalizado
            self.user_agents[user_id] = UCBBandit(self.strategies, confidence_level)
            
            logger.info(f"Nuevo agente UCB creado para usuario {user_id} "
                       f"(confidence={confidence_level:.2f})")
        
        return self.user_agents[user_id]
    
    def recommend(self, user_id: int, context: Optional[Dict] = None) -> Tuple[Recommendation, DecisionInfo]:
        """
        Ciclo completo: percepción → razonamiento → acción
        
        Args:
            user_id: ID del usuario
            context: Contexto adicional (opcional)
            
        Returns:
            Tupla (Recomendación, Información de decisión)
        """
        logger.info(f"Generando recomendación para usuario {user_id}")
        
        # PASO 1: PERCEPCIÓN - Obtener estado actual del usuario
        user_state = self.perception.get_user_state(user_id)
        
        # PASO 2: RAZONAMIENTO - Seleccionar estrategia óptima
        user_agent = self.get_user_agent(user_id)
        strategy_idx, action_type = user_agent.select_arm()
        selected_strategy = self.strategies[strategy_idx]
        
        logger.info(f"Estrategia seleccionada: {selected_strategy} (tipo={action_type})")
        
        # PASO 3: ACCIÓN - Generar recomendación específica
        recommendation = self._generate_specific_recommendation(
            user_id, selected_strategy, user_state
        )
        
        # Registrar decisión del agente
        decision_info = DecisionInfo(
            timestamp=datetime.now(),
            user_id=user_id,
            strategy=selected_strategy,
            action_type=action_type,
            user_state=user_state.copy(),
            recommendation=recommendation,
            agent_confidence=self._calculate_agent_confidence(user_agent)
        )
        
        return recommendation, decision_info
    
    def _generate_specific_recommendation(self, user_id: int, strategy: str,
                                         user_state: Dict) -> Recommendation:
        """
        Generar recomendación específica basada en estrategia
        
        Args:
            user_id: ID del usuario
            strategy: Estrategia de recomendación
            user_state: Estado del usuario
            
        Returns:
            Recomendación generada
        """
        if strategy == 'Social Influence':
            return self._social_influence_recommendation(user_id)
        elif strategy == 'Semantic Coherence':
            return self._semantic_coherence_recommendation(user_id)
        elif strategy == 'Exploration':
            return self._exploration_recommendation(user_id)
        else:  # Traditional CF
            return self._traditional_cf_recommendation(user_id)
    
    def _social_influence_recommendation(self, user_id: int) -> Recommendation:
        """Generar recomendación basada en influencia social"""
        friends = self.data_repository.get_user_friends_list(user_id)
        
        if friends:
            friends_music = self.data_repository.user_artists[
                self.data_repository.user_artists['userID'].isin(friends)
            ]
            if len(friends_music) > 0:
                popular_among_friends = friends_music.groupby('artistID')['weight'].sum().idxmax()
                artist_name = self.data_repository.get_artist_name(popular_among_friends)
                
                return Recommendation(
                    artist_id=int(popular_among_friends),
                    artist_name=artist_name,
                    strategy='Social Influence',
                    reason=f"Popular entre tus {len(friends)} amigos",
                    confidence=0.8,
                    timestamp=datetime.now()
                )
        
        # Fallback
        return self._random_recommendation('Social Influence')
    
    def _semantic_coherence_recommendation(self, user_id: int) -> Recommendation:
        """Generar recomendación basada en coherencia semántica"""
        user_tags = self.data_repository.get_user_tags(user_id)
        
        if len(user_tags) > 0:
            user_tag_ids = user_tags['tagID'].unique()
            similar_tagged = self.data_repository.user_tagged[
                self.data_repository.user_tagged['tagID'].isin(user_tag_ids)
            ]
            if len(similar_tagged) > 0:
                candidate_artist = similar_tagged['artistID'].value_counts().index[0]
                artist_name = self.data_repository.get_artist_name(candidate_artist)
                
                return Recommendation(
                    artist_id=int(candidate_artist),
                    artist_name=artist_name,
                    strategy='Semantic Coherence',
                    reason="Coherente con tus tags musicales",
                    confidence=0.7,
                    timestamp=datetime.now()
                )
        
        # Fallback
        return self._random_recommendation('Semantic Coherence')
    
    def _exploration_recommendation(self, user_id: int) -> Recommendation:
        """Generar recomendación exploratoria"""
        # Obtener artistas no escuchados por el usuario
        user_history = self.data_repository.get_user_listening_history(user_id)
        listened_artists = set(user_history['artistID'].values)
        
        all_artists = self.data_repository.artists['id'].values
        unlistened = [a for a in all_artists if a not in listened_artists]
        
        if unlistened:
            artist_id = int(np.random.choice(unlistened))
        else:
            artist_id = int(np.random.choice(all_artists))
        
        artist_name = self.data_repository.get_artist_name(artist_id)
        
        return Recommendation(
            artist_id=artist_id,
            artist_name=artist_name,
            strategy='Exploration',
            reason="Descubre algo nuevo",
            confidence=0.6,
            timestamp=datetime.now()
        )
    
    def _traditional_cf_recommendation(self, user_id: int) -> Recommendation:
        """Generar recomendación con filtrado colaborativo tradicional"""
        # Simplificación: recomendar artista popular no escuchado
        user_history = self.data_repository.get_user_listening_history(user_id)
        listened_artists = set(user_history['artistID'].values)
        
        popular_artists = self.data_repository.user_artists.groupby('artistID')['weight'].sum().sort_values(ascending=False)
        
        for artist_id in popular_artists.index:
            if artist_id not in listened_artists:
                artist_name = self.data_repository.get_artist_name(artist_id)
                return Recommendation(
                    artist_id=int(artist_id),
                    artist_name=artist_name,
                    strategy='Traditional CF',
                    reason="Popular globalmente",
                    confidence=0.7,
                    timestamp=datetime.now()
                )
        
        # Fallback
        return self._random_recommendation('Traditional CF')
    
    def _random_recommendation(self, strategy: str) -> Recommendation:
        """Generar recomendación aleatoria como fallback"""
        random_artist_id = self.data_repository.user_artists['artistID'].sample(1).iloc[0]
        artist_name = self.data_repository.get_artist_name(random_artist_id)
        
        return Recommendation(
            artist_id=int(random_artist_id),
            artist_name=artist_name,
            strategy=strategy,
            reason=f"Recomendación basada en {strategy}",
            confidence=0.5,
            timestamp=datetime.now()
        )
    
    def _calculate_agent_confidence(self, user_agent: UCBBandit) -> float:
        """Calcular confianza del agente en sus decisiones"""
        if user_agent.total_steps == 0:
            return 0.0
        
        interaction_confidence = min(1.0, user_agent.total_steps / 50)
        
        if user_agent.total_steps > 5:
            recent_rewards = [h['reward'] for h in user_agent.history[-10:]]
            reward_stability = 1 / (1 + np.std(recent_rewards))
        else:
            reward_stability = 0.5
        
        return (interaction_confidence + reward_stability) / 2
    
    def learn_from_feedback(self, user_id: int, recommendation: Recommendation,
                           feedback_type: str, feedback_value: Optional[float] = None) -> LearningInfo:
        """
        PASO 4: APRENDIZAJE - Actualizar agente basado en feedback del usuario
        
        Args:
            user_id: ID del usuario
            recommendation: Recomendación realizada
            feedback_type: Tipo de feedback
            feedback_value: Valor del feedback (opcional)
            
        Returns:
            Información sobre el aprendizaje
        """
        logger.info(f"Procesando feedback de usuario {user_id}: tipo={feedback_type}")
        
        # Convertir feedback a outcome
        outcome = self._convert_feedback_to_outcome(feedback_type, feedback_value)
        
        # Calcular recompensa usando sistema multimodal
        user_state = self.perception.get_user_state(user_id)
        reward, reward_components = self.reward_system.calculate_reward(
            user_id, recommendation.strategy, outcome, user_state
        )
        
        # Actualizar agente bandit del usuario
        user_agent = self.get_user_agent(user_id)
        strategy_idx = self.strategies.index(recommendation.strategy)
        user_agent.update(strategy_idx, reward)
        
        # Registrar aprendizaje
        learning_info = LearningInfo(
            timestamp=datetime.now(),
            user_id=user_id,
            feedback_type=feedback_type,
            feedback_value=feedback_value,
            outcome=outcome,
            reward=reward,
            reward_components=reward_components,
            strategy=recommendation.strategy
        )
        
        # Actualizar estadísticas globales
        self.global_statistics['total_recommendations'] += 1
        self.global_statistics['total_reward'] += reward
        self.global_statistics['user_sessions'][user_id].append(learning_info)
        self.global_statistics['strategy_performance'][recommendation.strategy].append(reward)
        
        # Guardar en memoria de interacciones
        self.interaction_memory[user_id].append({
            'recommendation': recommendation,
            'learning': learning_info
        })
        
        logger.info(f"Aprendizaje completado: reward={reward:.3f}, outcome={outcome}")
        
        return learning_info
    
    def _convert_feedback_to_outcome(self, feedback_type: str,
                                    feedback_value: Optional[float]) -> str:
        """Convertir feedback a outcome categórico"""
        if feedback_type == 'explicit_rating' and feedback_value is not None:
            if feedback_value >= 0.7:
                return 'positive'
            elif feedback_value >= 0.4:
                return 'neutral'
            else:
                return 'negative'
        elif feedback_type == 'implicit_behavior' and feedback_value is not None:
            if feedback_value > 0.7:
                return 'positive'
            elif feedback_value > 0.3:
                return 'neutral'
            else:
                return 'negative'
        else:
            # feedback directo
            return feedback_type if feedback_type in ['positive', 'neutral', 'negative'] else 'neutral'
    
    def get_agent_statistics(self) -> AgentStatistics:
        """Obtener estadísticas comprehensivas del agente"""
        strategy_performance = {}
        
        for strategy, rewards in self.global_statistics['strategy_performance'].items():
            if rewards:
                strategy_performance[strategy] = {
                    'count': len(rewards),
                    'avg_reward': float(np.mean(rewards)),
                    'std_reward': float(np.std(rewards)),
                    'success_rate': sum(1 for r in rewards if r > 0.6) / len(rewards)
                }
        
        user_profiles = {}
        for user_id, user_agent in self.user_agents.items():
            if user_agent.total_steps > 0:
                user_state = self.perception.get_user_state(user_id)
                user_profiles[user_id] = {
                    'total_interactions': user_agent.total_steps,
                    'preferred_strategy': self.strategies[np.argmax(user_agent.arm_means)],
                    'agent_confidence': self._calculate_agent_confidence(user_agent),
                    'user_sophistication': user_state['overall_sophistication']
                }
        
        return AgentStatistics(
            total_users=len(self.user_agents),
            total_recommendations=self.global_statistics['total_recommendations'],
            average_reward=(
                self.global_statistics['total_reward'] / 
                max(1, self.global_statistics['total_recommendations'])
            ),
            active_sessions=len([
                uid for uid, sessions in self.global_statistics['user_sessions'].items()
                if sessions
            ]),
            strategy_performance=strategy_performance,
            user_profiles=user_profiles
        )
    
    def get_user_profile(self, user_id: int) -> Dict:
        """Obtener perfil detallado de un usuario"""
        if user_id not in self.user_agents:
            return None
        
        user_agent = self.user_agents[user_id]
        user_state = self.perception.get_user_state(user_id)
        
        return {
            'user_id': user_id,
            'total_interactions': user_agent.total_steps,
            'preferred_strategy': self.strategies[np.argmax(user_agent.arm_means)] if user_agent.total_steps > 0 else 'None',
            'agent_confidence': self._calculate_agent_confidence(user_agent),
            'user_sophistication': user_state['overall_sophistication'],
            'interaction_history': self.interaction_memory.get(user_id, [])[-10:]
        }

