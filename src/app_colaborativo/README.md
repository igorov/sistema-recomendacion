# App Colaborativo - Frontend

Aplicación web Flask para el sistema de recomendación musical basado en Filtrado Colaborativo.

## Descripción

Esta aplicación web proporciona una interfaz de usuario para interactuar con el sistema de recomendación:
- **Login simple** por ID de usuario
- **Visualización del historial** de reproducción del usuario
- **Recomendaciones personalizadas** de artistas musicales
- **Interfaz moderna** con Bootstrap 5 y diseño responsive

## Instalación

```bash
cd src/app_colaborativo
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

La aplicación se iniciará en `http://localhost:5002`

## Configuración

La aplicación se conecta por defecto al backend en `http://localhost:5001`. Puedes cambiar esto con la variable de entorno:

```bash
export BACKEND_URL=http://localhost:5001
python app.py
```

## Funcionalidades

### 1. Login
- Pantalla inicial donde el usuario ingresa su ID
- Validación de usuario contra el backend
- Manejo de sesiones

### 2. Home
- Muestra el historial de reproducción del usuario (top 6 artistas más escuchados)
- Muestra recomendaciones personalizadas (top 12 artistas recomendados)
- Información del score de cada recomendación
- Links a los perfiles de Last.fm de los artistas

### 3. Características
- Diseño moderno y responsive
- Tema oscuro inspirado en aplicaciones musicales
- Mensajes flash para feedback al usuario
- Navegación intuitiva

## Estructura

```
app_colaborativo/
├── app.py              # Aplicación principal Flask
├── templates/
│   ├── base.html       # Template base con navbar y estilos
│   ├── login.html      # Pantalla de login
│   └── home.html       # Pantalla principal con recomendaciones
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## Notas

- Requiere que el backend esté corriendo en el puerto 5001
- Usa sesiones de Flask para mantener el estado del usuario
- Responsive design compatible con dispositivos móviles
