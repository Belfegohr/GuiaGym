from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from fitness_api.extensiones import db
from fitness_api.modelos.usuario import Usuario
from fitness_api.modelos.social import Seguidor
from fitness_api.modelos.entrenamiento import Entrenamiento
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("social", __name__, url_prefix="/social")


@bp.route("/seguir/<int:id_usuario>", methods=["POST"])
@requerir_autenticacion
def seguir_usuario(id_usuario):
    """Seguir a un usuario."""
    if id_usuario == request.usuario_actual_id:
        return jsonify({"error": "No puedes seguirte a ti mismo"}), 400

    if not Usuario.query.get(id_usuario):
        return jsonify({"error": "Usuario no encontrado"}), 404

    existente = Seguidor.query.filter_by(
        id_usuario_seguidor=request.usuario_actual_id,
        id_usuario_seguido=id_usuario
    ).first()
    if existente:
        return jsonify({"mensaje": "Ya sigues a este usuario"}), 200

    seg = Seguidor(
        id_usuario_seguidor=request.usuario_actual_id,
        id_usuario_seguido=id_usuario,
    )
    db.session.add(seg)
    db.session.commit()
    return jsonify({"mensaje": "Usuario seguido"}), 201


@bp.route("/dejar_de_seguir/<int:id_usuario>", methods=["DELETE"])
@requerir_autenticacion
def dejar_de_seguir(id_usuario):
    """Dejar de seguir."""
    seg = Seguidor.query.filter_by(
        id_usuario_seguidor=request.usuario_actual_id,
        id_usuario_seguido=id_usuario
    ).first()
    if not seg:
        return jsonify({"error": "No sigues a este usuario"}), 404

    db.session.delete(seg)
    db.session.commit()
    return jsonify({"mensaje": "Dejado de seguir"}), 200


@bp.route("/siguiendo", methods=["GET"])
@requerir_autenticacion
def listar_siguiendo():
    """Ver a quién sigo y su actividad reciente."""
    siguiendo = Seguidor.query.filter_by(id_usuario_seguidor=request.usuario_actual_id).all()
    ids_seguidos = [s.id_usuario_seguido for s in siguiendo]

    resultado = []
    hace_7 = datetime.utcnow().date() - timedelta(days=7)

    for seg in siguiendo:
        usuario = Usuario.query.get(seg.id_usuario_seguido)
        if not usuario:
            continue
        entrenamientos_recientes = Entrenamiento.query.filter(
            Entrenamiento.id_usuario == usuario.id_usuario,
            Entrenamiento.fecha >= hace_7
        ).order_by(Entrenamiento.fecha.desc()).limit(5).all()

        resultado.append({
            "usuario": usuario.a_dict(incluir_email=False),
            "actividad_reciente": [e.a_dict() for e in entrenamientos_recientes],
        })

    return jsonify(resultado)


@bp.route("/clasificacion", methods=["GET"])
@requerir_autenticacion
def obtener_clasificacion():
    """Rankings: por días entrenados y por volumen."""
    tipo = request.args.get("tipo", "dias")  # "dias" o "volumen"

    if tipo == "dias":
        ranking = db.session.query(
            Usuario.id_usuario,
            Usuario.nombre,
            func.count(Entrenamiento.id_entrenamiento).label("total")
        ).outerjoin(Entrenamiento, Usuario.id_usuario == Entrenamiento.id_usuario).group_by(
            Usuario.id_usuario
        ).order_by(func.count(Entrenamiento.id_entrenamiento).desc()).limit(20).all()

        return jsonify([
            {"posicion": i + 1, "id_usuario": r.id_usuario, "nombre": r.nombre, "dias_entrenados": r.total}
            for i, r in enumerate(ranking)
        ])

    # Por volumen (simplificado: suma de repeticiones * peso)
    from fitness_api.modelos.entrenamiento import RegistroEjercicio
    volumen_q = db.session.query(
        Usuario.id_usuario,
        Usuario.nombre,
        func.sum(RegistroEjercicio.repeticiones_realizadas * func.coalesce(RegistroEjercicio.peso_usado, 1)).label("vol")
    ).join(Entrenamiento, Usuario.id_usuario == Entrenamiento.id_usuario).join(
        RegistroEjercicio, Entrenamiento.id_entrenamiento == RegistroEjercicio.id_entrenamiento
    ).group_by(Usuario.id_usuario).order_by(func.sum(
        RegistroEjercicio.repeticiones_realizadas * func.coalesce(RegistroEjercicio.peso_usado, 1)
    ).desc()).limit(20).all()

    return jsonify([
        {"posicion": i + 1, "id_usuario": r.id_usuario, "nombre": r.nombre, "volumen": float(r.vol or 0)}
        for i, r in enumerate(volumen_q)
    ])
