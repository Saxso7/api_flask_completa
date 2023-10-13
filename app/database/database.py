from functools import wraps
from flask import request, jsonify
from firebase_admin import firestore, auth  # Importa auth desde firebase_admin

# Conexión a Firestore
db = firestore.client()
user_Ref = db.collection('usuarios')
diet_Ref = db.collection('dietas')

# Función para obtener el próximo ID autoincremental
def get_next_id_user():
    new_id = 1
    
    while True:
        user_doc_ref = db.collection('usuarios').document(str(new_id))
        user_doc = user_doc_ref.get()
        
        if not user_doc.exists:
            return str(new_id)
        
        new_id += 1

# Función para obtener el próximo ID autoincremental
def get_next_id_diet():
    new_id = 1
    
    while True:
        diet_doc_ref = db.collection('dietas').document(str(new_id))
        diet_doc = diet_doc_ref.get()
        
        if not diet_doc.exists:
            return str(new_id)
        
        new_id += 1

# Crea una función de middleware para verificar la autenticación con Firebase
def verify_firebase_token():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # Puedes acceder a 'uid' para obtener el ID único del usuario
        return True, uid
    except auth.ExpiredIdTokenError:
        return False, None
    except Exception as e:
        return False, None
    



# Crear una función de decorador para verificar el rol
def check_admin_role(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            # Verificar la autenticación del usuario con Firebase
            id_token = request.headers.get('Authorization').split('Bearer ')[1]
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            
            # Obtener el usuario de Firebase
            user = auth.get_user(uid)

            # Obtener el rol del usuario desde Firestore
            user_data = user_Ref.where('email', '==', user.email).get()
            
            if user_data:
                user_data = user_data[0].to_dict()
                user_role = user_data.get('role')  # Ajusta el nombre del campo 'rol' en tu colección
                
                if user_role == 'admin':
                    return func(*args, **kwargs)
                else:
                    return {'error': 'Usuario no autorizado'}, 401
            else:
                return {'error': 'Usuario no encontrado'}, 404

        except Exception as e:
            return {'error': 'Error de autenticación'}, 401

    return decorated_function