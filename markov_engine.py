import random

# La matriz de probabilidades exactas con subestados y limpieza biológica.
# DORMIR y COMER_BEBER están al mínimo (1-2%) para depender del biological_engine.
# OCIO_SOCIAL_CONVERSAR solo es accesible (salvo excepciones del 0%) desde OCIO_SOCIAL_SITIO.
TRANSITION_MATRIX = {
    "DORMIR": {
        # Te despiertas: Lo normal es ir a trabajar/estudiar, o relajarte/tareas si es finde.
        "DORMIR": 0.0, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.45, 
        "INACTIVO_RELAX": 0.20, "INACTIVO_TAREAS_CASA": 0.15, "OCIO_INDIVIDUAL": 0.05, 
        "OCIO_SOCIAL_SITIO": 0.03, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.10
    },
    "COMER_BEBER": {
        # Terminas de comer: Vuelves al trabajo, o te echas a relajar (la siesta/descanso).
        "DORMIR": 0.01, "COMER_BEBER": 0.0, "TRABAJAR_ESTUDIAR": 0.25, 
        "INACTIVO_RELAX": 0.25, "INACTIVO_TAREAS_CASA": 0.10, "OCIO_INDIVIDUAL": 0.15, 
        "OCIO_SOCIAL_SITIO": 0.10, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.14
    },
    "TRABAJAR_ESTUDIAR": {
        # Terminas la jornada laboral: Estás cansado. Te vas a casa a relajarte o quedas en un sitio.
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.0, 
        "INACTIVO_RELAX": 0.35, "INACTIVO_TAREAS_CASA": 0.15, "OCIO_INDIVIDUAL": 0.15, 
        "OCIO_SOCIAL_SITIO": 0.20, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.12
    },
    "INACTIVO_RELAX": {
        # Terminas de relajarte: Ya tienes energía para hacer tareas de casa, salir o mirar el móvil.
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.15, 
        "INACTIVO_RELAX": 0.0, "INACTIVO_TAREAS_CASA": 0.20, "OCIO_INDIVIDUAL": 0.20, 
        "OCIO_SOCIAL_SITIO": 0.21, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.20
    },
    "INACTIVO_TAREAS_CASA": {
        # Limpiar cansa: Lo normal es tirarse a relajarse o mirar el móvil al terminar.
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.10, 
        "INACTIVO_RELAX": 0.35, "INACTIVO_TAREAS_CASA": 0.0, "OCIO_INDIVIDUAL": 0.15, 
        "OCIO_SOCIAL_SITIO": 0.20, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.17
    },
    "OCIO_INDIVIDUAL": {
        # Vuelves del gimnasio/parque: A casa a relajarte o sigues por ahí.
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.10, 
        "INACTIVO_RELAX": 0.35, "INACTIVO_TAREAS_CASA": 0.15, "OCIO_INDIVIDUAL": 0.0, 
        "OCIO_SOCIAL_SITIO": 0.20, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.17
    },
    "OCIO_SOCIAL_SITIO": {
        # Estás en un local/plaza: ALTA probabilidad de ponerse a conversar, o te vas a casa.
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.12, "INACTIVO_TAREAS_CASA": 0.05, "OCIO_INDIVIDUAL": 0.05, 
        "OCIO_SOCIAL_SITIO": 0.10, "OCIO_SOCIAL_CONVERSAR": 0.55, "USANDO_RRSS": 0.05
    },
    "OCIO_SOCIAL_CONVERSAR": {
        # Acaba la charla: Te quedas en el sitio pero sin hablar, o te vas a tu casa a relajarte.
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.05, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.30, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.17
    },
    "USANDO_RRSS": {
        # Dejas el móvil: A relajarte, a hacer tareas o a salir.
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.15, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.20, "OCIO_INDIVIDUAL": 0.15, 
        "OCIO_SOCIAL_SITIO": 0.16, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.0
    }
}

def get_markov_probabilities(current_state):
    """
    Recibe el estado actual y devuelve las opciones y sus probabilidades base,
    SIN tirar los dados todavía, para permitir la alteración biológica.
    """
    # Si por algún motivo el estado no existe, forzamos un reset a INACTIVO_RELAX
    if current_state not in TRANSITION_MATRIX:
        current_state = "INACTIVO_RELAX"

    opciones = list(TRANSITION_MATRIX[current_state].keys())
    probabilidades = list(TRANSITION_MATRIX[current_state].values())
    
    return opciones, probabilidades

def evaluate_virtual_action(current_state, next_state):
    """
    Evalúa la transición para determinar si se ha producido una interacción
    con la red social (Simulodon), según las reglas del profesor.
    """
    if current_state != "USANDO_RRSS" and next_state == "USANDO_RRSS":
        return "ENTRAR EN RRSS"
    elif current_state == "USANDO_RRSS" and next_state == "USANDO_RRSS":
        return "SEGUIR EN RRSS"
    elif current_state == "USANDO_RRSS" and next_state != "USANDO_RRSS":
        return "SALIR DE RRSS"
    else:
        return "ACCION_FISICA"