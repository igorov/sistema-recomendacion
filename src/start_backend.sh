#!/bin/bash

echo "🚀 Iniciando Backend (FastAPI)..."
echo "================================="

cd "$(dirname "$0")/backend"

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

# Iniciar servidor
echo "🎯 Iniciando servidor FastAPI en http://localhost:8000"
echo "📚 Documentación API disponible en http://localhost:8000/docs"
echo "================================="

python main.py

