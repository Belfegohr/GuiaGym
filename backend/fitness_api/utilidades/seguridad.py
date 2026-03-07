from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta


def generar_token(usuario_id, secret_key, horas=24):
    payload = {
        "usuario_id": usuario_id,
        "exp": datetime.utcnow() + timedelta(hours=horas)
    }
    t = jwt.encode(payload, secret_key, algorithm="HS256")
    return t if isinstance(t, str) else t.decode("utf-8")


def decodificar_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload.get("usuario_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def requerir_autenticacion(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token requerido"}), 401
        token = auth_header.split(" ")[1]
        from flask import current_app
        usuario_id = decodificar_token(token, current_app.config["JWT_SECRET_KEY"])
        if not usuario_id:
            return jsonify({"error": "Token invalido o expirado"}), 401
        request.usuario_actual_id = usuario_id
        return f(*args, **kwargs)
    return decorador
