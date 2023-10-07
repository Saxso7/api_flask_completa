from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager


# Crea una instancia de la aplicación Flask
app = Flask(__name__)


cors = CORS(app, resources={ r"//*" :{"origins":"*"}})
# Configuración de la extensión JWT

# Configura la llave secreta de la aplicación Flask (para sesiones seguras, por ejemplo)
app.config['SECRET_KEY'] = '123456qwerty'


# Carga las credenciales de Firebase desde un archivo JSON
cred = credentials.Certificate("api/app/database/firebase.json")

# Inicializa la aplicación Firebase con las credenciales
default_app = initialize_app(cred)

# Define una función para crear la aplicación Flask
def create_app():
    # Registra el Blueprint 'userAPI' en la aplicación Flask
    from .userAPI import userAPI
    app.register_blueprint(userAPI, url_prefix='')

    return app
