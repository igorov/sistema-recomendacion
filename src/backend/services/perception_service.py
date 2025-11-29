"""Servicio de Percepción - Módulo de percepción multimodal"""
import pandas as pd
import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class PerceptionModule:
    """Módulo de percepción multimodal para análisis de usuarios"""
    
    def __init__(self, user_artists: pd.DataFrame, user_friends: pd.DataFrame,
                 user_tagged: pd.DataFrame, artists: pd.DataFrame, tags: pd.DataFrame):
        """
        Inicializar módulo de percepción
        
        Args:
            user_artists: DataFrame de interacciones usuario-artista
            user_friends: DataFrame de relaciones de amistad
            user_tagged: DataFrame de tags asignados
            artists: DataFrame de artistas
            tags: DataFrame de tags
        """
        self.user_artists = user_artists
        self.user_friends = user_friends
        self.user_tagged = user_tagged
        self.artists = artists
        self.tags = tags
        
        # Pre-computar métricas para eficiencia
        self._precompute_statistics()
        
        logger.info("PerceptionModule inicializado con estadísticas pre-computadas")
    
    def _precompute_statistics(self) -> None:
        """Pre-computar estadísticas de usuarios para eficiencia"""
        # Estadísticas musicales
        self.user_music_stats = self.user_artists.groupby('userID').agg({
            'weight': ['sum', 'count', 'mean', 'std'],
            'artistID': 'nunique'
        }).fillna(0)
        self.user_music_stats.columns = [
            'total_plays', 'total_interactions', 'avg_plays', 'std_plays', 'unique_artists'
        ]
        
        # Estadísticas sociales
        self.user_social_stats = self.user_friends.groupby('userID').size().to_frame('num_friends')
        
        # Estadísticas semánticas
        self.user_semantic_stats = self.user_tagged.groupby('userID').agg({
            'tagID': ['count', 'nunique'],
            'artistID': 'nunique'
        }).fillna(0)
        self.user_semantic_stats.columns = ['total_tags', 'unique_tags', 'tagged_artists']
    
    def get_user_state(self, user_id: int) -> Dict:
        """
        Obtener estado unificado del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con el estado del usuario
        """
        state = {'user_id': user_id}
        
        # Señales musicales
        if user_id in self.user_music_stats.index:
            music_data = self.user_music_stats.loc[user_id]
            state['music_engagement'] = min(1.0, music_data['total_plays'] / 10000)
            state['music_diversity'] = min(1.0, music_data['unique_artists'] / 200)
            state['music_intensity'] = min(1.0, music_data['avg_plays'] / 500)
        else:
            state.update({
                'music_engagement': 0.0,
                'music_diversity': 0.0,
                'music_intensity': 0.0
            })
        
        # Señales sociales
        if user_id in self.user_social_stats.index:
            social_data = self.user_social_stats.loc[user_id]
            state['social_connectivity'] = min(1.0, social_data['num_friends'] / 20)
            
            # Calcular overlap musical con amigos
            friends = self.user_friends[self.user_friends['userID'] == user_id]['friendID'].tolist()
            if friends:
                user_music = set(self.user_artists[self.user_artists['userID'] == user_id]['artistID'])
                friends_music = set(self.user_artists[self.user_artists['userID'].isin(friends)]['artistID'])
                if user_music and friends_music:
                    overlap = len(user_music.intersection(friends_music)) / len(user_music.union(friends_music))
                    state['social_alignment'] = overlap
                else:
                    state['social_alignment'] = 0.0
            else:
                state['social_alignment'] = 0.0
        else:
            state.update({
                'social_connectivity': 0.0,
                'social_alignment': 0.0
            })
        
        # Señales semánticas
        if user_id in self.user_semantic_stats.index:
            semantic_data = self.user_semantic_stats.loc[user_id]
            state['semantic_activity'] = min(1.0, semantic_data['total_tags'] / 200)
            state['semantic_diversity'] = min(1.0, semantic_data['unique_tags'] / 50)
        else:
            state.update({
                'semantic_activity': 0.0,
                'semantic_diversity': 0.0
            })
        
        # Score compuesto
        state['overall_sophistication'] = np.mean([
            state['music_diversity'],
            state['social_connectivity'],
            state['semantic_diversity']
        ])
        
        logger.debug(f"Estado del usuario {user_id}: sophistication={state['overall_sophistication']:.2f}")
        
        return state

