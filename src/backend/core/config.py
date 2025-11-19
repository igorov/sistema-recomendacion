"""Configuración de la aplicación"""
from pathlib import Path


class Settings:
    """Configuración general de la aplicación"""
    
    # API Configuration
    API_TITLE: str = "Sistema de Recomendación Inteligente"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API REST para sistema de recomendación musical con agente inteligente"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Data paths
    DATA_PATH: Path = Path(__file__).parent.parent.parent.parent / "notebooks"
    
    # Agent Configuration
    CONFIDENCE_LEVEL_NEW_USER: float = 2.0
    CONFIDENCE_LEVEL_EXPERIENCED_USER: float = 1.2
    MIN_INTERACTIONS_FOR_PERSONALIZATION: int = 5
    
    # Recommendation Strategies
    RECOMMENDATION_STRATEGIES: list = [
        'Social Influence',
        'Semantic Coherence',
        'Exploration',
        'Traditional CF'
    ]


settings = Settings()

