from flask import Blueprint, request, jsonify
from datetime import datetime
from fitness_api.extensiones import db
from fitness_api.modelos.entrenamiento import Entrenamiento, RegistroEjercicio
from fitness_api.modelos.ejercicio import Ejercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion
from fitness_api.utilidades.firestore_training_repo import (
    listar_entrenamientos_usuario as fs_listar_entrenamientos_usuario,
    crear_entrenamiento as fs_crear_entrenamiento,
    obtener_entrenamiento as fs_obtener_entrenamiento,
    anadir_registro_entrenamiento as fs_anadir_registro_entrenamiento,
)

bp = Blueprint("entrenamientos", __name__, url_prefix="/entrenamientos")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_entrenamientos():
    entrenamientos_fs = fs_listar_entrenamientos_usuario(request.firebase_uid)
    if entrenamientos_fs:
        return jsonify(entrenamientos_fs)
    entrenamientos = Entrenamiento.query.filter_by(id_usuario=request.usuario_actual_id).order_by(
        Entrenamiento.fecha.desc()
    ).all()
    return jsonify([e.a_dict() for e in entrenamientos])


@bp.route("", methods=["POST"])
@requerir_autenticacion
def registrar_entrenamiento():
    datos = request.get_json()
    if not datos or "fecha" not in datos:
        return jsonify({"error": "fecha requerida"}), 400

    try:
        fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "fecha invalida, formato esperado YYYY-MM-DD"}), 400
    hora_inicio = datetime.strptime(datos["hora_inicio"], "%H:%M").time() if datos.get("hora_inicio") else None
    hora_fin = datetime.strptime(datos["hora_fin"], "%H:%M").time() if datos.get("hora_fin") else None

    entrenamiento_fs = fs_crear_entrenamiento(
        request.firebase_uid,
        {
            "id_rutina": datos.get("id_rutina"),
            "fecha": datos["fecha"],
            "hora_inicio": datos.get("hora_inicio"),
            "hora_fin": datos.get("hora_fin"),
            "duracion_minutos": datos.get("duracion_minutos"),
            "notas": datos.get("notas"),
        },
    )

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
    return jsonify(entrenamiento_fs), 201


@bp.route("/<id_entrenamiento>", methods=["GET"])
@requerir_autenticacion
def obtener_entrenamiento(id_entrenamiento):
    e_fs = fs_obtener_entrenamiento(request.firebase_uid, id_entrenamiento)
    if e_fs:
        return jsonify(e_fs)

    if not str(id_entrenamiento).isdigit():
        return jsonify({"error": "Entrenamiento no encontrado"}), 404
    id_entrenamiento_int = int(id_entrenamiento)
    e = Entrenamiento.query.filter_by(
        id_entrenamiento=id_entrenamiento_int,
        id_usuario=request.usuario_actual_id
    ).first()
    if not e:
        return jsonify({"error": "Entrenamiento no encontrado"}), 404
    return jsonify(e.a_dict(incluir_registros=True))


@bp.route("/<id_entrenamiento>/registros", methods=["POST"])
@requerir_autenticacion
def registrar_serie(id_entrenamiento):
    datos = request.get_json()
    if not datos or "id_ejercicio" not in datos:
        return jsonify({"error": "id_ejercicio requerido"}), 400

    ejercicio = Ejercicio.query.get(datos["id_ejercicio"])
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    e_fs = fs_obtener_entrenamiento(request.firebase_uid, id_entrenamiento)
    if e_fs:
        registro_fs = fs_anadir_registro_entrenamiento(request.firebase_uid, id_entrenamiento, datos)
        if not registro_fs:
            return jsonify({"error": "Entrenamiento no encontrado"}), 404
        registro_fs["ejercicio"] = ejercicio.a_dict()
        return jsonify(registro_fs), 201

    if not str(id_entrenamiento).isdigit():
        return jsonify({"error": "Entrenamiento no encontrado"}), 404
    id_entrenamiento_int = int(id_entrenamiento)
    entrenamiento = Entrenamiento.query.filter_by(
        id_entrenamiento=id_entrenamiento_int,
        id_usuario=request.usuario_actual_id
    ).first()
    if not entrenamiento:
        return jsonify({"error": "Entrenamiento no encontrado"}), 404

    registro = RegistroEjercicio(
        id_entrenamiento=id_entrenamiento_int,
        id_ejercicio=datos["id_ejercicio"],
        serie_numero=datos.get("serie_numero"),
        repeticiones_realizadas=datos.get("repeticiones_realizadas"),
        peso_usado=datos.get("peso_usado"),
        completado=datos.get("completado", False),
    )
    db.session.add(registro)
    db.session.commit()
    return jsonify(registro.a_dict()), 201
