import random

# CAPA 1: MATRIZ PRIMARIA FASE 1 (5 Macro-Estados)
TRANSITION_MATRIX = {
    "DORMIR": {
        "DORMIR": 0.0, "COMER_BEBER": 0.01, "TRABAJAR_ESTUDIAR": 0.45, 
        "CASA": 0.35, "OCIO": 0.19
    },
    "COMER_BEBER": {
        "DORMIR": 0.01, "COMER_BEBER": 0.0, "TRABAJAR_ESTUDIAR": 0.35, 
        "CASA": 0.35, "OCIO": 0.29
    },
    "TRABAJAR_ESTUDIAR": {
        "DORMIR": 0.01, "COMER_BEBER": 0.1, "TRABAJAR_ESTUDIAR": 0.05, 
        "CASA": 0.45, "OCIO": 0.48
    },
    "CASA": {
        "DORMIR": 0.05, "COMER_BEBER": 0.05, "TRABAJAR_ESTUDIAR": 0.30, 
        "CASA": 0.15, "OCIO": 0.45
    },
    "OCIO": {
        "DORMIR": 0.025, "COMER_BEBER": 0.025, "TRABAJAR_ESTUDIAR": 0.20, 
        "CASA": 0.55, "OCIO": 0.20
    }
}

# CAPA 2: MICRO-ACCIONES (Encuesta del Empleo del Tiempo INE)
MICRO_ACTIONS = {
    "DORMIR": {
        "dormir_profundamente": 85,
        "dormir_siesta": 15
    },
    "COMER_BEBER": {
        "comer_en_casa": 45,            # (Basado en 31 Actividades culinarias: 63.7%)
        "comer_fuera_de_casa": 20,      # (Derivado de Visitas y vida social)
        "merendar_algo_rapido": 15,
        "usar_rrss_comiendo": 10,       # (Basado en 21 Uso de redes sociales: 32.3%) -> NUEVA ACCIÓN
        "conversar_comiendo": 10
    },
    "TRABAJAR_ESTUDIAR": {
        "trabajar": 35,                 # (Basado en 11 Trabajo principal: 31.6%)
        "ir_a_clase": 35,
        "tareas_personales": 15,        # (Basado en 324 Tareas de organización: 22.8%)
        "conversar": 10,
        "usar_rrss": 5
    },
    "CASA": {
        "ver_la_television": 35,        # (Basado en 82 Ver televisión: 84.5%)
        "usar_rrss": 20,                # (Basado en 21 Uso de redes sociales: 32.3%) -> NUEVA ACCIÓN
        "hacer_limpieza": 15,           # (Basado en 321 Limpieza de la vivienda: 35.9%)
        "jugar_videojuegos": 10,        # (Basado en 73 Juegos: 10.4%)
        "conversar": 10,                # (Basado en 51 Vida social: 43.7%) -> NUEVA ACCIÓN (Aunque no es tan común en casa, lo dejamos para dar variedad)
        "leer": 10                      # (Basado en 81 Lectura: 21.4%) -> NUEVA ACCIÓN
    },
    "OCIO": {
        "dar_una_vuelta": 10,
        "conversar": 40,        # (Basado en 51 Vida social: 43.7%)
        "usar_rrss": 5,
        "hacer_ejercicio": 10,  # (Agregado de gimnasia, balón, acuáticos: ~10%)
        "culturizarse": 10,
        "tomar_algo": 15,
        "leer": 10
    }
}

def get_markov_probabilities(current_macro_state):
    """Devuelve las probabilidades de la CAPA 1 (Macro-estados)."""
    if current_macro_state not in TRANSITION_MATRIX:
        current_macro_state = "CASA"
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
        
        # En la Fase 2 aquí leeremos los rasgos del agente para alterar el peso.
        # Por ahora, usamos el modificador genérico o 1.0
        multiplicador = agente.markov_modifiers.get(accion, 1.0)
        pesos_personalizados.append(peso_original * multiplicador)

    return random.choices(acciones_posibles, weights=pesos_personalizados, k=1)[0]



# CAPA 3: REDES SOCIALES (Cadena de Markov Absorbente)

# El estado "salir" es el estado absorbente. Una vez se llega a él, el bucle termina.
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
    estado_actual = "ver_contenido" # Siempre se entra a la app viendo el feed
    acciones_realizadas = {"ver_contenido": 0, "dar_like": 0, "comentar": 0, "publicar": 0}
    
    # Bucle intra-turno (Límite máximo de 15 acciones para evitar bucles infinitos por seguridad)
    for _ in range(15):
        if estado_actual == "salir":
            break
            
        acciones_realizadas[estado_actual] += 1
        
        probs = RRSS_TRANSITIONS[estado_actual]
        estado_actual = random.choices(list(probs.keys()), weights=list(probs.values()), k=1)[0]
        
    # --- TRADUCTOR NARRATIVO ---
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
        
    # Formateamos la lista a lenguaje natural (Ej: "hizo scroll, dio 2 likes y escribió 1 comentario")
    if len(resumen) > 1:
        texto_final = ", ".join(resumen[:-1]) + " y " + resumen[-1]
    else:
        texto_final = resumen[0]
        
    return texto_final