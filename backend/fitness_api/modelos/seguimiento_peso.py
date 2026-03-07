from datetime import datetime
from fitness_api.extensiones import db


class SeguimientoPeso(db.Model):
    __tablename__ = "seguimiento_peso"

    id_seguimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    peso_kg = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text, nullable=True)

    def a_dict(self):
        return {
            "id_seguimiento": self.id_seguimiento,
            "id_usuario": self.id_usuario,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "peso_kg": self.peso_kg,
            "notas": self.notas,
        }
