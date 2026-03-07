from datetime import datetime
from fitness_api.extensiones import db


class Entrenamiento(db.Model):
    __tablename__ = "entrenamiento"

    id_entrenamiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    id_rutina = db.Column(db.Integer, db.ForeignKey("rutina.id_rutina"), nullable=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_fin = db.Column(db.Time, nullable=True)
    duracion_minutos = db.Column(db.Integer, nullable=True)
    notas = db.Column(db.Text, nullable=True)

    registros = db.relationship("RegistroEjercicio", back_populates="entrenamiento", cascade="all, delete-orphan")

    def a_dict(self, incluir_registros=False):
        d = {
            "id_entrenamiento": self.id_entrenamiento,
            "id_usuario": self.id_usuario,
            "id_rutina": self.id_rutina,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora_inicio": self.hora_inicio.strftime("%H:%M") if self.hora_inicio else None,
            "hora_fin": self.hora_fin.strftime("%H:%M") if self.hora_fin else None,
            "duracion_minutos": self.duracion_minutos,
            "notas": self.notas,
        }
        if incluir_registros:
            d["registros"] = [r.a_dict() for r in self.registros]
        return d


class RegistroEjercicio(db.Model):
    __tablename__ = "registro_ejercicio"

    id_registro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_entrenamiento = db.Column(db.Integer, db.ForeignKey("entrenamiento.id_entrenamiento"), nullable=False)
    id_ejercicio = db.Column(db.Integer, db.ForeignKey("ejercicio.id_ejercicio"), nullable=False)
    serie_numero = db.Column(db.Integer, nullable=True)
    repeticiones_realizadas = db.Column(db.Integer, nullable=True)
    peso_usado = db.Column(db.Float, nullable=True)
    completado = db.Column(db.Boolean, default=False)

    entrenamiento = db.relationship("Entrenamiento", back_populates="registros")
    ejercicio = db.relationship("Ejercicio", backref="registros")

    def a_dict(self):
        d = {
            "id_registro": self.id_registro,
            "id_entrenamiento": self.id_entrenamiento,
            "id_ejercicio": self.id_ejercicio,
            "serie_numero": self.serie_numero,
            "repeticiones_realizadas": self.repeticiones_realizadas,
            "peso_usado": self.peso_usado,
            "completado": self.completado,
        }
        if self.ejercicio:
            d["ejercicio"] = self.ejercicio.a_dict()
        return d
