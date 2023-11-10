from flask import request
from flask_restx import Resource
from flask_cors import cross_origin
from app import app
from app.database.database import availability_Ref, get_next_id_av, verify_firebase_token
from app.models.models import DataAvAPI, dataA_api, dataA_model

# Crear una instancia de DataAvAPI y api para las rutas de horas disponibles
DataAvAPI = DataAvAPI
api = dataA_api

# Definir el modelo de horas disoonibles
dataA_model = dataA_model

@cross_origin
@api.route('/get', methods=['GET'])
class GetAvailability(Resource):
    def get(self):
        """Obtener datos de horas disponibles"""
        # Verifica la autenticación con Firebase
        authenticated = verify_firebase_token()

        if authenticated:
            try:
                # Cambia la colección a availability_Ref para obtener disponibilidades desde la base de datos
                availability_collection = availability_Ref.stream()

                # Crear una lista para almacenar los datos de todas las horas disponibles
                availability_data = []

                # Iterar a través de los documentos de disponibilidad en la colección
                for availability_doc in availability_collection:
                    availability_data.append(availability_doc.to_dict())

                return {"availability_data": availability_data}, 200  # Devolver los datos de horas disponibles como respuesta
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'No estás autenticado en Firebase'}, 401


@cross_origin
@api.route('/post')
class CreateAvailability(Resource):
    @api.expect(dataA_model, validate=True)
    def post(self):
        """Registrar nueva disponibilidad"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la disponibilidad
                new_id = get_next_id_av()

                # Almacenar los datos de la nueva disponibilidad en la base de datos
                availability_Ref.document(new_id).set({
                    'fechasDisponibles': request.json['fechasDisponibles'],
                    'hora': request.json['hora']
                })

                return {'success': True, 'message': 'Disponibilidad registrada'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415
