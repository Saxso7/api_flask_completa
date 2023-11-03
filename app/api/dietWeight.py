from flask import request
from flask_restx import Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import dietWeight_Ref, get_next_id_dietWeight, verify_firebase_token
from app.models.models import dietWeightAPI, dietWeight_api, dietWeight_model

# Crear una instancia de dietWeightAPI y api para las rutas de dieta Resistencia
dietWeightAPI = dietWeightAPI
api = dietWeight_api

# Definir el modelo de dieta Resistencia
dietWeight_model = dietWeight_model

# Ruta para obtener datos de dieta Resistencia (GET)
@cross_origin
@api.route('/get', methods=['GET'])
class GetDietRes(Resource):

    def get(self):
        """Obtener datos de dieta Resistencia"""
        try:
            # Obtener la colección de dieta Resistencias desde la base de datos
            diet_collection = dietWeight_Ref.stream()

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
@api.route('/post')
class CreateDietRes(Resource):
    @api.expect(dietWeight_model, validate=True)
    def post(self):
        """Registrar una nueva dieta"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la dieta
                new_id = get_next_id_dietWeight()

                # Almacenar los datos de la nueva dieta en la base de datos
                dietWeight_Ref.document(new_id).set({
                    'id': new_id,
                    'descripcionDesayuno': request.json['descripcionDesayuno'],
                    'desayuno': request.json['desayuno'],
                    'nombreDesayuno': request.json['nombreDesayuno'],
                    'descripcionDesayuno': request.json['descripcionDesayuno'],
                    'almuerzo': request.json['almuerzo'],
                    'nombreAlmuerzo': request.json['nombreAlmuerzo'],
                    'descripcionAlmuerzo': request.json['descripcionAlmuerzo'],
                    'meriendaTarde': request.json['meriendaTarde'],
                    'nombreMeriendaTarde': request.json['nombreMeriendaTarde'],
                    'descripcionDesayuno': request.json['descripcionDesayuno'],
                    'descripcionMeriendatarde': request.json['descripcionMeriendatarde'],
                    'cena': request.json['cena'],
                    'nombreCena': request.json['nombreCena'],
                    'descripcionCena': request.json['descripcionCena'],
                    'meriendaNocturna': request.json['meriendaNocturna'],
                    'nombreMeriendaNocturna': request.json['nombreMeriendaNocturna'],
                    'descripcionMeriendaNocturna': request.json['descripcionMeriendaNocturna'],
                })

                return {'success': True, 'message': 'Dieta registrada'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415

# Ruta para eliminar un Dieta por ID
@api.route('/delete/<diet_id>')
class DeleteDietRes(Resource):
    def delete(self, diet_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        diet_doc = dietWeight_Ref.document(diet_id).get()
        if diet_doc.exists:
            dietWeight_Ref.document(diet_id).delete()
            return {'success': True, 'message': 'Dieta eliminado con éxito'}, 200
        else:
            return {'error': 'Dieta no encontrado'}, 404
        
# Ruta para actualizar un Dieta por ID
@api.route('/put/<diet_id>')
class UpdateDietRes(Resource):
    @api.expect(dietWeight_model, validate=True)
    def put(self, diet_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = dietWeight_Ref.document(diet_id).get()
                if user_doc.exists:
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    descripcionDesayuno = request.json['descripcionDesayuno']
                    desayuno = request.json['desayuno']
                    
                    
                    diet_data = {
                        'descripcionDesayuno': descripcionDesayuno,
                        'desayuno': desayuno,
                        'nombreDesayuno': request.json['nombreDesayuno']
                    }

                    dietWeight_Ref.document(diet_id).update(diet_data)

                    return {'success': True, 'message': 'dieta Resistencia actualizado con éxito'}, 200
                else:
                    return {'error': 'dieta Resistencia Resistencia no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415