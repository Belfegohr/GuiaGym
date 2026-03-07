from datetime import datetime
from fitness_api.extensiones import db, bcrypt


class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    genero = db.Column(db.String(20), nullable=True)
    altura = db.Column(db.Float, nullable=True)
    peso_actual = db.Column(db.Float, nullable=True)
    objetivo = db.Column(db.String(50), nullable=True)
    nivel_experiencia = db.Column(db.String(50), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def establecer_contraseña(self, texto_plano):
        self.contraseña = bcrypt.generate_password_hash(texto_plano).decode("utf-8")

    def verificar_contraseña(self, texto_plano):
        return bcrypt.check_password_hash(self.contraseña, texto_plano)

    def a_dict(self, incluir_email=True):
        d = {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "genero": self.genero,
            "altura": self.altura,
            "peso_actual": self.peso_actual,
            "objetivo": self.objetivo,
            "nivel_experiencia": self.nivel_experiencia,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
        }
        if incluir_email:
            d["email"] = self.email
        return d
