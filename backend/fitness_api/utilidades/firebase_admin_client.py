import json
import os

import firebase_admin
from firebase_admin import auth, credentials

_firebase_app = None


def obtener_firebase_app():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    valor = os.environ.get(
        "FIREBASE_ADMINSDK_JSON",
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "firebase-adminsdk.json"),
    )

    if valor.strip().startswith("{"):
        cred = credentials.Certificate(json.loads(valor))
    elif os.path.exists(valor):
        cred = credentials.Certificate(valor)
    else:
        raise RuntimeError("FIREBASE_ADMINSDK_JSON no configurado: ruta inexistente o JSON invalido")

    _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app


def verificar_id_token(id_token):
    obtener_firebase_app()
    return auth.verify_id_token(id_token)
