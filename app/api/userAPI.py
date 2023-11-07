from flask import request
from flask_restx import  Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import verify_firebase_token, user_Ref, get_next_id_user, check_admin_role
from app.models.models import userAPI, user_model, user_api, update_field_model

#Asignamos el valor Blueprint y API desde models.py
userAPI = userAPI
api = user_api

#Asignamos el modelo de usuario
user_model = user_model

# Configuración de CORS
CORS = (app)

# Ruta para crear un nuevo usuario
@cross_origin
@api.route('/post')
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
                    'lastName': request.json['lastName'],
                    'age': age,
                    'numContact': request.json['numContact'],
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
@api.route('/get', methods=['GET'])
class GetUser(Resource):
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
@api.route('/get/<user_id>')
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
@api.route('/delete/<user_id>')
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
@api.route('/put/<user_id>')
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
                        'email': email,
                        'lastName': request.json['lastName'],
                        'numContact': request.json['numContact'],
                        'email': request.json['email']

                    }

                    user_Ref.document(user_id).update(user_data)

                    return {'success': True, 'message': 'Usuario actualizado con éxito'}, 200
                else:
                    return {'error': 'Usuario no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415
        
@api.route('/updateField/<user_id>')
class UpdateUserField(Resource):
    @api.expect(update_field_model, validate=True)
    def put(self, user_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()

        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = user_Ref.document(user_id).get()
                if user_doc.exists:
                    field_name = request.json.get('field_name')
                    new_value = request.json.get('new_value')

                    if field_name and new_value:
                        # Verifica si el campo a actualizar es válido
                        if field_name in ['name', 'age', 'email', 'lastName', 'numContact']:
                            # Actualiza el campo específico
                            user_Ref.document(user_id).update({field_name: new_value})

                            return {'success': True, 'message': f'Campo {field_name} actualizado con éxito'}, 200
                        else:
                            return {'error': 'Campo no válido para actualizar'}, 400
                    else:
                        return {'error': 'Se requiere field_name y new_value en la solicitud'}, 400
                else:
                    return {'error': 'Usuario no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415
