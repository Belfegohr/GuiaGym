from flask import Blueprint, request, jsonify
from fitness_api.extensiones import db
from fitness_api.modelos.usuario import Usuario
from fitness_api.utilidades.seguridad import requerir_autenticacion
from fitness_api.utilidades.firestore_repo import (
    actualizar_usuario,
    obtener_usuario_por_uid,
)

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route("/mi_perfil", methods=["GET"])
@requerir_autenticacion
def obtener_mi_perfil():
    usuario = obtener_usuario_por_uid(request.firebase_uid)
    if usuario:
        return jsonify(usuario)

    usuario_sql = Usuario.query.get(request.usuario_actual_id)
    if not usuario_sql:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario_sql.a_dict())


@bp.route("/mi_perfil", methods=["PUT"])
@requerir_autenticacion
def actualizar_mi_perfil():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    if "altura" in datos and datos["altura"] is not None:
        datos["altura"] = float(datos["altura"])
    if "peso_actual" in datos and datos["peso_actual"] is not None:
        datos["peso_actual"] = float(datos["peso_actual"])

    usuario_firestore = actualizar_usuario(request.firebase_uid, datos)

    # Compatibilidad temporal con el resto de rutas SQL del proyecto.
    usuario_sql = Usuario.query.get(request.usuario_actual_id)
    if usuario_sql:
        if "nombre" in datos:
            usuario_sql.nombre = datos["nombre"]
        if "genero" in datos:
            usuario_sql.genero = datos["genero"]
        if "altura" in datos:
            usuario_sql.altura = datos["altura"]
        if "peso_actual" in datos:
            usuario_sql.peso_actual = datos["peso_actual"]
        if "objetivo" in datos:
            usuario_sql.objetivo = datos["objetivo"]
        if "nivel_experiencia" in datos:
            usuario_sql.nivel_experiencia = datos["nivel_experiencia"]
        db.session.commit()

    return jsonify(usuario_firestore)


@bp.route("/<id_usuario>", methods=["GET"])
@requerir_autenticacion
def obtener_perfil_publico(id_usuario):
    usuario = obtener_usuario_por_uid(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario.pop("email", None)
    return jsonify(usuario)
