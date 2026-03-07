from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from fitness_api.extensiones import db
from fitness_api.modelos.entrenamiento import Entrenamiento, RegistroEjercicio
from fitness_api.modelos.seguimiento_peso import SeguimientoPeso
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.route("/progreso", methods=["GET"])
@requerir_autenticacion
def obtener_progreso():
    usuario_id = request.usuario_actual_id

    total_entrenamientos = Entrenamiento.query.filter_by(id_usuario=usuario_id).count()

    hace_30 = datetime.utcnow().date() - timedelta(days=30)
    entrenamientos_ultimo_mes = Entrenamiento.query.filter(
        Entrenamiento.id_usuario == usuario_id,
        Entrenamiento.fecha >= hace_30
    ).count()

    volumen = db.session.query(
        func.sum(RegistroEjercicio.repeticiones_realizadas * func.coalesce(RegistroEjercicio.peso_usado, 1))
    ).join(Entrenamiento).filter(Entrenamiento.id_usuario == usuario_id).scalar() or 0

    return jsonify({
        "total_entrenamientos": total_entrenamientos,
        "entrenamientos_ultimo_mes": entrenamientos_ultimo_mes,
        "volumen_total": float(volumen),
    })


@bp.route("/graficas", methods=["GET"])
@requerir_autenticacion
def obtener_datos_graficas():
    usuario_id = request.usuario_actual_id

    peso_registros = SeguimientoPeso.query.filter_by(id_usuario=usuario_id).order_by(
        SeguimientoPeso.fecha
    ).all()

    entrenamientos = Entrenamiento.query.filter_by(id_usuario=usuario_id).order_by(
        Entrenamiento.fecha
    ).all()

    return jsonify({
        "peso": [{"fecha": r.fecha.isoformat(), "peso_kg": r.peso_kg} for r in peso_registros],
        "entrenamientos_por_fecha": [{"fecha": e.fecha.isoformat(), "duracion_minutos": e.duracion_minutos} for e in entrenamientos],
    })
