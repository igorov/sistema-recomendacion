#!/bin/bash

echo "🎨 Iniciando Frontend (Flask)..."
echo "================================="

cd "$(dirname "$0")/app"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env..."
    echo "API_BASE_URL=http://localhost:8000" > .env
    echo "FLASK_ENV=development" >> .env
fi

# Iniciar servidor
echo "🎯 Iniciando servidor Flask en http://localhost:5000"
echo "================================="

python app.py

