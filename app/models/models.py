from flask import Blueprint
from flask_restx import Api, fields

# Creación de Blueprint y API para el sector de usuario
userAPI = Blueprint('userAPI', __name__)
user_api = Api(userAPI, doc='/swagger', title='API Energy Vibes (Usuario)', description='API Energy Vibes (Usuario)', default='API Energy Vibes (Usuario)')

# Definición del modelo de usuario para el sector de usuario
user_model = user_api.model('User', {
    'id': fields.String(description='ID del usuario'),
    'name': fields.String(description='Nombre del usuario'),
    'lastName': fields.String(description='Apellido del usuario'),
    'age': fields.String(description='Edad del usuario'),
    'numContact': fields.String(description='Contacto del usuario'),
    'email': fields.String(description='Email del usuario'),
    'password': fields.String(description='Contraseña del usuario'),
    'role': fields.String(description='Rol del usuario')
})

# Creación de Blueprint y API para el sector de dieta de resistencia
dietResAPI = Blueprint('dietResAPI', __name__)
dietRes_api = Api(dietResAPI, doc='/swagger', title='API Energy Vibes (Dieta Resitencia)', description='API Energy Vibes (Dieta Resistencia)', default='API Energy Vibes (Dieta Resistencia)')

# Definicion del modelo de dietas para el sector de dieta
dietRes_model = dietRes_api.model('DietRes', {
    'id': fields.String(description='ID de las dietas'),
    'state': fields.String(description='Opcion de esta dieta'),
    'desayuno': fields.String(),
    'nombreDesayuno': fields.String(description= 'Batido y frutas'),
    'descripcionDesayuno': fields.String(description='Como esta compuesto el desayuno'),
    'almuerzo': fields.String(),
    'nombreAlmuerzo': fields.String(description='Nombre de la comida'),
    'descripcionAlmuerzo': fields.String(description='Como esta compuesto la comida'),
    'meriendaTarde': fields.String(),
    'nombreMeriendaTarde': fields.String(description='Nombre de la merienda'),
    'descripcionMeriendatarde': fields.String(description='Como esta compuesto la merienda'),
    'cena': fields.String(),
    'nombreCena': fields.String(description='Nombre de la cena'),
    'descripcionCena': fields.String(description='descripcion de la cena'),
    'meriendaNocturna': fields.String(),
    'nombreMeriendaNocturna': fields.String(description='Nombre de la merienda nocturna'),
    'descripcionMeriendaNocturna': fields.String(description='Descripcion de la merienda nocturna'),

})

# Creación de Blueprint y API para el sector de dieta Cardio
dietCardApi = Blueprint('dietCardApi', __name__)
dietCard_api = Api(dietCardApi, doc='/swagger', title='API Energy Vibes (Dieta Cardio)', description='API Energy Vibes (Dieta Cardio)', default='API Energy Vibes (Dieta Cardio)')

# Definicion del modelo de dietas para el sector de dieta Cardio
dietCard_model = dietCard_api.model('DietCard', {
    'id': fields.String(description='ID de las dietas'),
    'state': fields.String(description='Opcion de esta dieta'),
    'desayuno': fields.String(),
    'nombreDesayuno': fields.String(description= 'Batido y frutas'),
    'descripcionDesayuno': fields.String(description='Como esta compuesto el desayuno'),
    'almuerzo': fields.String(),
    'nombreAlmuerzo': fields.String(description='Nombre de la comida'),
    'descripcionAlmuerzo': fields.String(description='Como esta compuesto la comida'),
    'meriendaTarde': fields.String(),
    'nombreMeriendaTarde': fields.String(description='Nombre de la merienda'),
    'descripcionMeriendatarde': fields.String(description='Como esta compuesto la merienda'),
    'cena': fields.String(),
    'nombreCena': fields.String(description='Nombre de la cena'),
    'descripcionCena': fields.String(description='descripcion de la cena'),
    'meriendaNocturna': fields.String(),
    'nombreMeriendaNocturna': fields.String(description='Nombre de la merienda nocturna'),
    'descripcionMeriendaNocturna': fields.String(description='Descripcion de la merienda nocturna'),

})
# Creación de Blueprint y API para el sector de dieta Entrenamiento Fuerte
dietHighAPI = Blueprint('dietHigh', __name__)
dietHigh_api = Api(dietHighAPI, doc='/swagger', title='API Energy Vibes (Dieta Entrenamiento Fuerte)', description='API Energy Vibes (Dieta Entrenamiento Fuerte)', default='API Energy Vibes (Dieta Entrenamiento Fuerte)')

