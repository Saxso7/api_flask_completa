from flask import request
from flask_restx import  Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import verify_firebase_token, user_Ref, get_next_id_user, check_admin_role
from app.models.models import userAPI, user_model, user_api

#Asignamos el valor Blueprint y API desde models.py
userAPI = userAPI
api = user_api

#Asignamos el modelo de usuario
user_model = user_model

# Configuración de CORS
CORS = (app)

# Ruta para crear un nuevo usuario
@cross_origin
@api.route('/user/post')
class CreateUser(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Crea un nuevo usuario"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                new_id = get_next_id_user()
                age = request.json['age']
                role = 'usuario'
                
                user_Ref.document(new_id).set({
                    'id': new_id,
                    'name': request.json['name'],
                    'age': age,
                    'email': request.json['email'],
                    'password': request.json['password'],
                    'role': role
                })

                return {'success': True, 'message': 'Usuario creado con éxito'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415

# Ruta para obtener todos los usuarios
@cross_origin
@api.route('/user/get', methods=['GET'])
class GetUser(Resource):
    @check_admin_role
    def get(self):
        # Verifica la autenticación con Firebase
        authenticated = verify_firebase_token()

        if authenticated:
            # Obtiene todos los documentos de la colección "users" en Firestore
            user_collection = user_Ref.stream()
        
            # Crea una lista para almacenar los datos de todos los usuarios
            users_data = []
        
            for user_doc in user_collection:
                user_data = user_doc.to_dict()
                users_data.append(user_data)
        
            return {"users": users_data}, 200
        else:
            return {'error': 'No estás autenticado en Firebase'}, 401
        

# Ruta para obtener un usuario por ID
@api.route('/user/get/<user_id>')
class GetSingleUser(Resource):
    def get(self, user_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        user_doc = user_Ref.document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return user_data, 200
        else:
            return {'error': 'Usuario no encontrado'}, 404

# Ruta para eliminar un usuario por ID
@api.route('/user/delete/<user_id>')
class DeleteUser(Resource):
    def delete(self, user_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        user_doc = user_Ref.document(user_id).get()
        if user_doc.exists:
            user_Ref.document(user_id).delete()
            return {'success': True, 'message': 'Usuario eliminado con éxito'}, 200
        else:
            return {'error': 'Usuario no encontrado'}, 404

# Ruta para actualizar un usuario por ID
@api.route('/user/put/<user_id>')
class UpdateUser(Resource):
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = user_Ref.document(user_id).get()
                if user_doc.exists:
                    age = request.json['age']
                    email = request.json['email']
                    
                    user_data = {
                        'name': request.json['name'],
                        'age': age,
                        'email': email
                    }

                    user_Ref.document(user_id).update(user_data)

                    return {'success': True, 'message': 'Usuario actualizado con éxito'}, 200
                else:
                    return {'error': 'Usuario no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415