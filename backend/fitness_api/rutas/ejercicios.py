from flask import Blueprint, request, jsonify
from fitness_api.modelos.ejercicio import Ejercicio
from fitness_api.utilidades.seguridad import requerir_autenticacion

bp = Blueprint("ejercicios", __name__, url_prefix="/ejercicios")


@bp.route("", methods=["GET"])
@requerir_autenticacion
def listar_ejercicios():
    """Listar ejercicios. Filtros opcionales: grupo_muscular, dificultad."""
    grupo = request.args.get("grupo_muscular")
    dificultad = request.args.get("dificultad")

    query = Ejercicio.query
    if grupo:
        query = query.filter(Ejercicio.grupo_muscular.ilike(f"%{grupo}%"))
    if dificultad:
        query = query.filter(Ejercicio.dificultad == dificultad)

    ejercicios = query.all()
    return jsonify([e.a_dict() for e in ejercicios])


@bp.route("/<int:id_ejercicio>", methods=["GET"])
@requerir_autenticacion
def obtener_ejercicio(id_ejercicio):
    """Ver detalle de un ejercicio."""
    ejercicio = Ejercicio.query.get(id_ejercicio)
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404
    return jsonify(ejercicio.a_dict())