# Definicion del modelo de dietas para el sector de dieta Entrenamiento Fuerte
dietHigh_model = dietHigh_api.model('DietCard', {
    'id': fields.String(description='ID de las dietas'),
    'state': fields.String(description='Opcion de esta dieta'),
    'desayuno': fields.String(),
    'nombreDesayuno': fields.String(description= 'Batido y frutas'),
    'descripcionDesayuno': fields.String(description='Como esta compuesto el desayuno'),
    'almuerzo': fields.String(),
    'nombreAlmuerzo': fields.String(description='Nombre de la comida'),
    'descripcionAlmuerzo': fields.String(description='Como esta compuesto la comida'),
    'meriendaTarde': fields.String(),
    'nombreMeriendaTarde': fields.String(description='Nombre de la merienda'),
    'descripcionMeriendatarde': fields.String(description='Como esta compuesto la merienda'),
    'cena': fields.String(),
    'nombreCena': fields.String(description='Nombre de la cena'),
    'descripcionCena': fields.String(description='descripcion de la cena'),
    'meriendaNocturna': fields.String(),
    'nombreMeriendaNocturna': fields.String(description='Nombre de la merienda nocturna'),
    'descripcionMeriendaNocturna': fields.String(description='Descripcion de la merienda nocturna'),

})
# Creación de Blueprint y API para el sector de dieta Entrenamiento Fuerte
dietWeightAPI = Blueprint('dietWeight', __name__)
dietWeight_api = Api(dietWeightAPI, doc='/swagger', title='API Energy Vibes (Dieta Perdida de peso)', description='API Energy Vibes (Dieta Perdida de peso)', default='API Energy Vibes (Dieta Perdida de peso)')

# Definicion del modelo de dietas para el sector de dieta Entrenamiento Fuerte
dietWeight_model = dietWeight_api.model('DietCard', {
    'id': fields.String(description='ID de las dietas'),
    'state': fields.String(description='Opcion de esta dieta'),
    'desayuno': fields.String(),
    'nombreDesayuno': fields.String(description= 'Batido y frutas'),
    'descripcionDesayuno': fields.String(description='Como esta compuesto el desayuno'),
    'almuerzo': fields.String(),
    'nombreAlmuerzo': fields.String(description='Nombre de la comida'),
    'descripcionAlmuerzo': fields.String(description='Como esta compuesto la comida'),
    'meriendaTarde': fields.String(),
    'nombreMeriendaTarde': fields.String(description='Nombre de la merienda'),
    'descripcionMeriendatarde': fields.String(description='Como esta compuesto la merienda'),
    'cena': fields.String(),
    'nombreCena': fields.String(description='Nombre de la cena'),
    'descripcionCena': fields.String(description='descripcion de la cena'),
    'meriendaNocturna': fields.String(),
    'nombreMeriendaNocturna': fields.String(description='Nombre de la merienda nocturna'),
    'descripcionMeriendaNocturna': fields.String(description='Descripcion de la merienda nocturna'),

})

# Creación de Blueprint y API para el sector de gym
gymAPI = Blueprint('gymAPI', __name__)
gym_api = Api(gymAPI, doc='/swagger', title='API Energy Vibes (gimnasio)', description='API Energy Vibes (gimnasio)', default='API Energy Vibes (gimnasio)')

# Definicion del modelo de dietas para el sector de dieta
gym_model = gym_api.model('Gym', {
    'id': fields.String(description='ID de las gimnasio'),
    'nombre': fields.String(description='Nombre del gimnacio'),
    'latitud': fields.Float(description='latitud del gimnasio'),
    'longitud': fields.Float(description='longitud del gimnasio'),
    'direccion': fields.String(description='direccion del gimnasio'),
    'horario': fields.String(description='horario del gimnasio'),

})