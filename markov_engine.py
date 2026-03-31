import random

# CAPA 1: MATRIZ PRIMARIA FASE 1 (5 Macro-Estados Formales)
TRANSITION_MATRIX = {
    "DESCANSO": {
        "DESCANSO": 0.0, "ALIMENTACION": 0.01, "OBLIGACIONES": 0.45, 
        "TAREAS_DOMESTICAS": 0.35, "OCIO": 0.19
    },
    "ALIMENTACION": {
        "DESCANSO": 0.01, "ALIMENTACION": 0.0, "OBLIGACIONES": 0.35, 
        "TAREAS_DOMESTICAS": 0.35, "OCIO": 0.29
    },
    "OBLIGACIONES": {
        "DESCANSO": 0.01, "ALIMENTACION": 0.01, "OBLIGACIONES": 0.05, 
        "TAREAS_DOMESTICAS": 0.45, "OCIO": 0.48
    },
    "TAREAS_DOMESTICAS": {
        "DESCANSO": 0.05, "ALIMENTACION": 0.05, "OBLIGACIONES": 0.30, 
        "TAREAS_DOMESTICAS": 0.15, "OCIO": 0.45
    },
    "OCIO": {
        "DESCANSO": 0.03, "ALIMENTACION": 0.03, "OBLIGACIONES": 0.20, 
        "TAREAS_DOMESTICAS": 0.54, "OCIO": 0.20
    }
}

# CAPA 2: MICRO-ACCIONES (Formalizadas)
MICRO_ACTIONS = {
    "DESCANSO": {
        "sueno_profundo": 85,
        "descanso_diurno": 15
    },
    "ALIMENTACION": {
        "ingesta_en_hogar": 45,
        "ingesta_en_restauracion": 20,
        "ingesta_ligera": 15,
        "interaccion_ingesta": 10,
        "ingesta_rrss": 10
    },
    "OBLIGACIONES": {
        "jornada_laboral": 35,
        "jornada_academica": 35,
        "gestiones_personales": 15,
        "conversacion_con_companeros": 10,
        "revisar_rrss": 5
    },
    "TAREAS_DOMESTICAS": {
        "mantenimiento_del_hogar": 75,
        "conversacion_con_convivientes": 25
    },
    "OCIO": {
        "conversacion_social": 25,
        "ocio_hosteleria": 15,
        "paseo_recreativo": 10,
        "actividad_fisica": 10,
        "actividad_cultural": 10,
        "lectura": 10,
        "consumo_audiovisual": 10,
        "ocio_digital_activo": 5,
        "ver_rrss": 5
    }
}

def get_markov_probabilities(current_macro_state):
    """Devuelve las probabilidades de la CAPA 1 (Macro-estados)."""
    if current_macro_state not in TRANSITION_MATRIX:
        current_macro_state = "TAREAS_DOMESTICAS" # Actualizado el fallback
    return list(TRANSITION_MATRIX[current_macro_state].keys()), list(TRANSITION_MATRIX[current_macro_state].values())

def choose_micro_action(agente, macro_state):
    """
    Decide la acción específica de la CAPA 2 basándose en los pesos base 
    y aplicando los modificadores de personalidad del agente.
    """
    acciones_dict = MICRO_ACTIONS.get(macro_state, {"accion_por_defecto": 100})
    
    acciones_posibles = list(acciones_dict.keys())
    pesos_base = list(acciones_dict.values())
    
    pesos_personalizados = []
    for i in range(len(acciones_posibles)):
        accion = acciones_posibles[i]
        peso_original = pesos_base[i]
        
        multiplicador = agente.markov_modifiers.get(accion, 1.0)
        pesos_personalizados.append(peso_original * multiplicador)

    return random.choices(acciones_posibles, weights=pesos_personalizados, k=1)[0]


# CAPA 3: REDES SOCIALES (Cadena de Markov Absorbente)
RRSS_TRANSITIONS = {
    "ver_contenido": {"ver_contenido": 0.40, "dar_like": 0.30, "comentar": 0.05, "publicar": 0.05, "salir": 0.20},
    "dar_like":      {"ver_contenido": 0.45, "dar_like": 0.00, "comentar": 0.15, "publicar": 0.00, "salir": 0.40},
    "comentar":      {"ver_contenido": 0.30, "dar_like": 0.00, "comentar": 0.00, "publicar": 0.00, "salir": 0.70},
    "publicar":      {"ver_contenido": 0.20, "dar_like": 0.00, "comentar": 0.00, "publicar": 0.00, "salir": 0.80}
}

def simulate_rrss_session():
    """
    Simula una sesión completa de redes sociales en una fracción de segundo.
    Devuelve un string narrativo resumiendo todo lo que el agente hizo.
    """
    estado_actual = "ver_contenido" 
    acciones_realizadas = {"ver_contenido": 0, "dar_like": 0, "comentar": 0, "publicar": 0}
    
    for _ in range(15):
        if estado_actual == "salir":
            break
            
        acciones_realizadas[estado_actual] += 1
        
        probs = RRSS_TRANSITIONS[estado_actual]
        estado_actual = random.choices(list(probs.keys()), weights=list(probs.values()), k=1)[0]
        
    resumen = []
    if acciones_realizadas["ver_contenido"] > 0:
        resumen.append("hizo scroll viendo publicaciones")
    if acciones_realizadas["dar_like"] > 0:
        likes = acciones_realizadas["dar_like"]
        resumen.append(f"dio {likes} like{'s' if likes > 1 else ''}")
    if acciones_realizadas["comentar"] > 0:
        comentarios = acciones_realizadas["comentar"]
        resumen.append(f"escribió {comentarios} comentario{'s' if comentarios > 1 else ''}")
    if acciones_realizadas["publicar"] > 0:
        resumen.append("subió una nueva publicación")
        
    if not resumen:
        return "abrió la red social pero la cerró al instante sin hacer nada"
        
    if len(resumen) > 1:
        texto_final = ", ".join(resumen[:-1]) + " y " + resumen[-1]
    else:
        texto_final = resumen[0]
        
    return texto_final