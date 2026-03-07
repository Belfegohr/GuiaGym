from flask import Blueprint, request, jsonify
from fitness_api.extensiones import db
from fitness_api.modelos.rutina import Rutina, RutinaEjercicio
from fitness_api.modelos.ejercicio import Ejercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("rutinas", __name__, url_prefix="/rutinas")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_rutinas():
    """Mis rutinas."""
    rutinas = Rutina.query.filter_by(id_usuario=request.usuario_actual_id).all()
    return jsonify([r.a_dict(incluir_ejercicios=True) for r in rutinas])


@bp.route("", methods=["POST"])
@requerir_autenticacion
def crear_rutina():
    """Crear rutina."""
    datos = request.get_json()
    if not datos or not datos.get("nombre_rutina"):
        return jsonify({"error": "nombre_rutina requerido"}), 400

    rutina = Rutina(
        id_usuario=request.usuario_actual_id,
        nombre_rutina=datos["nombre_rutina"],
        descripcion=datos.get("descripcion"),
        objetivo_rutina=datos.get("objetivo_rutina"),
        dias_semana=datos.get("dias_semana"),
    )
    db.session.add(rutina)
    db.session.commit()
    return jsonify(rutina.a_dict()), 201


@bp.route("/<int:id_rutina>", methods=["GET"])
@requerir_autenticacion
def obtener_rutina(id_rutina):
    """Ver una rutina."""
    rutina = Rutina.query.filter_by(id_rutina=id_rutina, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404
    return jsonify(rutina.a_dict(incluir_ejercicios=True))


@bp.route("/<int:id_rutina>", methods=["PUT"])
@requerir_autenticacion
def modificar_rutina(id_rutina):
    """Modificar rutina."""
    rutina = Rutina.query.filter_by(id_rutina=id_rutina, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    datos = request.get_json()
    if datos:
        if "nombre_rutina" in datos:
            rutina.nombre_rutina = datos["nombre_rutina"]
        if "descripcion" in datos:
            rutina.descripcion = datos["descripcion"]
        if "objetivo_rutina" in datos:
            rutina.objetivo_rutina = datos["objetivo_rutina"]
        if "dias_semana" in datos:
            rutina.dias_semana = datos["dias_semana"]
        if "activa" in datos:
            rutina.activa = datos["activa"]

    db.session.commit()
    return jsonify(rutina.a_dict())


@bp.route("/<int:id_rutina>", methods=["DELETE"])
@requerir_autenticacion
def borrar_rutina(id_rutina):
    """Borrar rutina."""
    rutina = Rutina.query.filter_by(id_rutina=id_rutina, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    db.session.delete(rutina)
    db.session.commit()
    return jsonify({"mensaje": "Rutina borrada"}), 200


@bp.route("/<int:id_rutina>/ejercicios", methods=["POST"])
@requerir_autenticacion
def añadir_ejercicio(id_rutina):
    """Añadir ejercicio a rutina."""
    rutina = Rutina.query.filter_by(id_rutina=id_rutina, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    datos = request.get_json()
    if not datos or "id_ejercicio" not in datos:
        return jsonify({"error": "id_ejercicio requerido"}), 400

    ejercicio = Ejercicio.query.get(datos["id_ejercicio"])
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    re = RutinaEjercicio(
        id_rutina=id_rutina,
        id_ejercicio=datos["id_ejercicio"],
        dia_semana=datos.get("dia_semana"),
        orden=datos.get("orden"),
        series=datos.get("series"),
        repeticiones=datos.get("repeticiones"),
        descanso_segundos=datos.get("descanso_segundos"),
        notas=datos.get("notas"),
    )
    db.session.add(re)
    db.session.commit()
    return jsonify(re.a_dict()), 201


@bp.route("/<int:id_rutina>/ejercicios/<int:id_ejercicio>", methods=["DELETE"])
@requerir_autenticacion
def quitar_ejercicio(id_rutina, id_ejercicio):
    """Quitar ejercicio de rutina."""
    rutina = Rutina.query.filter_by(id_rutina=id_rutina, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    re = RutinaEjercicio.query.filter_by(id_rutina=id_rutina, id_ejercicio=id_ejercicio).first()
    if not re:
        return jsonify({"error": "Ejercicio no está en la rutina"}), 404

    db.session.delete(re)
    db.session.commit()
    return jsonify({"mensaje": "Ejercicio quitado de la rutina"}), 200
