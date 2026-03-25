import random

# MATRIZ PRIMARIA (Solo acciones físicas y de ubicación)
TRANSITION_MATRIX = {
    "DORMIR": {
        "DORMIR": 0.0, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.45, 
        "INACTIVO_RELAX": 0.23, "INACTIVO_TAREAS_CASA": 0.15, 
        "OCIO_INDIVIDUAL": 0.05, "OCIO_PUBLICO": 0.10
    },
    "COMER_BEBER": {
        "DORMIR": 0.01, "COMER_BEBER": 0.0, "TRABAJAR_ESTUDIAR": 0.35, 
        "INACTIVO_RELAX": 0.20, "INACTIVO_TAREAS_CASA": 0.10, 
        "OCIO_INDIVIDUAL": 0.19, "OCIO_PUBLICO": 0.15
    },
    "TRABAJAR_ESTUDIAR": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.0, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.15, 
        "OCIO_INDIVIDUAL": 0.22, "OCIO_PUBLICO": 0.30
    },
    "INACTIVO_RELAX": {
        "DORMIR": 0.02, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.16, 
        "INACTIVO_RELAX": 0.05, "INACTIVO_TAREAS_CASA": 0.25, 
        "OCIO_INDIVIDUAL": 0.25, "OCIO_PUBLICO": 0.25
    },
    "INACTIVO_TAREAS_CASA": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.15, 
        "INACTIVO_RELAX": 0.30, "INACTIVO_TAREAS_CASA": 0.0, 
        "OCIO_INDIVIDUAL": 0.20, "OCIO_PUBLICO": 0.32
    },
    "OCIO_INDIVIDUAL": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.17, 
        "INACTIVO_RELAX": 0.35, "INACTIVO_TAREAS_CASA": 0.15, 
        "OCIO_INDIVIDUAL": 0.0, "OCIO_PUBLICO": 0.30
    },
    "OCIO_PUBLICO": {
        "DORMIR": 0.01, "COMER_BEBER": 0.02, "TRABAJAR_ESTUDIAR": 0.17, 
        "INACTIVO_RELAX": 0.25, "INACTIVO_TAREAS_CASA": 0.15, 
        "OCIO_INDIVIDUAL": 0.20, "OCIO_PUBLICO": 0.20
    }
}

# MATRIZ SECUNDARIA (Probabilidad de multitarea según el Hilo Primario)
SECONDARY_PROBABILITIES = {
    "DORMIR": {"USANDO_RRSS": 0.0, "CONVERSAR": 0.0, "NINGUNO": 1.0},
    "COMER_BEBER": {"USANDO_RRSS": 0.20, "CONVERSAR": 0.10, "NINGUNO": 0.70},
    "TRABAJAR_ESTUDIAR": {"USANDO_RRSS": 0.05, "CONVERSAR": 0.15, "NINGUNO": 0.80},
    "INACTIVO_RELAX": {"USANDO_RRSS": 0.40, "CONVERSAR": 0.20, "NINGUNO": 0.40},
    "INACTIVO_TAREAS_CASA": {"USANDO_RRSS": 0.10, "CONVERSAR": 0.20, "NINGUNO": 0.70},
    "OCIO_INDIVIDUAL": {"USANDO_RRSS": 0.15, "CONVERSAR": 0.05, "NINGUNO": 0.80},
    "OCIO_PUBLICO": {"USANDO_RRSS": 0.05, "CONVERSAR": 0.60, "NINGUNO": 0.35}
}

def get_markov_probabilities(current_primary_state):
    """Devuelve probabilidades del HILO PRIMARIO."""
    if current_primary_state not in TRANSITION_MATRIX:
        current_primary_state = "INACTIVO_RELAX"
    return list(TRANSITION_MATRIX[current_primary_state].keys()), list(TRANSITION_MATRIX[current_primary_state].values())

def evaluate_secondary_state(primary_state):
    """Lanza los dados para ver si el agente decide activar un hilo secundario."""
    probs = SECONDARY_PROBABILITIES.get(primary_state, {"NINGUNO": 1.0})
    return random.choices(list(probs.keys()), weights=list(probs.values()), k=1)[0]

def evaluate_virtual_action(current_sec, next_sec):
    """Actualizado para usar el Hilo Secundario."""
    if current_sec != "USANDO_RRSS" and next_sec == "USANDO_RRSS":
        return "ENTRAR EN RRSS"
    elif current_sec == "USANDO_RRSS" and next_sec == "USANDO_RRSS":
        return "SEGUIR EN RRSS"
    elif current_sec == "USANDO_RRSS" and next_sec != "USANDO_RRSS":
        return "SALIR DE RRSS"
    else:
        return "ACCION_FISICA"