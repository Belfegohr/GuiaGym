import os

class Configuracion:
    """Variables de configuracion de la API."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_secreta_cambiar_en_produccion")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///fitness_app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_EXPIRACION_HORAS = 24
