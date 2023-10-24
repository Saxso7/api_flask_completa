from flask import Blueprint
from flask_restx import Api, fields

# Creación de Blueprint y API para el sector de usuario
userAPI = Blueprint('userAPI', __name__)
user_api = Api(userAPI, doc='/swagger', title='API Energy Vibes (Usuario)', description='API Energy Vibes (Usuario)', default='API Energy Vibes (Usuario)')

# Definición del modelo de usuario para el sector de usuario
user_model = user_api.model('User', {
    'id': fields.String(description='ID del usuario'),
    'name': fields.String(description='Nombre del usuario'),
    'age': fields.String(description='Edad del usuario'),
    'email': fields.String(description='Email del usuario'),
    'password': fields.String(description='Contraseña del usuario'),
    'role': fields.String(description='Rol del usuario')
})

# Creación de Blueprint y API para el sector de dieta
dietAPI = Blueprint('dietAPI', __name__)
diet_api = Api(dietAPI, doc='/swagger', title='API Energy Vibes (Dieta)', description='API Energy Vibes (Dieta)', default='API Energy Vibes (Dieta)')

# Definicion del modelo de dietas para el sector de dieta
diet_model = diet_api.model('Diet', {
    'id': fields.String(description='ID de las dietas'),
    'tipo': fields.String(description='Tipo de dieta'),
    'contenido': fields.String(description='Contenido de la dieta'),
    'periodo': fields.String(description='Tiempo de duracion de la dieta')
})

# Creación de Blueprint y API para el sector de dieta
gymAPI = Blueprint('gymAPI', __name__)
gym_api = Api(gymAPI, doc='/swagger', title='API Energy Vibes (gimnasio)', description='API Energy Vibes (gimnasio)', default='API Energy Vibes (gimnasio)')

# Definicion del modelo de dietas para el sector de dieta
gym_model = gym_api.model('Gym', {
    'id': fields.String(description='ID de las gimnasio'),
    'nombre': fields.String(description='Nombre del gimnacio'),
    'latitud': fields.Float(description='latitud del gimnasio'),
    'longitud': fields.Float(description='longitud del gimnasio'),
    'direccion': fields.String(description='direccion del gimnasio'),
    'horario': fields.String(description='horario del gimnasio'),

})