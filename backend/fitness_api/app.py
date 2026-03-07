from flask import Flask
from flask_cors import CORS
from fitness_api.configuracion import Configuracion
from fitness_api.extensiones import db, bcrypt
from fitness_api.rutas import autenticacion, usuarios, ejercicios, rutinas, entrenamientos, peso, estadisticas, social, desafios


def crear_app():
    app = Flask(__name__)
    app.config.from_object(Configuracion)
    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(autenticacion.bp)
    app.register_blueprint(usuarios.bp)
    app.register_blueprint(ejercicios.bp)
    app.register_blueprint(rutinas.bp)
    app.register_blueprint(entrenamientos.bp)
    app.register_blueprint(peso.bp)
    app.register_blueprint(estadisticas.bp)
    app.register_blueprint(social.bp)
    app.register_blueprint(desafios.bp)

    with app.app_context():
        import fitness_api.modelos
        db.create_all()

    return app


aplicacion = crear_app()

if __name__ == "__main__":
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)
