# Deploy en Google Cloud Run

## Requisitos previos

- Cuenta en [Google Cloud](https://cloud.google.com)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) instalado y autenticado
- Proyecto de GCP creado

## 1. Configurar proyecto

```bash
# Iniciar sesión
gcloud auth login

# Seleccionar proyecto (o crearlo)
gcloud config set project TU_PROYECTO_ID
```

## 2. Habilitar APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## 3. Secret para Firebase Admin SDK

```bash
# Crear el secret con el contenido del JSON
gcloud secrets create firebase-adminsdk --data-file=firebase-adminsdk.json
```

O si ya existe:
```bash
gcloud secrets versions add firebase-adminsdk --data-file=firebase-adminsdk.json
```

## 4. Base de datos

**Opción A – SQLite (solo pruebas, datos efímeros)**  
Sin cambios. Los datos se pierden al redeploy.

**Opción B – Cloud SQL (recomendado para producción)**

1. Crear instancia Cloud SQL (MySQL o PostgreSQL)
2. Crear base de datos y usuario
3. Usar `DATABASE_URL` con la cadena de conexión

Ejemplo Cloud SQL + MySQL:
```
mysql+pymysql://usuario:contraseña@/nombre_bd?unix_socket=/cloudsql/PROYECTO:REGION:INSTANCIA
```

## 5. Deploy del contenedor

Desde la carpeta `backend`:

```bash
cd d:\TFG\backend

# Desplegar (Cloud Run construye la imagen automáticamente)
gcloud run deploy guiagym-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "SECRET_KEY=tu_clave_secreta_fuerte,JWT_SECRET_KEY=otra_clave_fuerte" \
  --set-secrets "FIREBASE_ADMINSDK_JSON=firebase-adminsdk:latest"
```

Si usas Cloud SQL, añade:
```bash
--add-cloudsql-instances PROYECTO:REGION:INSTANCIA
--set-env-vars "DATABASE_URL=mysql+pymysql://..."
```

## 6. Variables de entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `SECRET_KEY` | Clave para sesiones Flask | Sí (producción) |
| `JWT_SECRET_KEY` | Clave para JWT | Sí (producción) |
| `DATABASE_URL` | Conexión a BD (Cloud SQL) | Sí si no usas SQLite |
| `FIREBASE_ADMINSDK_JSON` | Secret con el JSON de Firebase | Sí para Google Sign-In |

## 7. URL de la API

Tras el deploy, la API quedará en algo como:
```
https://guiagym-api-XXXXX-ew.a.run.app
```

Actualiza la URL base en la app Android (`RetrofitCliente.kt`) para usar esta URL en producción.

## 8. Probar localmente con Docker

```bash
cd backend
docker build -t guiagym-api .
docker run -p 8080:8080 -e SECRET_KEY=test -e FIREBASE_ADMINSDK_JSON="$(cat firebase-adminsdk.json)" guiagym-api
```

(En Windows PowerShell, ajusta el comando para pasar el JSON según tu entorno.)
