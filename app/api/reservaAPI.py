from flask import request
from flask_restx import Resource, marshal_with
from flask_cors import cross_origin
from app import app
from app.database.database import reservation_Ref, get_next_id_reservation, verify_firebase_token
from app.models.models import ReservationAPI, res_api, res_model

# Crear una instancia de ReservationAPI y api para las rutas de horas disponibles
ReservationAPI = ReservationAPI
api = res_api

# Definir el modelo de horas disoonibles
res_model = res_model

@cross_origin
@res_api.route('/post', methods=['POST'])
class CreateReservation(Resource):
    @res_api.expect(res_model, validate=True)
    def post(self):
        """Registrar una nueva reserva"""
        if request.headers['Content-Type'] == 'application/json':
            try:
                # Obtener un nuevo ID para la reserva
                new_id = get_next_id_reservation()

                # Almacenar los datos de la nueva reserva en la base de datos
                reservation_Ref.document(new_id).set({
                    'id': new_id,
                    'usuario': request.json['usuario'],
                    'nombreGym': request.json['nombreGym'],
                    'direccion': request.json['direccion'],
                    'horaAgendada': request.json['horaAgendada'],
                    'fechaAgendada': request.json['fechaAgendada'],
                })

                return {'success': True, 'message': 'Reserva registrada'}, 201
            except Exception as e:
                return {'error': f'Ha ocurrido un error: {str(e)}'}, 500
        else:
            return {'error': 'Content-Type debe ser application/json'}, 415

@cross_origin
@res_api.route('/get', methods=['GET'])
class GetReservations(Resource):
    def get(self):
        """Obtener datos de reservas realizadas"""
        # Verifica la autenticación con Firebase
        authenticated = verify_firebase_token()

        if authenticated:
            try:
                # Cambia la colección a reservation_Ref para obtener reservas desde la base de datos
                reservation_collection = reservation_Ref.stream()

                # Crear una lista para almacenar los datos de todas las reservas
                reservations_data = []

                # Iterar a través de los documentos de reserva en la colección
                for reservation_doc in reservation_collection:
                    reservations_data.append(reservation_doc.to_dict())

                return {"reservations_data": reservations_data}, 200  # Devolver los datos de reservas como respuesta
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {'error': 'No estás autenticado en Firebase'}, 401
