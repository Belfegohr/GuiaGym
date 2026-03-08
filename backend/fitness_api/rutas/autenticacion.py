from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from fitness_api.extensiones import db, bcrypt
from fitness_api.modelos.usuario import Usuario
from fitness_api.utilidades.seguridad import generar_token

bp = Blueprint("autenticacion", __name__, url_prefix="/auth")


@bp.route("/registro", methods=["POST"])
def registro():
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


@bp.route("/renovar", methods=["POST"])
def renovar():
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
