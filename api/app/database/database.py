from flask import request
from firebase_admin import firestore, auth  # Importa auth desde firebase_admin

# Conexión a Firestore
db = firestore.client()
user_Ref = db.collection('usuarios')

# Función para obtener el próximo ID autoincremental
def get_next_id():
    new_id = 1
    
    while True:
        user_doc_ref = db.collection('usuarios').document(str(new_id))
        user_doc = user_doc_ref.get()
        
        if not user_doc.exists:
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