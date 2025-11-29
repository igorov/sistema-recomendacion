#!/bin/bash

# Script para iniciar el sistema completo de recomendación colaborativo

echo "=========================================="
echo "Sistema de Recomendación Colaborativo"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para verificar si un puerto está en uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Verificar puertos
if check_port 5001; then
    echo -e "${RED}⚠ El puerto 5001 (Backend) ya está en uso${NC}"
    echo "Por favor cierra el proceso o cambia el puerto"
    exit 1
fi

if check_port 5002; then
    echo -e "${RED}⚠ El puerto 5002 (Frontend) ya está en uso${NC}"
    echo "Por favor cierra el proceso o cambia el puerto"
    exit 1
fi

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Instalar dependencias del backend
echo -e "${BLUE}📦 Instalando dependencias del backend...${NC}"
cd "$BASE_DIR/backend_colaborativo"
pip install -q -r requirements.txt

# Instalar dependencias del frontend
echo -e "${BLUE}📦 Instalando dependencias del frontend...${NC}"
cd "$BASE_DIR/app_colaborativo"
pip install -q -r requirements.txt

echo ""
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Iniciar backend en segundo plano
echo -e "${BLUE}🚀 Iniciando Backend API (puerto 5001)...${NC}"
cd "$BASE_DIR/backend_colaborativo"
python api.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Esperar a que el backend esté listo
echo "Esperando a que el backend esté listo..."
sleep 5

# Verificar que el backend está corriendo
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Error al iniciar el backend${NC}"
    echo "Ver backend.log para más detalles"
    exit 1
fi

# Iniciar frontend en segundo plano
echo -e "${BLUE}🚀 Iniciando Frontend (puerto 5002)...${NC}"
cd "$BASE_DIR/app_colaborativo"
python app.py > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Esperar a que el frontend esté listo
sleep 3

# Verificar que el frontend está corriendo
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Error al iniciar el frontend${NC}"
    echo "Ver frontend.log para más detalles"
    kill $BACKEND_PID
    exit 1
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Sistema iniciado correctamente!"
echo "==========================================${NC}"
echo ""
echo -e "${BLUE}📍 URLs:${NC}"
echo "   - Frontend: http://localhost:5002"
echo "   - Backend API: http://localhost:5001"
echo ""
echo -e "${BLUE}📋 PIDs:${NC}"
echo "   - Backend: $BACKEND_PID"
echo "   - Frontend: $FRONTEND_PID"
echo ""
echo -e "${BLUE}📄 Logs:${NC}"
echo "   - Backend: $BASE_DIR/backend_colaborativo/backend.log"
echo "   - Frontend: $BASE_DIR/app_colaborativo/frontend.log"
echo ""
echo -e "${RED}Para detener el sistema:${NC}"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${GREEN}¡Abre http://localhost:5002 en tu navegador!${NC}"
echo ""

# Guardar PIDs en un archivo para poder detenerlos después
echo "$BACKEND_PID $FRONTEND_PID" > "$BASE_DIR/.colaborativo_pids"

# Esperar
wait
