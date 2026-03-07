from datetime import datetime
from fitness_api.extensiones import db


class Rutina(db.Model):
    __tablename__ = "rutina"

    id_rutina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    nombre_rutina = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    objetivo_rutina = db.Column(db.String(80), nullable=True)
    dias_semana = db.Column(db.Integer, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)

    ejercicios = db.relationship("RutinaEjercicio", back_populates="rutina", cascade="all, delete-orphan")

    def a_dict(self, incluir_ejercicios=False):
        d = {
            "id_rutina": self.id_rutina,
            "id_usuario": self.id_usuario,
            "nombre_rutina": self.nombre_rutina,
            "descripcion": self.descripcion,
            "objetivo_rutina": self.objetivo_rutina,
            "dias_semana": self.dias_semana,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "activa": self.activa,
        }
        if incluir_ejercicios:
            d["ejercicios"] = [e.a_dict() for e in self.ejercicios]
        return d


class RutinaEjercicio(db.Model):
    __tablename__ = "rutina_ejercicio"

    id_rutina_ejercicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_rutina = db.Column(db.Integer, db.ForeignKey("rutina.id_rutina"), nullable=False)
    id_ejercicio = db.Column(db.Integer, db.ForeignKey("ejercicio.id_ejercicio"), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=True)
    orden = db.Column(db.Integer, nullable=True)
    series = db.Column(db.Integer, nullable=True)
    repeticiones = db.Column(db.Integer, nullable=True)
    descanso_segundos = db.Column(db.Integer, nullable=True)
    notas = db.Column(db.Text, nullable=True)

    rutina = db.relationship("Rutina", back_populates="ejercicios")
    ejercicio = db.relationship("Ejercicio", backref="rutinas_asociadas")

    def a_dict(self):
        d = {
            "id_rutina_ejercicio": self.id_rutina_ejercicio,
            "id_rutina": self.id_rutina,
            "id_ejercicio": self.id_ejercicio,
            "dia_semana": self.dia_semana,
            "orden": self.orden,
            "series": self.series,
            "repeticiones": self.repeticiones,
            "descanso_segundos": self.descanso_segundos,
            "notas": self.notas,
        }
        if self.ejercicio:
            d["ejercicio"] = self.ejercicio.a_dict()
        return d
