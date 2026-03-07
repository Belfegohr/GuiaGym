from flask import Blueprint, request, jsonify
from datetime import datetime
from fitness_api.extensiones import db
from fitness_api.modelos.entrenamiento import Entrenamiento, RegistroEjercicio
from fitness_api.modelos.ejercicio import Ejercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("entrenamientos", __name__, url_prefix="/entrenamientos")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_entrenamientos():
    """Listar mis entrenamientos."""
    entrenamientos = Entrenamiento.query.filter_by(id_usuario=request.usuario_actual_id).order_by(
        Entrenamiento.fecha.desc()
    ).all()
    return jsonify([e.a_dict() for e in entrenamientos])


@bp.route("", methods=["POST"])
@requerir_autenticacion
def registrar_entrenamiento():
    """Registrar entrenamiento."""
    datos = request.get_json()
    if not datos or "fecha" not in datos:
        return jsonify({"error": "fecha requerida"}), 400

    fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
    hora_inicio = datetime.strptime(datos["hora_inicio"], "%H:%M").time() if datos.get("hora_inicio") else None
    hora_fin = datetime.strptime(datos["hora_fin"], "%H:%M").time() if datos.get("hora_fin") else None

    entrenamiento = Entrenamiento(
        id_usuario=request.usuario_actual_id,
        id_rutina=datos.get("id_rutina"),
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        duracion_minutos=datos.get("duracion_minutos"),
        notas=datos.get("notas"),
    )
    db.session.add(entrenamiento)
    db.session.commit()
    return jsonify(entrenamiento.a_dict()), 201


@bp.route("/<int:id_entrenamiento>", methods=["GET"])
@requerir_autenticacion
def obtener_entrenamiento(id_entrenamiento):
    """Ver detalle de entrenamiento."""
    e = Entrenamiento.query.filter_by(
        id_entrenamiento=id_entrenamiento,
        id_usuario=request.usuario_actual_id
    ).first()
    if not e:
        return jsonify({"error": "Entrenamiento no encontrado"}), 404
    return jsonify(e.a_dict(incluir_registros=True))


@bp.route("/<int:id_entrenamiento>/registros", methods=["POST"])
@requerir_autenticacion
def registrar_serie(id_entrenamiento):
    """Registrar series y repeticiones de un ejercicio."""
    entrenamiento = Entrenamiento.query.filter_by(
        id_entrenamiento=id_entrenamiento,
        id_usuario=request.usuario_actual_id
    ).first()
    if not entrenamiento:
        return jsonify({"error": "Entrenamiento no encontrado"}), 404

    datos = request.get_json()
    if not datos or "id_ejercicio" not in datos:
        return jsonify({"error": "id_ejercicio requerido"}), 400

    registro = RegistroEjercicio(
        id_entrenamiento=id_entrenamiento,
        id_ejercicio=datos["id_ejercicio"],
        serie_numero=datos.get("serie_numero"),
        repeticiones_realizadas=datos.get("repeticiones_realizadas"),
        peso_usado=datos.get("peso_usado"),
        completado=datos.get("completado", False),
    )
    db.session.add(registro)
    db.session.commit()
    return jsonify(registro.a_dict()), 201
