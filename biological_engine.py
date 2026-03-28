import random

def update_biological_needs(agente):
    """
    Actualiza las variables fisiológicas en cada turno usando la CAPA 1 (Macro-estados).
    Dentro de cada estado, se ajusta el gasto usando la CAPA 2 (Micro-acciones).
    Se aplican los multiplicadores de personalidad (Surgency, Conscientiousness, Neuroticism).
    """
    estado = agente.current_macro_state
    micro = agente.current_micro_action
    
    # 1. ENERGÍA (Media matemática esperada: -6 por turno)
    if estado == "DORMIR":
        if micro == "dormir_profundamente":
            agente.energia = min(100, agente.energia + (100 * agente.energy_recovery_mult))
        else: # dormir_siesta
            agente.energia = min(100, agente.energia + (40 * agente.energy_recovery_mult))
    else:
        # Desgaste dinámico pero simplificado (Valores: 4, 6, u 8)
        if micro in ["hacer_ejercicio", "hacer_limpieza", "dar_una_vuelta", "trabajar", "ir_a_clase", "tareas_personales"]:
            gasto_energia = 7  # Alto desgaste
        else: 
            gasto_energia = 5  # Bajo desgaste
            
        agente.energia = max(0, agente.energia - (gasto_energia * agente.energy_decay_mult))

    # 2. SACIEDAD (Media matemática esperada: -18 por turno)
    if estado == "COMER_BEBER":
        if micro in ["comer_en_casa", "comer_fuera_de_casa", "conversar_comiendo"]:
            agente.saciedad = min(100, agente.saciedad + 100)
        elif micro in ["merendar_algo_rapido", "tomar_algo", "usar_rrss_comiendo"]:
            agente.saciedad = min(100, agente.saciedad + 40) 
        
    else:
        if micro in ["hacer_ejercicio", "hacer_limpieza"]:
            gasto_saciedad = 20 # El esfuerzo físico da más hambre
        else:
            gasto_saciedad = 15 # Desgaste normal (trabajar, estudiar, tareas...)
            
        agente.saciedad = max(0, agente.saciedad - gasto_saciedad)


def calculate_utilities(agente):
    """Calcula el estrés fisiológico usando la curva exponencial."""
    k = agente.urgency_k 
    
    deficit_energia = 100 - agente.energia
    deficit_saciedad = 100 - agente.saciedad
    
    utilidades = {
        "DORMIR": (deficit_energia / 100.0) ** k,
        "COMER_BEBER": (deficit_saciedad / 100.0) ** k
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
        
        if estado == "DORMIR":
            peso_extra = utilidades.get("DORMIR", 0)
        elif estado == "COMER_BEBER":
            peso_extra = utilidades.get("COMER_BEBER", 0)
            
        peso_final = peso_normal + peso_extra
        pesos_combinados.append(peso_final)
        
    suma_total = sum(pesos_combinados)
    if suma_total > 0:
        pesos_combinados = [p / suma_total for p in pesos_combinados]
    else:
        pesos_combinados = [1.0 / len(estados_posibles)] * len(estados_posibles)
        
    siguiente_estado = random.choices(estados_posibles, weights=pesos_combinados, k=1)[0]
    
    return siguiente_estado