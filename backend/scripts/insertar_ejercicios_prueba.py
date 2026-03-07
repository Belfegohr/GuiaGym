import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fitness_api.app import aplicacion as app
from fitness_api.extensiones import db
from fitness_api.modelos.ejercicio import Ejercicio

ejercicios = [
    {"nombre": "Press banca", "descripcion": "Tumbado, empujar la barra hacia arriba", "grupo_muscular": "Pecho", "tipo_equipo": "Barra", "dificultad": "Intermedio", "url_video": ""},
    {"nombre": "Sentadilla", "descripcion": "Bajar flexionando rodillas manteniendo espalda recta", "grupo_muscular": "Piernas", "tipo_equipo": "Barra", "dificultad": "Intermedio", "url_video": ""},
    {"nombre": "Peso muerto", "descripcion": "Levantar la barra desde el suelo con espalda recta", "grupo_muscular": "Espalda", "tipo_equipo": "Barra", "dificultad": "Intermedio", "url_video": ""},
    {"nombre": "Dominadas", "descripcion": "Colgado de una barra, subir hasta que la barbilla pase la barra", "grupo_muscular": "Espalda", "tipo_equipo": "Peso corporal", "dificultad": "Principiante", "url_video": ""},
    {"nombre": "Curl bíceps", "descripcion": "Flexionar el brazo levantando la mancuerna", "grupo_muscular": "Bíceps", "tipo_equipo": "Mancuerna", "dificultad": "Principiante", "url_video": ""},
]

with app.app_context():
    for e in ejercicios:
        if not Ejercicio.query.filter_by(nombre=e["nombre"]).first():
            ej = Ejercicio(**e)
            db.session.add(ej)
    db.session.commit()
    print("Ejercicios de prueba insertados.")
