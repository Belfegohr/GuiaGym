from flask import Blueprint, request, jsonify
from datetime import datetime
from fitness_api.extensiones import db
from fitness_api.modelos.usuario import Usuario
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route("/mi_perfil", methods=["GET"])
@requerir_autenticacion
def obtener_mi_perfil():
    """Ver mi perfil."""
    usuario = Usuario.query.get(request.usuario_actual_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.a_dict())


@bp.route("/mi_perfil", methods=["PUT"])
@requerir_autenticacion
def actualizar_mi_perfil():
    """Actualizar mi perfil."""
    usuario = Usuario.query.get(request.usuario_actual_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"error": "Datos requeridos"}), 400

    if "nombre" in datos:
        usuario.nombre = datos["nombre"]
    if "fecha_nacimiento" in datos:
        usuario.fecha_nacimiento = datetime.strptime(datos["fecha_nacimiento"], "%Y-%m-%d").date()
    if "genero" in datos:
        usuario.genero = datos["genero"]
    if "altura" in datos:
        usuario.altura = float(datos["altura"])
    if "peso_actual" in datos:
        usuario.peso_actual = float(datos["peso_actual"])
    if "objetivo" in datos:
        usuario.objetivo = datos["objetivo"]
    if "nivel_experiencia" in datos:
        usuario.nivel_experiencia = datos["nivel_experiencia"]
    if "contraseña" in datos and datos["contraseña"]:
        usuario.establecer_contraseña(datos["contraseña"])

    db.session.commit()
    return jsonify(usuario.a_dict())


@bp.route("/<int:id_usuario>", methods=["GET"])
@requerir_autenticacion
def obtener_perfil_publico(id_usuario):
    """Ver perfil público de otro usuario (para seguir)."""
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.a_dict(incluir_email=False))
