# Usar imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto (Cloud Run usa la variable de entorno PORT)
EXPOSE 8080

# Comando para ejecutar la aplicación
# Cloud Run proporciona la variable de entorno PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
