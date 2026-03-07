from datetime import datetime
from fitness_api.extensiones import db


class Desafio(db.Model):
    __tablename__ = "desafio"

    id_desafio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    objetivo = db.Column(db.Integer, nullable=True)
    tipo_objetivo = db.Column(db.String(50), nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)

    def a_dict(self):
        return {
            "id_desafio": self.id_desafio,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "objetivo": self.objetivo,
            "tipo_objetivo": self.tipo_objetivo,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
        }


class UsuarioDesafio(db.Model):
    __tablename__ = "usuario_desafio"

    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), primary_key=True)
    id_desafio = db.Column(db.Integer, db.ForeignKey("desafio.id_desafio"), primary_key=True)
    progreso = db.Column(db.Integer, default=0)
    completado = db.Column(db.Boolean, default=False)
