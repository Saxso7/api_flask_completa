from flask import Flask, render_template, request, url_for
from firebase_admin import credentials, initialize_app
from flask_cors import CORS
from firebase_admin import auth

# Crea una instancia de la aplicación Flask
app = Flask(__name__)


cors = CORS(app, resources={ r"//*" :{"origins":"*"}})


# Configura la llave secreta de la aplicación Flask (para sesiones seguras, por ejemplo)
app.config['SECRET_KEY'] = '123456qwerty'


# Carga las credenciales de Firebase desde un archivo JSON
cred = credentials.Certificate("app/database/firebase.json")

# Inicializa la aplicación Firebase con las credenciales
default_app = initialize_app(cred)

@app.route('/')
def index():
    return render_template('API.html')


# Define una función para crear la aplicación Flask
def create_app():    
    # Registra el Blueprint 'userAPI' en la aplicación Flask
    from app.api.userAPI import userAPI
    from app.api.dietResAPI import dietResAPI
    from app.api.gymAPI import gymAPI
    from app.api.dietCardAPI import dietCardApi
    from app.api.dietHighAPI import dietHighAPI
    from app.api.dietWeight import dietWeightAPI
    app.register_blueprint(userAPI, url_prefix='/user')
    app.register_blueprint(dietResAPI, url_prefix='/dietRes')
    app.register_blueprint(gymAPI, url_prefix='/gym')
    app.register_blueprint(dietCardApi, url_prefix='/dietCard')
    app.register_blueprint(dietHighAPI, url_prefix='/dietHigh')
    app.register_blueprint(dietWeightAPI, url_prefix='/dietWeight')

    
    


    return app
