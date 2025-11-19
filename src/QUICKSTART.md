# 🚀 Inicio Rápido

## Opción 1: Iniciar Todo Automáticamente

```bash
cd src
./start_all.sh
```

Este script iniciará tanto el backend como el frontend automáticamente.

## Opción 2: Iniciar Manualmente

### Paso 1: Iniciar el Backend (Terminal 1)

```bash
cd src
./start_backend.sh
```

O manualmente:

```bash
cd src/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

El backend estará disponible en: **http://localhost:8000**

### Paso 2: Iniciar el Frontend (Terminal 2)

```bash
cd src
./start_frontend.sh
```

O manualmente:

```bash
cd src/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

El frontend estará disponible en: **http://localhost:5000**

## 📱 Acceso a la Aplicación

Una vez iniciados ambos servicios:

1. Abre tu navegador en **http://localhost:5000**
2. Selecciona un usuario de la lista o usa el botón "Usuario Aleatorio"
3. Haz clic en "Cargar Usuario" para ver su perfil
4. Obtén recomendaciones y proporciona feedback
5. Observa cómo el agente aprende y se adapta

## 📚 Documentación de la API

La documentación interactiva de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Verificar Estado

Para verificar que el backend está funcionando:

```bash
curl http://localhost:8000/health
```

## ⚠️ Solución de Problemas

### Error: No se encuentran los datos

Asegúrate de que los archivos `.dat` estén en la carpeta `notebooks/`:
- artists.dat
- user_artists.dat
- tags.dat
- user_taggedartists.dat
- user_friends.dat

### Error: Puerto ya en uso

Si el puerto 8000 o 5000 ya está en uso:

```bash
# Ver qué está usando el puerto
lsof -i :8000
lsof -i :5000

# Matar el proceso
kill -9 <PID>
```

### Error de dependencias

```bash
# Backend
cd src/backend
pip install --upgrade -r requirements.txt

# Frontend
cd src/app
pip install --upgrade -r requirements.txt
```

## 🎯 Próximos Pasos

1. Experimenta con diferentes usuarios
2. Observa cómo cambian las estrategias de recomendación
3. Analiza las estadísticas del agente
4. Prueba dar diferentes tipos de feedback
5. Observa el aprendizaje continuo del sistema

## 📊 Endpoints Principales de la API

- `GET /api/users` - Lista de usuarios disponibles
- `GET /api/users/{user_id}/state` - Estado del usuario
- `POST /api/recommend` - Obtener recomendación
- `POST /api/feedback` - Enviar feedback
- `GET /api/statistics` - Estadísticas del agente
- `GET /api/users/{user_id}/profile` - Perfil del usuario

