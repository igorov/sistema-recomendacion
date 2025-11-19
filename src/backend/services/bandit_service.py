"""Servicio de Multi-Armed Bandit - Algoritmo UCB"""
import numpy as np
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class UCBBandit:
    """Implementación del algoritmo Upper Confidence Bound (UCB) para Multi-Armed Bandit"""
    
    def __init__(self, arms: List[str], confidence_level: float = 1.5):
        """
        Inicializar UCB Bandit
        
        Args:
            arms: Lista de brazos (estrategias) disponibles
            confidence_level: Nivel de confianza para el bound
        """
        self.arms = arms
        self.n_arms = len(arms)
        self.confidence_level = confidence_level
        
        # Estadísticas por brazo
        self.arm_counts = np.zeros(self.n_arms)
        self.arm_rewards = np.zeros(self.n_arms)
        self.arm_means = np.zeros(self.n_arms)
        self.ucb_values = np.full(self.n_arms, float('inf'))
        
        # Historial
        self.history = []
        self.total_steps = 0
        
        logger.info(f"UCBBandit inicializado con {self.n_arms} brazos: {arms}")
    
    def select_arm(self) -> Tuple[int, str]:
        """
        Seleccionar brazo usando UCB
        
        Returns:
            Tupla (índice del brazo, tipo de acción)
        """
        # Primero explorar todos los brazos no jugados
        unplayed_arms = np.where(self.arm_counts == 0)[0]
        if len(unplayed_arms) > 0:
            selected_arm = unplayed_arms[0]
            logger.debug(f"Seleccionando brazo no jugado: {self.arms[selected_arm]}")
            return selected_arm, 'explore_unplayed'
        
        # Calcular UCB values y seleccionar el mejor
        self._calculate_ucb_values()
        selected_arm = int(np.argmax(self.ucb_values))
        
        logger.debug(f"Seleccionando brazo UCB: {self.arms[selected_arm]} "
                    f"(UCB={self.ucb_values[selected_arm]:.3f})")
        
        return selected_arm, 'ucb_optimistic'
    
    def _calculate_ucb_values(self) -> None:
        """Calcular Upper Confidence Bounds para cada brazo"""
        for i in range(self.n_arms):
            if self.arm_counts[i] > 0:
                confidence_bonus = self.confidence_level * np.sqrt(
                    np.log(self.total_steps + 1) / self.arm_counts[i]
                )
                self.ucb_values[i] = self.arm_means[i] + confidence_bonus
    
    def update(self, arm: int, reward: float) -> None:
        """
        Actualizar estadísticas después de recibir recompensa
        
        Args:
            arm: Índice del brazo seleccionado
            reward: Recompensa recibida
        """
        self.arm_counts[arm] += 1
        self.arm_rewards[arm] += reward
        self.arm_means[arm] = self.arm_rewards[arm] / self.arm_counts[arm]
        
        self.history.append({
            'step': self.total_steps,
            'arm': arm,
            'arm_name': self.arms[arm],
            'reward': reward
        })
        
        self.total_steps += 1
        
        logger.debug(f"Brazo {self.arms[arm]} actualizado: "
                    f"count={self.arm_counts[arm]}, mean={self.arm_means[arm]:.3f}")
    
    def get_statistics(self) -> Dict:
        """
        Obtener estadísticas del bandit
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'total_steps': self.total_steps,
            'arm_counts': self.arm_counts.tolist(),
            'arm_means': self.arm_means.tolist(),
            'arm_names': self.arms,
            'ucb_values': self.ucb_values.tolist(),
            'history': self.history[-10:]  # Últimas 10 interacciones
        }

