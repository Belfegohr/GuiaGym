from datetime import datetime

from fitness_api.utilidades.firebase_admin_client import obtener_firebase_app

from firebase_admin import firestore


def obtener_firestore():
    app = obtener_firebase_app()
    return firestore.client(app=app)


def _coleccion_usuarios():
    return obtener_firestore().collection("usuarios")


def _normalizar_usuario(doc_id, data):
    return {
        "id_usuario": doc_id,
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "fecha_nacimiento": data.get("fecha_nacimiento"),
        "genero": data.get("genero"),
        "altura": data.get("altura"),
        "peso_actual": data.get("peso_actual"),
        "objetivo": data.get("objetivo"),
        "nivel_experiencia": data.get("nivel_experiencia"),
        "fecha_registro": data.get("fecha_registro"),
    }


def obtener_usuario_por_uid(uid):
    doc = _coleccion_usuarios().document(uid).get()
    if not doc.exists:
        return None
    return _normalizar_usuario(doc.id, doc.to_dict() or {})


def obtener_usuario_por_email(email):
    resultados = _coleccion_usuarios().where("email", "==", email).limit(1).stream()
    for doc in resultados:
        return _normalizar_usuario(doc.id, doc.to_dict() or {})
    return None


def crear_o_actualizar_usuario(uid, datos):
    payload = {
        "nombre": datos.get("nombre"),
        "email": datos.get("email"),
        "fecha_nacimiento": datos.get("fecha_nacimiento"),
        "genero": datos.get("genero"),
        "altura": datos.get("altura"),
        "peso_actual": datos.get("peso_actual"),
        "objetivo": datos.get("objetivo"),
        "nivel_experiencia": datos.get("nivel_experiencia"),
        "fecha_registro": datos.get("fecha_registro") or datetime.utcnow().isoformat(),
    }
    _coleccion_usuarios().document(uid).set(payload, merge=True)
    return obtener_usuario_por_uid(uid)


def actualizar_usuario(uid, datos):
    permitidos = {
        "nombre",
        "fecha_nacimiento",
        "genero",
        "altura",
        "peso_actual",
        "objetivo",
        "nivel_experiencia",
    }
    payload = {k: v for k, v in datos.items() if k in permitidos}
    if not payload:
        return obtener_usuario_por_uid(uid)
    _coleccion_usuarios().document(uid).set(payload, merge=True)
    return obtener_usuario_por_uid(uid)
