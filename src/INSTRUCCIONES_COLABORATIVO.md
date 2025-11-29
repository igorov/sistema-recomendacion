# Sistema de Recomendación Musical - Filtrado Colaborativo

## 📋 Descripción

Sistema completo de recomendación musical basado en **Filtrado Colaborativo** usando el algoritmo **SVD (Singular Value Decomposition)**.

El sistema está compuesto por:
- **Backend API** (puerto 5001): Servicio REST que implementa el algoritmo de recomendación
- **Frontend Web** (puerto 5002): Aplicación Flask con interfaz de usuario moderna

## 🏗️ Arquitectura

```
src/
├── backend_colaborativo/         # API de Recomendación
│   ├── recommender.py           # Lógica del modelo SVD
│   ├── api.py                   # API REST con Flask
│   ├── requirements.txt         # Dependencias del backend
│   ├── model.pkl               # Modelo entrenado (se genera automáticamente)
│   └── README.md               # Documentación del backend
│
├── app_colaborativo/            # Aplicación Web
│   ├── app.py                  # Aplicación Flask
│   ├── templates/              # Templates HTML
│   │   ├── base.html          # Template base
│   │   ├── login.html         # Pantalla de login
│   │   └── home.html          # Pantalla principal
│   ├── requirements.txt        # Dependencias del frontend
│   └── README.md              # Documentación del frontend
│
├── start_colaborativo.sh       # Script para iniciar todo el sistema
└── stop_colaborativo.sh        # Script para detener el sistema
```

## 🚀 Inicio Rápido

### Opción 1: Usando el script de inicio automático

```bash
cd src
chmod +x start_colaborativo.sh
./start_colaborativo.sh
```

Este script:
1. Instala todas las dependencias
2. Inicia el backend en el puerto 5001
3. Inicia el frontend en el puerto 5002
4. Muestra los logs y PIDs de los procesos

### Opción 2: Inicio manual

**Terminal 1 - Backend:**
```bash
cd src/backend_colaborativo
pip install -r requirements.txt
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd src/app_colaborativo
pip install -r requirements.txt
python app.py
```

## 🌐 Acceso a la Aplicación

Una vez iniciado el sistema:

1. **Aplicación Web**: http://localhost:5002
2. **API Backend**: http://localhost:5001

## 📱 Uso de la Aplicación

### Paso 1: Login
- Abre http://localhost:5002 en tu navegador
- Ingresa un ID de usuario válido (ejemplo: 2, 100, 500)
- El sistema validará que el usuario existe en la base de datos

### Paso 2: Ver Recomendaciones
- La pantalla principal muestra:
  - **Tu Música Más Escuchada**: Top 6 artistas que más has escuchado
  - **Recomendaciones Personalizadas**: Top 12 artistas recomendados para ti
- Cada recomendación incluye:
  - Nombre del artista
  - Score de recomendación
  - Link al perfil de Last.fm (si está disponible)

### Paso 3: Cambiar de Usuario
- Usa el botón "Cambiar" en la barra superior para probar con otro usuario
- O usa el botón "Salir" para cerrar sesión

## 🔧 API Endpoints

El backend expone los siguientes endpoints:

### 1. Health Check
```bash
GET http://localhost:5001/health
```

### 2. Obtener todos los usuarios
```bash
GET http://localhost:5001/users
```

### 3. Obtener recomendaciones
```bash
GET http://localhost:5001/recommendations/<user_id>?top_k=10
```

### 4. Obtener historial de usuario
```bash
GET http://localhost:5001/user/<user_id>/history?top_k=10
```

### 5. Validar usuario
```bash
GET http://localhost:5001/user/<user_id>/validate
```

## 🧪 Ejemplos con curl

```bash
# Ver recomendaciones para usuario 2
curl http://localhost:5001/recommendations/2?top_k=5

# Ver historial de usuario 100
curl http://localhost:5001/user/100/history?top_k=5

# Validar si existe usuario 500
curl http://localhost:5001/user/500/validate
```

## 🛑 Detener el Sistema

### Con el script:
```bash
./stop_colaborativo.sh
```

### Manualmente:
```bash
# Ver los PIDs guardados
cat .colaborativo_pids

# Detener los procesos
kill <BACKEND_PID> <FRONTEND_PID>
```

## 📊 Algoritmo: Filtrado Colaborativo con SVD

El sistema utiliza **Matrix Factorization** con **SVD Truncado**:

1. **Matriz Usuario-Artista**: Se crea una matriz dispersa con las reproducciones
2. **Normalización**: Transformación logarítmica para manejar la dispersión
3. **SVD**: Descomposición en 50 componentes latentes
4. **Scoring**: Producto punto entre factores de usuario y artista
5. **Filtrado**: Se excluyen artistas ya escuchados
6. **Ranking**: Se ordenan por score y se devuelven los top-k

### Ventajas del enfoque:
- ✓ Captura patrones latentes de preferencias musicales
- ✓ Maneja bien la dispersión de datos (99.72% sparse)
- ✓ Escalable a grandes datasets
- ✓ No requiere información de contenido (basado solo en comportamiento)

## 📦 Dependencias

### Backend:
- Flask 3.0.0
- Flask-CORS 4.0.0
- pandas 2.2.0
- numpy 1.26.4
- scikit-learn 1.4.0
- scipy 1.12.0

### Frontend:
- Flask 3.0.0
- requests 2.31.0

## 🎨 Características de la Interfaz

- **Diseño moderno**: Tema oscuro inspirado en Spotify
- **Responsive**: Compatible con móviles y tablets
- **Intuitivo**: Navegación simple y clara
- **Informativo**: Muestra scores y estadísticas
- **Rápido**: Carga asíncrona de datos

## 📝 Notas Importantes

1. **Primera ejecución**: El backend entrenará el modelo la primera vez (puede tomar 1-2 minutos)
2. **Modelo guardado**: El modelo se guarda en `model.pkl` para reutilización
3. **Datos**: Los archivos `.dat` deben estar en `notebooks/` directory
4. **Usuarios válidos**: Solo funcionan IDs de usuarios existentes en el dataset
5. **Puertos**: Backend (5001) y Frontend (5002) deben estar libres

## 🐛 Troubleshooting

### Error: "Puerto ya en uso"
```bash
# Ver qué proceso está usando el puerto
lsof -i :5001
lsof -i :5002

# Detener el proceso
kill <PID>
```

### Error: "Usuario no encontrado"
```bash
# Ver lista de usuarios disponibles
curl http://localhost:5001/users

# Probar con un usuario de la lista
```

### Error: "Modelo no cargado"
```bash
# Eliminar modelo corrupto y reiniciar
rm backend_colaborativo/model.pkl
./start_colaborativo.sh
```

## 📚 Recursos Adicionales

- [Documentación del Backend](backend_colaborativo/README.md)
- [Documentación del Frontend](app_colaborativo/README.md)
- [Notebook Original](../notebooks/SR_Filtrado_Colaborativo.ipynb)

## 🎯 Próximos Pasos

Posibles mejoras:
- [ ] Añadir autenticación real
- [ ] Guardar favoritos del usuario
- [ ] Mostrar carátulas de álbumes
- [ ] Añadir reproductor de música
- [ ] Implementar feedback de recomendaciones
- [ ] A/B testing de algoritmos
