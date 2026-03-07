from datetime import datetime
from fitness_api.extensiones import db


class Seguidor(db.Model):
    __tablename__ = "seguidor"

    id_seguidor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario_seguidor = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_seguido = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("id_usuario_seguidor", "id_usuario_seguido", name="uq_seguidor_seguido"),
    )
