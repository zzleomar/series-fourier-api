#!/bin/bash
# Script para ejecutar la API FastAPI de Fourier

cd "$(dirname "$0")"

# Verificar si existe un entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar la API
echo "Iniciando API en http://0.0.0.0:8000"
echo "Documentación disponible en http://0.0.0.0:8000/api/docs"
python main.py
