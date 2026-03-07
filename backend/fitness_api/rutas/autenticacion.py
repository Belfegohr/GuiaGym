import os
import secrets
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from fitness_api.extensiones import db, bcrypt
from fitness_api.modelos.usuario import Usuario
from fitness_api.utilidades.seguridad import generar_token

bp = Blueprint("autenticacion", __name__, url_prefix="/auth")

_firebase_app = None


def _obtener_firebase():
    """Inicializa Firebase Admin SDK una sola vez.
    Soporta FIREBASE_ADMINSDK_JSON como:
    - Ruta a archivo .json
    - JSON string (para Secret Manager en Cloud Run)
    """
    global _firebase_app
    if _firebase_app is None:
        import json
        import firebase_admin
        from firebase_admin import credentials
        valor = os.environ.get(
            "FIREBASE_ADMINSDK_JSON",
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "firebase-adminsdk.json")
        )
        if valor.strip().startswith("{"):
            cred = credentials.Certificate(json.loads(valor))
        elif os.path.exists(valor):
            cred = credentials.Certificate(valor)
        else:
            raise RuntimeError("FIREBASE_ADMINSDK_JSON no configurado: ruta inexistente o JSON inválido")
        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app


@bp.route("/registro", methods=["POST"])
def registro():
    """Registrar nuevo usuario."""
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    email = datos.get("email")
    contraseña = datos.get("contraseña")
    nombre = datos.get("nombre")

    if not email or not contraseña or not nombre:
        return jsonify({"error": "Faltan email, contraseña o nombre"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    fecha_nac = None
    if datos.get("fecha_nacimiento"):
        try:
            fecha_nac = datetime.strptime(datos["fecha_nacimiento"], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            pass

    usuario = Usuario(
        nombre=nombre,
        email=email,
        fecha_nacimiento=fecha_nac,
        genero=datos.get("genero"),
        altura=float(datos["altura"]) if datos.get("altura") else None,
        peso_actual=float(datos["peso_actual"]) if datos.get("peso_actual") else None,
        objetivo=datos.get("objetivo"),
        nivel_experiencia=datos.get("nivel_experiencia"),
    )
    usuario.establecer_contraseña(contraseña)
    db.session.add(usuario)
    db.session.commit()

    token = generar_token(usuario.id_usuario, current_app.config["JWT_SECRET_KEY"])
    return jsonify({
        "mensaje": "Usuario creado",
        "token": token,
        "usuario": usuario.a_dict()
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    """Iniciar sesión. Devuelve token JWT."""
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    email = datos.get("email")
    contraseña = datos.get("contraseña")

    if not email or not contraseña:
        return jsonify({"error": "Email y contraseña requeridos"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_contraseña(contraseña):
        return jsonify({"error": "Email o contraseña incorrectos"}), 401

    token = generar_token(usuario.id_usuario, current_app.config["JWT_SECRET_KEY"])
    return jsonify({
        "token": token,
        "usuario": usuario.a_dict()
    })


@bp.route("/google", methods=["POST"])
def login_google():
    """Iniciar sesión con Google. Recibe id_token de Firebase Auth y devuelve JWT de la app."""
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    id_token = datos.get("id_token")
    if not id_token:
        return jsonify({"error": "id_token requerido"}), 400

    try:
        _obtener_firebase()
        from firebase_admin import auth
        decoded = auth.verify_id_token(id_token)
    except Exception as e:
        return jsonify({"error": "Token de Google inválido", "detalle": str(e)}), 401

    email = decoded.get("email")
    nombre = decoded.get("name") or decoded.get("email", "").split("@")[0]

    if not email:
        return jsonify({"error": "El token no contiene email"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(
            nombre=nombre,
            email=email,
            objetivo=None,
            nivel_experiencia=None,
        )
        usuario.contraseña = bcrypt.generate_password_hash(secrets.token_urlsafe(32)).decode("utf-8")
        db.session.add(usuario)
        db.session.commit()

    token = generar_token(usuario.id_usuario, current_app.config["JWT_SECRET_KEY"])
    return jsonify({
        "token": token,
        "usuario": usuario.a_dict()
    })


@bp.route("/renovar", methods=["POST"])
def renovar():
    """Renovar token. Necesita enviar el token actual en Authorization."""
    from fitness_api.utilidades.seguridad import decodificar_token

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token requerido"}), 401

    token_viejo = auth_header.split(" ")[1]
    usuario_id = decodificar_token(token_viejo, current_app.config["JWT_SECRET_KEY"])
    if not usuario_id:
        return jsonify({"error": "Token invalido o expirado"}), 401

    token_nuevo = generar_token(usuario_id, request.application.config["JWT_SECRET_KEY"])
    return jsonify({"token": token_nuevo})
