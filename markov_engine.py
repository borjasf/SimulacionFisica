import random

# Matriz de transición entre 5 macro-estados
# Probabilidades base calibradas mediante Cadena de Markov con distribución realista
# Se evita que agentes queden atrapados en patrones repetitivos
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

# Micro-acciones por macro-estado
# Pesos relativos basados en la Encuesta de Empleo del Tiempo (INE)
# Permiten variabilidad mientras mantienen proporciones realistas
MICRO_ACCIONES = {
    "DESCANSO": {
        # INE: Dormir 8.5h (85%), descanso diurno 1.2h (15%)
        "sueno_profundo": 80,
        "descanso_diurno": 20
    },
    
    "ALIMENTACION": {
        # INE: Mayormente en hogar, con variación según estilo de vida
        "ingesta_en_hogar": 40,
        "ingesta_en_restauracion": 20,
        "ingesta_ligera": 20,
        "interaccion_ingesta": 10,     # Comer socializando
        "ingesta_rrss": 10             # Comer frente a pantallas
    },
    
    "OBLIGACIONES": {
        # INE: Trabajo y estudios son mutuamente excluyentes por edad/ocupación
        "jornada_laboral": 30,
        "jornada_academica": 30,
        "gestiones_personales": 20,    # INE (Grupo 37): Gestiones y compras
        "conversacion_con_companeros": 12, # Pausas para el café
        "revisar_rrss": 8              # Procrastinación base
    },
    
    "TAREAS_DOMESTICAS": {
        # INE (Grupo 32 vs 511): Mantenimiento del hogar domina en horas (casi 1h 10m),
        # pero la vida social en familia es frecuente (unos 45m).
        "mantenimiento_del_hogar": 70,
        "conversacion_con_convivientes": 30
    },
    
    "OCIO": {
        # Reajuste masivo basado en INE:
        # 1. Medios de comunicación (Grupo 8): 88.3% participación (TV).
        # 2. Vida social (Grupo 5): 57.7% participación. Conversación y hostelería.
        # 3. Deportes (Grupo 6): 39.8% participación.
        # 4. Cultura: Se reduce a 5 por ser la de menor frecuencia diaria habitual.
        "consumo_audiovisual": 20,     # Lidera el ocio base por la EET del INE
        "conversacion_social": 15,
        "ocio_hosteleria": 12,
        "paseo_recreativo": 12,        # Ocio exterior de bajo impacto
        "actividad_fisica": 10,
        "ver_rrss": 10,                # (Ocio digital pasivo)
        "lectura": 8,
        "ocio_digital_activo": 8,      # Videojuegos y PC
        "actividad_cultural": 5        # Cine/Teatro/Museos (Raro de hacer a diario)
    }
}


def get_markov_probabilities(current_macro_state):
    """Devuelve las probabilidades de la CAPA 1 (Macro-estados)."""
    if current_macro_state not in TRANSITION_MATRIX:
        current_macro_state = "TAREAS_DOMESTICAS" # Actualizado el fallback
    return list(TRANSITION_MATRIX[current_macro_state].keys()), list(TRANSITION_MATRIX[current_macro_state].values())

def choose_micro_action(agente, macro_state):
    """
    Decide la acción específica aplicando modificadores de personalidad.
    Incluye protección matemática (Suavizado) para evitar colapsos de probabilidad 0.
    """
    # Si el macro_estado no existe, devolvemos un diccionario seguro temporal
    acciones_dict = MICRO_ACCIONES.get(macro_state, {"ver_rrss": 100})
    
    acciones_posibles = list(acciones_dict.keys())
    pesos_base = list(acciones_dict.values())
    
    pesos_finales = []
    for i in range(len(acciones_posibles)):
        accion = acciones_posibles[i]
        peso_original = pesos_base[i]
        
        multiplicador = agente.markov_modifiers.get(accion, 1.0)
        
        # Respetar los Ceros Estructurales (Reglas demográficas estrictas)
        if multiplicador == 0.0:
            peso_final = 0.0
        else:
            # Suavizado: Garantizamos un peso mínimo de 1.0 para mantener viva la opción
            peso_final = max(1.0, peso_original * multiplicador)
            
        pesos_finales.append(peso_final)

    # Seguro anti-crashes de Python (ValueError: Total of weights must be greater than zero)
    if sum(pesos_finales) <= 0:
        return acciones_posibles[0] 

    return random.choices(acciones_posibles, weights=pesos_finales, k=1)[0]


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