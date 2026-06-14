import random
import config

def update_biological_needs(agente):
    """
    Actualiza energía y saciedad según el estado y acción del agente.
    Aplica multiplicadores de personalidad a consumo y recuperación.
    """
    estado = agente.current_macro_state
    micro = agente.current_micro_action
    
    # Actualizar energía según estado
    if estado == "DESCANSO":
        if micro == "sueno_profundo":
            agente.energia = min(config.MAX_BIOLOGICAL_LEVEL, agente.energia + (config.ENERGY_RECOVERY_DEEP_SLEEP * agente.energy_recovery_mult))
        else:  # descanso_diurno
            agente.energia = min(config.MAX_BIOLOGICAL_LEVEL, agente.energia + (config.ENERGY_RECOVERY_LIGHT_REST * agente.energy_recovery_mult))
    else:
        acciones_alto_desgaste = ["actividad_fisica", "mantenimiento_del_hogar", "paseo_recreativo", 
                                  "jornada_laboral", "jornada_academica", "gestiones_personales"]
        gasto_energia = config.ENERGY_DECAY_HIGH if micro in acciones_alto_desgaste else config.ENERGY_DECAY_NORMAL
        agente.energia = max(0, agente.energia - (gasto_energia * agente.energy_decay_mult))

    # Actualizar saciedad según estado
    if estado == "ALIMENTACION":
        if micro in ["ingesta_en_hogar", "ingesta_en_restauracion", "interaccion_ingesta"]:
            agente.saciedad = min(config.MAX_BIOLOGICAL_LEVEL, agente.saciedad + config.SATIETY_RECOVERY_FULL)
        elif micro in ["ingesta_ligera", "ingesta_rrss"]:
            agente.saciedad = min(config.MAX_BIOLOGICAL_LEVEL, agente.saciedad + config.SATIETY_RECOVERY_LIGHT) 
    else:
        gasto_saciedad = config.SATIETY_DECAY_HIGH if micro in ["actividad_fisica", "mantenimiento_del_hogar"] else config.SATIETY_DECAY_NORMAL
        agente.saciedad = max(0, agente.saciedad - gasto_saciedad)

def calculate_utilities(agente):
    # [INTERRUPTOR DE LABORATORIO] 
    # Si FORCE_URGENCY_K está en config, ignora la psicología del agente.
    k_global = getattr(config, 'FORCE_URGENCY_K', None)
    k = k_global if k_global is not None else agente.urgency_k 
    
    deficit_energia = config.MAX_BIOLOGICAL_LEVEL - agente.energia
    deficit_saciedad = config.MAX_BIOLOGICAL_LEVEL - agente.saciedad
    
    utilidades = {
        "DESCANSO": (deficit_energia / float(config.MAX_BIOLOGICAL_LEVEL)) ** k,
        "ALIMENTACION": (deficit_saciedad / float(config.MAX_BIOLOGICAL_LEVEL)) ** k
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