from datetime import datetime
import uuid

from fitness_api.utilidades.firebase_admin_client import obtener_firebase_app
from firebase_admin import firestore


def obtener_firestore():
    app = obtener_firebase_app()
    return firestore.client(app=app)


def _col_rutinas():
    return obtener_firestore().collection("rutinas")


def _col_entrenamientos():
    return obtener_firestore().collection("entrenamientos")


def _normalizar_rutina(doc_id, data):
    return {
        "id_rutina": doc_id,
        "id_usuario": data.get("id_usuario"),
        "nombre_rutina": data.get("nombre_rutina"),
        "descripcion": data.get("descripcion"),
        "objetivo_rutina": data.get("objetivo_rutina"),
        "dias_semana": data.get("dias_semana"),
        "fecha_creacion": data.get("fecha_creacion"),
        "activa": data.get("activa", True),
        "ejercicios": data.get("ejercicios", []),
    }


def listar_rutinas_usuario(uid):
    docs = _col_rutinas().where("id_usuario", "==", uid).stream()
    return [_normalizar_rutina(d.id, d.to_dict() or {}) for d in docs]


def crear_rutina(uid, datos):
    doc_ref = _col_rutinas().document()
    payload = {
        "id_usuario": uid,
        "nombre_rutina": datos["nombre_rutina"],
        "descripcion": datos.get("descripcion"),
        "objetivo_rutina": datos.get("objetivo_rutina"),
        "dias_semana": datos.get("dias_semana"),
        "fecha_creacion": datetime.utcnow().isoformat(),
        "activa": datos.get("activa", True),
        "ejercicios": [],
    }
    doc_ref.set(payload)
    return _normalizar_rutina(doc_ref.id, payload)


def obtener_rutina(uid, id_rutina):
    doc = _col_rutinas().document(str(id_rutina)).get()
    if not doc.exists:
        return None
    rutina = _normalizar_rutina(doc.id, doc.to_dict() or {})
    if rutina.get("id_usuario") != uid:
        return None
    return rutina


def actualizar_rutina(uid, id_rutina, datos):
    rutina = obtener_rutina(uid, id_rutina)
    if not rutina:
        return None
    permitidos = {"nombre_rutina", "descripcion", "objetivo_rutina", "dias_semana", "activa"}
    payload = {k: v for k, v in datos.items() if k in permitidos}
    if payload:
        _col_rutinas().document(str(id_rutina)).set(payload, merge=True)
    return obtener_rutina(uid, id_rutina)


def borrar_rutina(uid, id_rutina):
    rutina = obtener_rutina(uid, id_rutina)
    if not rutina:
        return False
    _col_rutinas().document(str(id_rutina)).delete()
    return True


def anadir_ejercicio_rutina(uid, id_rutina, datos):
    rutina = obtener_rutina(uid, id_rutina)
    if not rutina:
        return None
    ejercicios = rutina.get("ejercicios", [])
    nuevo = {
        "id_rutina_ejercicio": str(uuid.uuid4()),
        "id_rutina": str(id_rutina),
        "id_ejercicio": datos["id_ejercicio"],
        "dia_semana": datos.get("dia_semana"),
        "orden": datos.get("orden"),
        "series": datos.get("series"),
        "repeticiones": datos.get("repeticiones"),
        "descanso_segundos": datos.get("descanso_segundos"),
        "notas": datos.get("notas"),
    }
    ejercicios.append(nuevo)
    _col_rutinas().document(str(id_rutina)).set({"ejercicios": ejercicios}, merge=True)
    return nuevo


def quitar_ejercicio_rutina(uid, id_rutina, id_ejercicio):
    rutina = obtener_rutina(uid, id_rutina)
    if not rutina:
        return None
    ejercicios = rutina.get("ejercicios", [])
    restantes = [e for e in ejercicios if str(e.get("id_ejercicio")) != str(id_ejercicio)]
    if len(restantes) == len(ejercicios):
        return False
    _col_rutinas().document(str(id_rutina)).set({"ejercicios": restantes}, merge=True)
    return True


def _normalizar_entrenamiento(doc_id, data):
    return {
        "id_entrenamiento": doc_id,
        "id_usuario": data.get("id_usuario"),
        "id_rutina": data.get("id_rutina"),
        "fecha": data.get("fecha"),
        "hora_inicio": data.get("hora_inicio"),
        "hora_fin": data.get("hora_fin"),
        "duracion_minutos": data.get("duracion_minutos"),
        "notas": data.get("notas"),
        "registros": data.get("registros", []),
    }


def listar_entrenamientos_usuario(uid):
    docs = _col_entrenamientos().where("id_usuario", "==", uid).stream()
    entrenamientos = [_normalizar_entrenamiento(d.id, d.to_dict() or {}) for d in docs]
    entrenamientos.sort(key=lambda x: x.get("fecha") or "", reverse=True)
    return entrenamientos


def crear_entrenamiento(uid, datos):
    doc_ref = _col_entrenamientos().document()
    payload = {
        "id_usuario": uid,
        "id_rutina": str(datos.get("id_rutina")) if datos.get("id_rutina") is not None else None,
        "fecha": datos["fecha"],
        "hora_inicio": datos.get("hora_inicio"),
        "hora_fin": datos.get("hora_fin"),
        "duracion_minutos": datos.get("duracion_minutos"),
        "notas": datos.get("notas"),
        "registros": [],
    }
    doc_ref.set(payload)
    return _normalizar_entrenamiento(doc_ref.id, payload)


def obtener_entrenamiento(uid, id_entrenamiento):
    doc = _col_entrenamientos().document(str(id_entrenamiento)).get()
    if not doc.exists:
        return None
    e = _normalizar_entrenamiento(doc.id, doc.to_dict() or {})
    if e.get("id_usuario") != uid:
        return None
    return e


def anadir_registro_entrenamiento(uid, id_entrenamiento, datos):
    e = obtener_entrenamiento(uid, id_entrenamiento)
    if not e:
        return None
    registros = e.get("registros", [])
    nuevo = {
        "id_registro": str(uuid.uuid4()),
        "id_entrenamiento": str(id_entrenamiento),
        "id_ejercicio": datos["id_ejercicio"],
        "serie_numero": datos.get("serie_numero"),
        "repeticiones_realizadas": datos.get("repeticiones_realizadas"),
        "peso_usado": datos.get("peso_usado"),
        "completado": datos.get("completado", False),
    }
    registros.append(nuevo)
    _col_entrenamientos().document(str(id_entrenamiento)).set({"registros": registros}, merge=True)
    return nuevo
