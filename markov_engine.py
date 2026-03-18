import random

# La matriz de probabilidades exactas con subestados y limpieza biológica.
# DORMIR y COMER_BEBER están al mínimo (1-2%) para depender del biological_engine.
# OCIO_SOCIAL_CONVERSAR solo es accesible (salvo excepciones del 0%) desde OCIO_SOCIAL_SITIO.
TRANSITION_MATRIX = {
    "DORMIR": {
        "DORMIR": 0.0, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.45, 
        "INACTIVO_RELAX": 0.15, "INACTIVO_TAREAS_CASA": 0.10, "OCIO_INDIVIDUAL": 0.05, 
        "OCIO_SOCIAL_SITIO": 0.10, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.13
    },
    "COMER_BEBER": {
        "DORMIR": 0.01, "COMER_BEBER": 0.0, "TRABAJAR_ESTUDIAR": 0.15, 
        "INACTIVO_RELAX": 0.25, "INACTIVO_TAREAS_CASA": 0.15, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.14, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.20
    },
    "TRABAJAR_ESTUDIAR": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.10, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.25, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.17
    },
    "INACTIVO_RELAX": {
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.15, "INACTIVO_TAREAS_CASA": 0.15, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.16, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.35
    },
    "INACTIVO_TAREAS_CASA": {
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.35, "INACTIVO_TAREAS_CASA": 0.05, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.15, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.26
    },
    "OCIO_INDIVIDUAL": {
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.10, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.10, "OCIO_INDIVIDUAL": 0.01, 
        "OCIO_SOCIAL_SITIO": 0.25, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.20
    },
    "OCIO_SOCIAL_SITIO": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.25, "INACTIVO_TAREAS_CASA": 0.05, "OCIO_INDIVIDUAL": 0.05, 
        "OCIO_SOCIAL_SITIO": 0.15, "OCIO_SOCIAL_CONVERSAR": 0.30, "USANDO_RRSS": 0.12
    },
    "OCIO_SOCIAL_CONVERSAR": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.05, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.05, "OCIO_INDIVIDUAL": 0.05, 
        "OCIO_SOCIAL_SITIO": 0.25, "OCIO_SOCIAL_CONVERSAR": 0.15, "USANDO_RRSS": 0.12
    },
    "USANDO_RRSS": {
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.10, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.10, "OCIO_INDIVIDUAL": 0.10, 
        "OCIO_SOCIAL_SITIO": 0.20, "OCIO_SOCIAL_CONVERSAR": 0.0, "USANDO_RRSS": 0.16
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