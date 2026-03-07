from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import func
from fitness_api.extensiones import db
from fitness_api.modelos.desafio import Desafio, UsuarioDesafio
from fitness_api.modelos.entrenamiento import Entrenamiento
from fitness_api.modelos.entrenamiento import RegistroEjercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("desafios", __name__, url_prefix="/desafios")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_desafios():
    """Ver desafíos activos."""
    hoy = datetime.utcnow().date()
    desafios = Desafio.query.filter(
        Desafio.fecha_inicio <= hoy,
        Desafio.fecha_fin >= hoy
    ).all()
    return jsonify([d.a_dict() for d in desafios])


@bp.route("/<int:id_desafio>/unirse", methods=["POST"])
@requerir_autenticacion
def unirse_desafio(id_desafio):
    """Unirse a un desafío."""
    desafio = Desafio.query.get(id_desafio)
    if not desafio:
        return jsonify({"error": "Desafío no encontrado"}), 404

    hoy = datetime.utcnow().date()
    if desafio.fecha_inicio > hoy or desafio.fecha_fin < hoy:
        return jsonify({"error": "El desafío no está activo"}), 400

    ud = UsuarioDesafio.query.filter_by(
        id_usuario=request.usuario_actual_id,
        id_desafio=id_desafio
    ).first()
    if ud:
        return jsonify({"mensaje": "Ya estás en este desafío"}), 200

    ud = UsuarioDesafio(id_usuario=request.usuario_actual_id, id_desafio=id_desafio)
    db.session.add(ud)
    db.session.commit()
    return jsonify({"mensaje": "Te has unido al desafío"}), 201


@bp.route("/<int:id_desafio>/mi_progreso", methods=["GET"])
@requerir_autenticacion
def mi_progreso(id_desafio):
    """Ver mi progreso en el desafío."""
    desafio = Desafio.query.get(id_desafio)
    if not desafio:
        return jsonify({"error": "Desafío no encontrado"}), 404

    ud = UsuarioDesafio.query.filter_by(
        id_usuario=request.usuario_actual_id,
        id_desafio=id_desafio
    ).first()
    if not ud:
        return jsonify({"error": "No estás en este desafío"}), 404

    # Calcular progreso real según tipo de desafío
    if desafio.tipo_objetivo == "entrenamientos":
        progreso = Entrenamiento.query.filter(
            Entrenamiento.id_usuario == request.usuario_actual_id,
            Entrenamiento.fecha >= desafio.fecha_inicio,
            Entrenamiento.fecha <= desafio.fecha_fin
        ).count()
    else:
        # volumen
        vol = db.session.query(
            func.sum(RegistroEjercicio.repeticiones_realizadas * func.coalesce(RegistroEjercicio.peso_usado, 1))
        ).join(Entrenamiento).filter(
            Entrenamiento.id_usuario == request.usuario_actual_id,
            Entrenamiento.fecha >= desafio.fecha_inicio,
            Entrenamiento.fecha <= desafio.fecha_fin
        ).scalar() or 0
        progreso = int(vol)

    return jsonify({
        "desafio": desafio.a_dict(),
        "progreso": progreso,
        "objetivo": desafio.objetivo,
        "completado": progreso >= (desafio.objetivo or 0),
    })
