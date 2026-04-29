from flask import Blueprint, request, jsonify
from fitness_api.extensiones import db, bcrypt
from fitness_api.modelos.usuario import Usuario
from fitness_api.utilidades.firebase_admin_client import verificar_id_token
from fitness_api.utilidades.firestore_repo import crear_o_actualizar_usuario

bp = Blueprint("autenticacion", __name__, url_prefix="/auth")


@bp.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    id_token = datos.get("id_token")
    if not id_token:
        return jsonify({"error": "id_token de Firebase requerido"}), 400

    try:
        decoded = verificar_id_token(id_token)
    except Exception as e:
        return jsonify({"error": "Token de Firebase invalido", "detalle": str(e)}), 401

    email = decoded.get("email")
    uid = decoded.get("uid")
    nombre = datos.get("nombre") or decoded.get("name") or (email.split("@")[0] if email else None)

    if not email or not uid:
        return jsonify({"error": "El token de Firebase debe contener uid y email"}), 400

    usuario = Usuario(
        nombre=(nombre or "usuario")[:100],
        email=email,
        fecha_nacimiento=None,
        genero=datos.get("genero"),
        altura=float(datos["altura"]) if datos.get("altura") else None,
        peso_actual=float(datos["peso_actual"]) if datos.get("peso_actual") else None,
        objetivo=datos.get("objetivo"),
        nivel_experiencia=datos.get("nivel_experiencia"),
    )
    existente = Usuario.query.filter_by(email=email).first()
    if existente:
        usuario = existente
    else:
        usuario.establecer_contraseña(uid)
        db.session.add(usuario)
        db.session.commit()

    usuario_firestore = crear_o_actualizar_usuario(
        uid=uid,
        datos={
            "nombre": usuario.nombre,
            "email": usuario.email,
            "genero": usuario.genero,
            "altura": usuario.altura,
            "peso_actual": usuario.peso_actual,
            "objetivo": usuario.objetivo,
            "nivel_experiencia": usuario.nivel_experiencia,
        },
    )

    return jsonify({
        "mensaje": "Usuario sincronizado con Firebase",
        "token": id_token,
        "usuario": usuario_firestore
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    id_token = datos.get("id_token")
    if not id_token:
        return jsonify({"error": "id_token de Firebase requerido"}), 400

    try:
        decoded = verificar_id_token(id_token)
    except Exception as e:
        return jsonify({"error": "Token de Firebase invalido", "detalle": str(e)}), 401

    email = decoded.get("email")
    uid = decoded.get("uid")
    if not email or not uid:
        return jsonify({"error": "El token de Firebase debe contener uid y email"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(
            nombre=(decoded.get("name") or email.split("@")[0])[:100],
            email=email,
            objetivo=None,
            nivel_experiencia=None,
        )
        usuario.contraseña = bcrypt.generate_password_hash(decoded.get("uid", "firebase_user")).decode("utf-8")
        db.session.add(usuario)
        db.session.commit()

    usuario_firestore = crear_o_actualizar_usuario(
        uid=uid,
        datos={
            "nombre": usuario.nombre,
            "email": usuario.email,
            "genero": usuario.genero,
            "altura": usuario.altura,
            "peso_actual": usuario.peso_actual,
            "objetivo": usuario.objetivo,
            "nivel_experiencia": usuario.nivel_experiencia,
        },
    )

    return jsonify({
        "token": id_token,
        "proveedor": "firebase",
        "usuario": usuario_firestore
    })


@bp.route("/renovar", methods=["POST"])
def renovar():
    return jsonify({
        "mensaje": "Con Firebase, la renovacion de token se hace en el cliente (SDK Firebase)."
    }), 400
