from flask import Blueprint, request, jsonify
from fitness_api.extensiones import db
from fitness_api.modelos.rutina import Rutina, RutinaEjercicio
from fitness_api.modelos.ejercicio import Ejercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion
from fitness_api.utilidades.firestore_training_repo import (
    listar_rutinas_usuario as fs_listar_rutinas_usuario,
    crear_rutina as fs_crear_rutina,
    obtener_rutina as fs_obtener_rutina,
    actualizar_rutina as fs_actualizar_rutina,
    borrar_rutina as fs_borrar_rutina,
    anadir_ejercicio_rutina as fs_anadir_ejercicio_rutina,
    quitar_ejercicio_rutina as fs_quitar_ejercicio_rutina,
)

bp = Blueprint("rutinas", __name__, url_prefix="/rutinas")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_rutinas():
    rutinas_fs = fs_listar_rutinas_usuario(request.firebase_uid)
    if rutinas_fs:
        return jsonify(rutinas_fs)
    rutinas = Rutina.query.filter_by(id_usuario=request.usuario_actual_id).all()
    return jsonify([r.a_dict(incluir_ejercicios=True) for r in rutinas])


@bp.route("", methods=["POST"])
@requerir_autenticacion
def crear_rutina():
    datos = request.get_json()
    if not datos or not datos.get("nombre_rutina"):
        return jsonify({"error": "nombre_rutina requerido"}), 400

    rutina_fs = fs_crear_rutina(request.firebase_uid, datos)

    rutina = Rutina(
        id_usuario=request.usuario_actual_id,
        nombre_rutina=datos["nombre_rutina"],
        descripcion=datos.get("descripcion"),
        objetivo_rutina=datos.get("objetivo_rutina"),
        dias_semana=datos.get("dias_semana"),
    )
    db.session.add(rutina)
    db.session.commit()
    return jsonify(rutina_fs), 201


@bp.route("/<id_rutina>", methods=["GET"])
@requerir_autenticacion
def obtener_rutina(id_rutina):
    rutina_fs = fs_obtener_rutina(request.firebase_uid, id_rutina)
    if rutina_fs:
        return jsonify(rutina_fs)

    if not str(id_rutina).isdigit():
        return jsonify({"error": "Rutina no encontrada"}), 404
    id_rutina_int = int(id_rutina)
    rutina = Rutina.query.filter_by(id_rutina=id_rutina_int, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404
    return jsonify(rutina.a_dict(incluir_ejercicios=True))


@bp.route("/<id_rutina>", methods=["PUT"])
@requerir_autenticacion
def modificar_rutina(id_rutina):
    datos = request.get_json()
    rutina_fs = fs_actualizar_rutina(request.firebase_uid, id_rutina, datos or {})
    if rutina_fs:
        return jsonify(rutina_fs)

    if not str(id_rutina).isdigit():
        return jsonify({"error": "Rutina no encontrada"}), 404
    id_rutina_int = int(id_rutina)
    rutina = Rutina.query.filter_by(id_rutina=id_rutina_int, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

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


@bp.route("/<id_rutina>", methods=["DELETE"])
@requerir_autenticacion
def borrar_rutina(id_rutina):
    borrada_fs = fs_borrar_rutina(request.firebase_uid, id_rutina)
    if borrada_fs:
        return jsonify({"mensaje": "Rutina borrada"}), 200

    if not str(id_rutina).isdigit():
        return jsonify({"error": "Rutina no encontrada"}), 404
    id_rutina_int = int(id_rutina)
    rutina = Rutina.query.filter_by(id_rutina=id_rutina_int, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    db.session.delete(rutina)
    db.session.commit()
    return jsonify({"mensaje": "Rutina borrada"}), 200


@bp.route("/<id_rutina>/ejercicios", methods=["POST"])
@requerir_autenticacion
def añadir_ejercicio(id_rutina):
    datos = request.get_json()
    if not datos or "id_ejercicio" not in datos:
        return jsonify({"error": "id_ejercicio requerido"}), 400

    ejercicio = Ejercicio.query.get(datos["id_ejercicio"])
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    rutina_fs = fs_obtener_rutina(request.firebase_uid, id_rutina)
    if rutina_fs:
        re_fs = fs_anadir_ejercicio_rutina(request.firebase_uid, id_rutina, datos)
        if not re_fs:
            return jsonify({"error": "Rutina no encontrada"}), 404
        re_fs["ejercicio"] = ejercicio.a_dict()
        return jsonify(re_fs), 201

    if not str(id_rutina).isdigit():
        return jsonify({"error": "Rutina no encontrada"}), 404
    id_rutina_int = int(id_rutina)
    rutina = Rutina.query.filter_by(id_rutina=id_rutina_int, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    re = RutinaEjercicio(
        id_rutina=id_rutina_int,
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


@bp.route("/<id_rutina>/ejercicios/<id_ejercicio>", methods=["DELETE"])
@requerir_autenticacion
def quitar_ejercicio(id_rutina, id_ejercicio):
    resultado_fs = fs_quitar_ejercicio_rutina(request.firebase_uid, id_rutina, id_ejercicio)
    if resultado_fs is True:
        return jsonify({"mensaje": "Ejercicio quitado de la rutina"}), 200
    if resultado_fs is False:
        return jsonify({"error": "Ejercicio no está en la rutina"}), 404

    if not str(id_rutina).isdigit() or not str(id_ejercicio).isdigit():
        return jsonify({"error": "Rutina no encontrada"}), 404
    id_rutina_int = int(id_rutina)
    id_ejercicio_int = int(id_ejercicio)
    rutina = Rutina.query.filter_by(id_rutina=id_rutina_int, id_usuario=request.usuario_actual_id).first()
    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    re = RutinaEjercicio.query.filter_by(id_rutina=id_rutina_int, id_ejercicio=id_ejercicio_int).first()
    if not re:
        return jsonify({"error": "Ejercicio no está en la rutina"}), 404

    db.session.delete(re)
    db.session.commit()
    return jsonify({"mensaje": "Ejercicio quitado de la rutina"}), 200
