from fitness_api.extensiones import db


class Ejercicio(db.Model):
    __tablename__ = "ejercicio"

    id_ejercicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    grupo_muscular = db.Column(db.String(80), nullable=True)
    tipo_equipo = db.Column(db.String(80), nullable=True)
    dificultad = db.Column(db.String(30), nullable=True)
    url_video = db.Column(db.String(500), nullable=True)

    def a_dict(self):
        return {
            "id_ejercicio": self.id_ejercicio,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "grupo_muscular": self.grupo_muscular,
            "tipo_equipo": self.tipo_equipo,
            "dificultad": self.dificultad,
            "url_video": self.url_video,
        }
