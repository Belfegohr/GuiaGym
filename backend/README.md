# API GuiaGym

API REST en Python (Flask) para la app de rutinas de ejercicios. Integrada con Firebase Auth y migracion progresiva a Firestore. Tecnologías: Python, Flask, SQLAlchemy, Firebase Admin, bcrypt.

## Estado actual de autenticacion

- La API valida `id_token` de Firebase en `Authorization: Bearer <token>`.
- Endpoints `POST /auth/login` y `POST /auth/registro` requieren `id_token`.
- `POST /auth/renovar` no aplica: la renovacion se hace con el SDK de Firebase en cliente.
- Para ejecutar, define `FIREBASE_ADMINSDK_JSON` (ruta al JSON o el JSON completo en variable).

## Ejecutar con Docker (recomendado)

1. Entra en la carpeta del backend:

```bash
cd backend
```

2. Crea el archivo de variables:

```bash
cp env.example .env
```

En Windows PowerShell:

```powershell
copy env.example .env
```

3. Levanta la API:

```bash
docker compose up -d --build
```

4. Comprueba que está activa:

```bash
docker compose ps
```

La API quedará en `http://localhost:5000`.

Para pararla:

```bash
docker compose down
```

## Requisitos

- Python 3.10 o superior
- MySQL (crear base de datos `fitness_app`)

## Instalación

```bash
cd backend
pip install -r requirements.txt
```

## Configuración

Crear la base de datos en MySQL:

```sql
CREATE DATABASE fitness_app;
```

Configurar la conexión en `app/configuracion.py` o con variables de entorno:

- `DATABASE_URL`: mysql+pymysql://usuario:contraseña@localhost:3306/fitness_app
- `SECRET_KEY` y `JWT_SECRET_KEY`: claves secretas (opcional)

## Ejecutar

```bash
python run.py
```

La API estará en http://localhost:5000

## Rutas principales

- **Auth**: POST /auth/registro, POST /auth/login, POST /auth/renovar
- **Usuarios**: GET/PUT /usuarios/mi_perfil, GET /usuarios/{id}
- **Ejercicios**: GET /ejercicios, GET /ejercicios/{id}
- **Rutinas**: CRUD /rutinas, POST/DELETE /rutinas/{id}/ejercicios
- **Entrenamientos**: GET/POST /entrenamientos, POST /entrenamientos/{id}/registros
- **Peso**: GET/POST /peso
- **Estadísticas**: GET /estadisticas/progreso, GET /estadisticas/graficas
- **Social**: POST /social/seguir/{id}, DELETE /social/dejar_de_seguir/{id}, GET /social/siguiendo, GET /social/clasificacion
- **Desafíos**: GET /desafios, POST /desafios/{id}/unirse, GET /desafios/{id}/mi_progreso

Todas las rutas excepto auth requieren cabecera: `Authorization: Bearer <token>`
