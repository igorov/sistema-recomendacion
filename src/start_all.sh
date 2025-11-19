#!/bin/bash

echo "🚀 Iniciando Sistema de Recomendación Completo"
echo "=============================================="
echo ""

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT

# Iniciar backend en background
echo "1️⃣ Iniciando Backend..."
cd "$(dirname "$0")"
./start_backend.sh > backend.log 2>&1 &
BACKEND_PID=$!

# Esperar a que el backend esté listo
echo "⏳ Esperando a que el backend esté listo..."
sleep 10

# Iniciar frontend en background
echo "2️⃣ Iniciando Frontend..."
./start_frontend.sh > frontend.log 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✅ Sistema iniciado exitosamente!"
echo "=================================="
echo "📊 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🌐 Frontend: http://localhost:5000"
echo "=================================="
echo "📝 Logs:"
echo "   Backend: tail -f src/backend.log"
echo "   Frontend: tail -f src/frontend.log"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Mostrar logs en tiempo real
tail -f backend.log &
TAIL_PID=$!

wait

