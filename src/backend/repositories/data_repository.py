"""Repositorio de datos - Capa de acceso a datos"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataRepository:
    """Repositorio para acceso a datos del sistema"""
    
    def __init__(self, data_path: Path):
        """
        Inicializar repositorio de datos
        
        Args:
            data_path: Ruta a los archivos de datos
        """
        self.data_path = data_path
        self._artists: Optional[pd.DataFrame] = None
        self._user_artists: Optional[pd.DataFrame] = None
        self._tags: Optional[pd.DataFrame] = None
        self._user_tagged: Optional[pd.DataFrame] = None
        self._user_friends: Optional[pd.DataFrame] = None
        
        # Cargar datos al inicializar
        self.load_data()
    
    def load_data(self) -> None:
        """Cargar todos los datasets"""
        try:
            logger.info(f"Cargando datos desde {self.data_path}")
            
            # Artistas
            self._artists = pd.read_csv(
                self.data_path / 'artists.dat',
                sep='\t',
                encoding='latin-1'
            )
            
            # Interacciones usuario-artista
            self._user_artists = pd.read_csv(
                self.data_path / 'user_artists.dat',
                sep='\t',
                encoding='latin-1'
            )
            
            # Tags
            self._tags = pd.read_csv(
                self.data_path / 'tags.dat',
                sep='\t',
                encoding='latin-1'
            )
            
            # Tags de usuarios
            self._user_tagged = pd.read_csv(
                self.data_path / 'user_taggedartists.dat',
                sep='\t',
                encoding='latin-1'
            )
            
            # Amigos
            self._user_friends = pd.read_csv(
                self.data_path / 'user_friends.dat',
                sep='\t',
                encoding='latin-1'
            )
            
            # Procesar fechas
            self._user_tagged['date'] = pd.to_datetime(
                self._user_tagged[['year', 'month', 'day']]
            )
            
            logger.info(f"✅ Datos cargados: {len(self._artists)} artistas, "
                       f"{len(self._user_artists)} interacciones, "
                       f"{len(self._user_friends)} relaciones de amistad")
            
        except Exception as e:
            logger.error(f"Error cargando datos: {e}")
            raise
    
    @property
    def artists(self) -> pd.DataFrame:
        """Obtener DataFrame de artistas"""
        return self._artists
    
    @property
    def user_artists(self) -> pd.DataFrame:
        """Obtener DataFrame de interacciones usuario-artista"""
        return self._user_artists
    
    @property
    def tags(self) -> pd.DataFrame:
        """Obtener DataFrame de tags"""
        return self._tags
    
    @property
    def user_tagged(self) -> pd.DataFrame:
        """Obtener DataFrame de tags de usuarios"""
        return self._user_tagged
    
    @property
    def user_friends(self) -> pd.DataFrame:
        """Obtener DataFrame de amigos"""
        return self._user_friends
    
    def get_artist_name(self, artist_id: int) -> str:
        """
        Obtener nombre de artista por ID
        
        Args:
            artist_id: ID del artista
            
        Returns:
            Nombre del artista o ID como string si no se encuentra
        """
        result = self._artists[self._artists['id'] == artist_id]
        if len(result) > 0:
            return result['name'].iloc[0]
        return f"Artist_{artist_id}"
    
    def get_user_exists(self, user_id: int) -> bool:
        """
        Verificar si un usuario existe
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si el usuario existe, False en caso contrario
        """
        return user_id in self._user_artists['userID'].values
    
    def get_available_users(self, limit: int = 100) -> list:
        """
        Obtener lista de usuarios disponibles
        
        Args:
            limit: Número máximo de usuarios a retornar
            
        Returns:
            Lista de IDs de usuarios
        """
        return self._user_artists['userID'].unique()[:limit].tolist()
    
    def get_user_listening_history(self, user_id: int) -> pd.DataFrame:
        """
        Obtener historial de escucha de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            DataFrame con historial de escucha
        """
        return self._user_artists[self._user_artists['userID'] == user_id]
    
    def get_user_friends_list(self, user_id: int) -> list:
        """
        Obtener lista de amigos de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de IDs de amigos
        """
        friends = self._user_friends[self._user_friends['userID'] == user_id]
        return friends['friendID'].tolist()
    
    def get_user_tags(self, user_id: int) -> pd.DataFrame:
        """
        Obtener tags asignados por un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            DataFrame con tags del usuario
        """
        return self._user_tagged[self._user_tagged['userID'] == user_id]

