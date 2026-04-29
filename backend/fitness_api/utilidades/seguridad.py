from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from fitness_api.modelos.usuario import Usuario
from fitness_api.extensiones import db
from fitness_api.utilidades.firebase_admin_client import verificar_id_token
from fitness_api.utilidades.firestore_repo import crear_o_actualizar_usuario


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
        try:
            decoded = verificar_id_token(token)
        except Exception:
            return jsonify({"error": "Token de Firebase invalido o expirado"}), 401

        email = decoded.get("email")
        uid = decoded.get("uid")
        if not email:
            return jsonify({"error": "El token no contiene email"}), 401

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario(
                nombre=(decoded.get("name") or email.split("@")[0])[:100],
                email=email,
                objetivo=None,
                nivel_experiencia=None,
            )
            # Contraseña no se usa cuando la autenticacion la hace Firebase.
            usuario.establecer_contraseña(uid or "firebase_user")
            db.session.add(usuario)
            db.session.commit()

        request.usuario_actual_id = usuario.id_usuario
        request.firebase_uid = uid
        request.firebase_email = email
        crear_o_actualizar_usuario(
            uid=uid,
            datos={
                "nombre": decoded.get("name") or usuario.nombre or email.split("@")[0],
                "email": email,
            },
        )
        return f(*args, **kwargs)
    return decorador
