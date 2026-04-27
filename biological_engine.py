import random

def update_biological_needs(agente):
    """
    Actualiza energía y saciedad según el estado y acción del agente.
    Aplica multiplicadores de personalidad a consumo y recuperación.
    """
    estado = agente.current_macro_state
    micro = agente.current_micro_action
    
    # Actualizar energía según estado
    if estado == "DESCANSO":
        # En descanso se recupera energía: máximo recuperable según tipo de descanso
        if micro == "sueno_profundo":
            agente.energia = min(100, agente.energia + (100 * agente.energy_recovery_mult))
        else:  # descanso_diurno
            agente.energia = min(100, agente.energia + (50 * agente.energy_recovery_mult))
    else:
        # En otras actividades se consume energía según intensidad física
        acciones_alto_desgaste = ["actividad_fisica", "mantenimiento_del_hogar", "paseo_recreativo", 
                                  "jornada_laboral", "jornada_academica", "gestiones_personales"]
        gasto_energia = 7 if micro in acciones_alto_desgaste else 5
        agente.energia = max(0, agente.energia - (gasto_energia * agente.energy_decay_mult))

    # Actualizar saciedad según estado
    if estado == "ALIMENTACION":
        # En alimentación se incrementa saciedad: cantidad varía por tipo de ingesta
        if micro in ["ingesta_en_hogar", "ingesta_en_restauracion", "interaccion_ingesta"]:
            agente.saciedad = min(100, agente.saciedad + 100)
        elif micro in ["ingesta_ligera", "ingesta_rrss"]:
            agente.saciedad = min(100, agente.saciedad + 40) 
    else:
        # En otras actividades se consume saciedad: más en actividad física
        gasto_saciedad = 20 if micro in ["actividad_fisica", "mantenimiento_del_hogar"] else 15
        agente.saciedad = max(0, agente.saciedad - gasto_saciedad)


def calculate_utilities(agente):
    """
    Calcula deficiencia fisiológica mediante curva exponencial.
    Mayor deficiencia = mayor urgencia de satisfacer necesidad.
    """
    k = agente.urgency_k 
    
    deficit_energia = 100 - agente.energia
    deficit_saciedad = 100 - agente.saciedad
    
    utilidades = {
        "DESCANSO": (deficit_energia / 100.0) ** k,
        "ALIMENTACION": (deficit_saciedad / 100.0) ** k
    }
    
    return utilidades


def get_next_state_with_biology(agente, markov_probabilities, estados_posibles):
    """
    Integra la rutina de la Cadena de Markov (Capa 1) con las urgencias biológicas.
    Devuelve el siguiente macro-estado elegido estocásticamente.
    """
    utilidades = calculate_utilities(agente)
    pesos_combinados = []
    
    for i in range(len(estados_posibles)):
        estado = estados_posibles[i]
        peso_normal = markov_probabilities[i]
        peso_extra = 0
        
        if estado == "DESCANSO":
            peso_extra = utilidades.get("DESCANSO", 0)
        elif estado == "ALIMENTACION":
            peso_extra = utilidades.get("ALIMENTACION", 0)
            
        peso_final = peso_normal + peso_extra
        pesos_combinados.append(peso_final)
        
    suma_total = sum(pesos_combinados)
    if suma_total > 0:
        pesos_combinados = [p / suma_total for p in pesos_combinados]
    else:
        pesos_combinados = [1.0 / len(estados_posibles)] * len(estados_posibles)
        
    siguiente_estado = random.choices(estados_posibles, weights=pesos_combinados, k=1)[0]
    
    return siguiente_estado