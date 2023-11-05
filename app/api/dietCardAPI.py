from flask import request
from flask_restx import Resource
from flask_cors import cross_origin, CORS
from app import app
from app.database.database import dietCard_Ref, get_next_id_dietCard, verify_firebase_token
from app.models.models import dietCardApi, dietCard_api, dietCard_model

# Crear una instancia de dietCardApi y api para las rutas de dieta Resistencia
dietCardApi = dietCardApi
api = dietCard_api

# Definir el modelo de dieta Resistencia
diedietCard_model = dietCard_model

# Ruta para obtener datos de dieta Resistencia (GET)
@cross_origin
@api.route('/get', methods=['GET'])
class GetDietRes(Resource):
    def get(self):
        """Obtener datos de dieta Resistencia"""
        # Verifica la autenticación con Firebase
        authenticated = verify_firebase_token()

        if authenticated:
            try:
                # Cambia la colección a dietCard_Ref para obtener dietas Resistencia desde la base de datos
                diet_collection = dietCard_Ref.stream()

                # Crear una lista para almacenar los datos de todas las dietas Resistencia
                diets_data = []

                # Iterar a través de los documentos de dieta en la colección
                for diet_doc in diet_collection:
                    diet_data = diet_doc.to_dict()
                    diets_data.append(diet_data)

                return {"diet_resistencias": diets_data}, 200  # Devolver los datos de las dietas Resistencia como respuesta
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'No estás autenticado en Firebase'}, 401


# Ruta para registrar una nueva dieta (POST)
@cross_origin
@api.route('/post')
class CreateDietRes(Resource):
    @api.expect(diedietCard_model, validate=True)
    def post(self):
        """Registrar una nueva dieta"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la dieta
                new_id = get_next_id_dietCard()

                # Almacenar los datos de la nueva dieta en la base de datos
                dietCard_Ref.document(new_id).set({
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

        diet_doc = dietCard_Ref.document(diet_id).get()
        if diet_doc.exists:
            dietCard_Ref.document(diet_id).delete()
            return {'success': True, 'message': 'Dieta eliminado con éxito'}, 200
        else:
            return {'error': 'Dieta no encontrado'}, 404
        
# Ruta para actualizar un Dieta por ID
@api.route('/put/<diet_id>')
class UpdateDietRes(Resource):
    @api.expect(diedietCard_model, validate=True)
    def put(self, diet_id):
        # Verifica la autenticación con Firebase
        authenticated, _ = verify_firebase_token()
        
        if not authenticated:
            return {'error': 'No estás autenticado en Firebase'}, 401

        if request.headers['Content-Type'] == 'application/json':
            try:
                user_doc = dietCard_Ref.document(diet_id).get()
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

                    dietCard_Ref.document(diet_id).update(diet_data)

                    return {'success': True, 'message': 'dieta Resistencia actualizado con éxito'}, 200
                else:
                    return {'error': 'dieta Resistencia Resistencia no encontrado'}, 404
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415