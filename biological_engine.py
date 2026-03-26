import random

def update_biological_needs(agente):
    """
    Actualiza las variables fisiológicas en cada turno usando la CAPA 1 (Macro-estados).
    Se aplican los multiplicadores de personalidad (Surgency, Conscientiousness, Neuroticism).
    """
    estado = agente.current_macro_state
    
    # 1. ENERGÍA 
    if estado == "DORMIR":
        agente.energia = min(100, agente.energia + (100 * agente.energy_recovery_mult))
    elif estado in ["TRABAJAR_ESTUDIAR", "OCIO"]:
        # El trabajo y el ocio fuera de casa gastan más energía
        agente.energia = max(0, agente.energia - (10 * agente.energy_decay_mult))
    else:
        # Estar en CASA o COMER_BEBER desgasta menos
        agente.energia = max(0, agente.energia - (5 * agente.energy_decay_mult))

    # 2. SACIEDAD 
    if estado == "COMER_BEBER":
        agente.saciedad = min(100, agente.saciedad + 100)
    else:
        agente.saciedad = max(0, agente.saciedad - 10)


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