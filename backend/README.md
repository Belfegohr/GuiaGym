# API Fitness App - Backend

API REST en Python (Flask) para la app de rutinas de ejercicios. Tecnologías: Python, MySQL, SQLAlchemy, JWT, bcrypt.

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
