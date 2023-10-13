from flask import request
from flask_restx import Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import diet_Ref, get_next_id_diet, verify_firebase_token
from app.models.models import dietAPI, diet_api, diet_model

# Crear una instancia de dietAPI y api para las rutas de dieta
dietAPI = dietAPI
api = diet_api

# Definir el modelo de dieta
diet_model = diet_model

# Ruta para obtener datos de dieta (GET)
@cross_origin
@api.route('/diet/get', methods=['GET'])
class GetDiet(Resource):

    def get(self):
        """Obtener datos de dieta"""
        try:
            # Obtener la colección de dietas desde la base de datos
            diet_collection = diet_Ref.stream()

            # Crear una lista para almacenar los datos de todas las dietas
            diets_data = []

            # Iterar a través de los documentos de dieta en la colección
            for diet_doc in diet_collection:
                diet_data = diet_doc.to_dict()
                print(diet_data)
                diets_data.append(diet_data)

            return diets_data  # Devolver los datos de las dietas como respuesta
        except Exception as e:
            return {'error': str(e)}, 500

# Ruta para registrar una nueva dieta (POST)
@cross_origin
@api.route('/diet/post')
class CreateDiet(Resource):
    @api.expect(diet_model, validate=True)
    def post(self):
        """Registrar una nueva dieta"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la dieta
                new_id = get_next_id_diet()

                # Almacenar los datos de la nueva dieta en la base de datos
                diet_Ref.document(new_id).set({
                    'id': new_id,
                    'tipo': request.json['tipo'],
                    'contenido': request.json['contenido'],
                    'periodo': request.json['periodo']
                })

                return {'success': True, 'message': 'Dieta registrada'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415

# Ruta para eliminar un Dieta por ID
@api.route('/diet/delete/<diet_id>')
class DeleteDiet(Resource):
    def delete(self, diet_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        diet_doc = diet_Ref.document(diet_id).get()
        if diet_doc.exists:
            diet_Ref.document(diet_id).delete()
            return {'success': True, 'message': 'Dieta eliminado con éxito'}, 200
        else:
            return {'error': 'Dieta no encontrado'}, 404
        
# Ruta para actualizar un Dieta por ID
@api.route('/user/put/<diet_id>')
class UpdateUser(Resource):
    @api.expect(diet_model, validate=True)
    def put(self, diet_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = diet_Ref.document(diet_id).get()
                if user_doc.exists:
                    tipo = request.json['tipo']
                    contenido = request.json['contenido']
                    
                    diet_data = {
                        'tipo': tipo,
                        'contenido': contenido,
                        'periodo': request.json['periodo']
                    }

                    diet_Ref.document(diet_id).update(diet_data)

                    return {'success': True, 'message': 'Dieta actualizado con éxito'}, 200
                else:
                    return {'error': 'Dieta no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415