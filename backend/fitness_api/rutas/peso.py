from flask import Blueprint, request, jsonify
from datetime import datetime
from fitness_api.extensiones import db
from fitness_api.modelos.seguimiento_peso import SeguimientoPeso
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("peso", __name__, url_prefix="/peso")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def obtener_historial():
    registros = SeguimientoPeso.query.filter_by(id_usuario=request.usuario_actual_id).order_by(
        SeguimientoPeso.fecha.desc()
    ).all()
    return jsonify([r.a_dict() for r in registros])


@bp.route("", methods=["POST"])
@requerir_autenticacion
def registrar_peso():
    datos = request.get_json()
    if not datos or "fecha" not in datos or "peso_kg" not in datos:
        return jsonify({"error": "fecha y peso_kg requeridos"}), 400

    fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()

    sp = SeguimientoPeso(
        id_usuario=request.usuario_actual_id,
        fecha=fecha,
        peso_kg=float(datos["peso_kg"]),
        notas=datos.get("notas"),
    )
    db.session.add(sp)
    db.session.commit()
    return jsonify(sp.a_dict()), 201
