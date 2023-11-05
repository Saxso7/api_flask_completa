from flask import request
from flask_restx import Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import gym_Ref, get_next_id_gym, verify_firebase_token
from app.models.models import gym_api, gym_model, gymAPI

# Crear una instancia de gymAPI y api para las rutas de gimnasio
gymAPI = gymAPI
api = gym_api

# Definir el modelo de gimnasio
gym_model = gym_model

# Ruta para obtener datos de gimnasio (GET)
@cross_origin
@api.route('/get', methods=['GET'])  # Cambia la ruta a '/get_gym'
class GetGym(Resource):
    def get(self):
        """Obtener datos de gimnasio"""
        # Verifica la autenticación con Firebase
        authenticated = verify_firebase_token()

        if authenticated:
            try:
                # Obtener la colección de gimnasios desde la base de datos
                gym_collection = gym_Ref.stream()

                # Crear una lista para almacenar los datos de todas las gimnasios
                gyms_data = []

                # Iterar a través de los documentos de gimnasio en la colección
                for gym_doc in gym_collection:
                    gym_data = gym_doc.to_dict()
                    gyms_data.append(gym_data)

                return {"gyms": gyms_data}, 200  # Devolver los datos de los gimnasios como respuesta
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'No estás autenticado en Firebase'}, 401


# Ruta para registrar una nuevo gimnasio (POST)
@cross_origin
@api.route('/post')
class CreateGym(Resource):
    @api.expect(gym_model, validate=True)
    def post(self):
        """Registrar una nuevo gimnasio"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la gimnasio
                new_id = get_next_id_gym()

                # Almacenar los datos de la nuevo gimnasio en la base de datos
                gym_Ref.document(new_id).set({
                    'id': new_id,
                    'nombre': request.json['nombre'],
                    'latitud': request.json['latitud'],
                    'longitud': request.json['longitud'],
                    'direccion': request.json['direccion'],
                    'horario': request.json['horario']
                    

                })

                return {'success': True, 'message': 'gimnasio registrada'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415

# Ruta para eliminar un gimnasio por ID
@api.route('/delete/<gym_id>')
class DeleteGym(Resource):
    def delete(self, gym_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        gym_doc = gym_Ref.document(gym_id).get()
        if gym_doc.exists:
            gym_Ref.document(gym_id).delete()
            return {'success': True, 'message': 'gimnasio eliminado con éxito'}, 200
        else:
            return {'error': 'gimnasio no encontrado'}, 404
        
# Ruta para actualizar un gimnasio por ID
@api.route('/put/<gym_id>')
class UpdateUser(Resource):
    @api.expect(gym_model, validate=True)
    def put(self, gym_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = gym_Ref.document(gym_id).get()
                if user_doc.exists:
                    tipo = request.json['tipo']
                    contenido = request.json['contenido']
                    
                    gym_data = {
                        'tipo': tipo,
                        'contenido': contenido,
                        'periodo': request.json['periodo']
                    }

                    gym_Ref.document(gym_id).update(gym_data)

                    return {'success': True, 'message': 'gimnasio actualizado con éxito'}, 200
                else:
                    return {'error': 'gimnasio no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415