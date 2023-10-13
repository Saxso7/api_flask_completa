from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS



# Crea una instancia de la aplicación Flask
app = Flask(__name__)


cors = CORS(app, resources={ r"//*" :{"origins":"*"}})


# Configura la llave secreta de la aplicación Flask (para sesiones seguras, por ejemplo)
app.config['SECRET_KEY'] = '123456qwerty'


# Carga las credenciales de Firebase desde un archivo JSON
cred = credentials.Certificate("app/database/firebase.json")

# Inicializa la aplicación Firebase con las credenciales
default_app = initialize_app(cred)

# Define una función para crear la aplicación Flask
def create_app():
    # Registra el Blueprint 'userAPI' en la aplicación Flask
    from app.api.userAPI import userAPI
    from app.api.dietAPI import dietAPI
    app.register_blueprint(userAPI, url_prefix='/user')
    app.register_blueprint(dietAPI, url_prefix='/diet')


    return app