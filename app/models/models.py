from flask import Blueprint
from flask_restx import  Api, fields

# Creación de Blueprint y API
userAPI = Blueprint('userAPI', __name__)
api = Api(userAPI, doc='/swagger', title='API de Usuarios', description='API Usuarios Energy Vibes', default='Crud API Energy Vibes')

# Definición del modelo de usuario
user_model = api.model('User', {
    'id': fields.String(description='ID del usuario'),
    'name': fields.String(description='Nombre del usuario'),
    'age': fields.String(description='Edad del usuario'),
    'email': fields.String(description='Email del usuario'),
    'password': fields.String(description='Contraseña del usuario'),
    'role': fields.String(descrption='Rol del usuario')
})