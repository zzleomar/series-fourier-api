# Guía de Despliegue - Fourier API

## Opción 1: Hugging Face Spaces (Sin tarjeta requerida) ⭐

### Pasos:
1. Crear cuenta en https://huggingface.co (gratis, sin tarjeta)
2. Ir a https://huggingface.co/spaces
3. Click en "Create new Space"
4. Configurar:
   - **Name:** fourier-api
   - **License:** MIT
   - **Space SDK:** Docker
   - **Visibility:** Public

5. Clonar el repositorio del Space:
```bash
git clone https://huggingface.co/spaces/TU_USERNAME/fourier-api
cd fourier-api
```

6. Copiar los archivos de tu API:
```bash
cp -r /home/leomar/Documents/proyectos/python/proyecto\ seriesFourier/api/* .
```

7. Commit y push:
```bash
git add .
git commit -m "Initial deployment"
git push
```

8. La URL será: `https://TU_USERNAME-fourier-api.hf.space`

---

## Opción 2: Railway.app (Puede requerir tarjeta)

### Pasos:
1. Crear cuenta en https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Conectar tu repositorio
4. Railway detectará automáticamente el Dockerfile
5. Desplegar

**Nota:** Railway ofrece $5 de crédito gratis mensualmente sin tarjeta, pero puede solicitarla después.

---

## Opción 3: Fly.io (Requiere tarjeta para verificación)

### Pasos:
```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Desde el directorio de la API
flyctl launch

# Configurar fly.toml cuando se genere
flyctl deploy
```

---

## Opción 4: PythonAnywhere (Sin tarjeta, limitado)

### Limitaciones:
- Solo permite conexiones a dominios en whitelist
- No tan flexible como las otras opciones

### Pasos:
1. Crear cuenta gratuita en https://www.pythonanywhere.com
2. Subir archivos manualmente
3. Configurar WSGI para FastAPI

---

## Variables de Entorno (si las necesitas)

Para cualquier plataforma, puedes agregar variables de entorno en su dashboard:
- `PORT` - Generalmente se asigna automáticamente
- Otras variables según tus necesidades

---

## Recomendación Final

**Hugging Face Spaces** es la mejor opción sin tarjeta y funciona perfectamente con tu Dockerfile existente.
