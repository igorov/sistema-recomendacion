#!/bin/bash

# Script para detener el sistema de recomendación colaborativo

echo "Deteniendo sistema de recomendación colaborativo..."

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BASE_DIR/.colaborativo_pids"

if [ -f "$PID_FILE" ]; then
    PIDS=$(cat "$PID_FILE")
    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo "Deteniendo proceso $PID..."
            kill $PID
        fi
    done
    rm "$PID_FILE"
    echo "✓ Sistema detenido"
else
    echo "No se encontró archivo de PIDs"
    echo "Buscando procesos manualmente..."
    
    # Buscar procesos por puerto
    BACKEND_PID=$(lsof -ti:5001)
    FRONTEND_PID=$(lsof -ti:5002)
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Deteniendo backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "Deteniendo frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi
    
    if [ -z "$BACKEND_PID" ] && [ -z "$FRONTEND_PID" ]; then
        echo "No se encontraron procesos activos"
    else
        echo "✓ Procesos detenidos"
    fi
fi
