# Backend Colaborativo - API de Recomendación

API REST para el sistema de recomendación basado en Filtrado Colaborativo usando SVD.

## Descripción

Este backend implementa un sistema de recomendación de artistas musicales utilizando:
- **Filtrado Colaborativo** con Matrix Factorization (SVD)
- Dataset Last.fm con historial de reproducción de usuarios

## Instalación

```bash
cd src/backend_colaborativo
pip install -r requirements.txt
```

## Uso

```bash
python api.py
```

El servidor se iniciará en `http://localhost:5001`

## Endpoints

### 1. Health Check
```
GET /health
```
Verifica el estado del servicio y si el modelo está cargado.

### 2. Obtener Usuarios
```
GET /users
```
Retorna la lista de todos los usuarios disponibles.

### 3. Obtener Recomendaciones
```
GET /recommendations/<user_id>?top_k=10
```
Retorna las recomendaciones de artistas para un usuario específico.

**Parámetros:**
- `user_id`: ID del usuario (requerido)
- `top_k`: Número de recomendaciones (opcional, default: 10)

**Respuesta:**
```json
{
  "user_id": 2,
  "recommendations": [
    {
      "artistID": 123,
      "name": "Pet Shop Boys",
      "score": 5.277,
      "url": "http://...",
      "pictureURL": "http://..."
    }
  ],
  "total": 10
}
```

### 4. Obtener Historial
```
GET /user/<user_id>/history?top_k=10
```
Retorna el historial de reproducción de un usuario.

### 5. Validar Usuario
```
GET /user/<user_id>/validate
```
Verifica si un usuario existe en el sistema.

## Arquitectura

- **recommender.py**: Implementación del modelo de Filtrado Colaborativo
- **api.py**: API REST con Flask
- **model.pkl**: Modelo entrenado (se genera automáticamente)

## Notas

- El modelo se entrena automáticamente la primera vez que se inicia el servidor
- Los datos se cargan desde `../../notebooks/*.dat`
- El modelo entrenado se guarda en `model.pkl` para reutilización
