import random

def update_biological_needs(agente):
    """
    Actualiza las variables fisiológicas en cada turno.
    Se aplican los multiplicadores de personalidad (Surgency, Conscientiousness, Neuroticism).
    Solo se evalúan Energía y Saciedad.
    """
    estado = agente.current_state
    
    # 1. ENERGÍA 
    if estado == "DORMIR":
        agente.energia = min(100, agente.energia + (100 * agente.energy_recovery_mult))
    elif estado in ["TRABAJAR_ESTUDIAR", "OCIO_INDIVIDUAL", "INACTIVO_TAREAS_CASA"]:
        agente.energia = max(0, agente.energia - (4 * agente.energy_decay_mult))
    else:
        # Para relax, rrss, ocio social, comer... el desgaste es mínimo
        agente.energia = max(0, agente.energia - (2 * agente.energy_decay_mult))

    # 2. SACIEDAD 
    if estado == "COMER_BEBER":
        agente.saciedad = min(100, agente.saciedad + 80)
    else:
        agente.saciedad = max(0, agente.saciedad - 10)


def calculate_utilities(agente):
    """
    Calcula el estrés fisiológico usando la curva exponencial.
    La agresividad de la curva (k) depende de la personalidad.
    """
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
    Integra la rutina de la Cadena de Markov con las urgencias biológicas.
    Devuelve el siguiente estado elegido estocásticamente.
    """
    utilidades = calculate_utilities(agente)
    pesos_combinados = []
    
    # Recorremos la fila de probabilidades de la matriz de Markov
    for i in range(len(estados_posibles)):
        estado = estados_posibles[i]
        peso_normal = markov_probabilities[i]
        peso_extra = 0
        
        # Leemos si la biología exige que el agente transicione a este estado
        if estado == "DORMIR":
            peso_extra = utilidades.get("DORMIR", 0)
        elif estado == "COMER_BEBER":
            peso_extra = utilidades.get("COMER_BEBER", 0)
            
        # El peso final en la ruleta es la suma del hábito (Markov) + necesidad (Biología)
        peso_final = peso_normal + peso_extra
        pesos_combinados.append(peso_final)
        
    # Normalizamos los pesos para evitar desajustes en la función random.choices
    suma_total = sum(pesos_combinados)
    if suma_total > 0:
        pesos_combinados = [p / suma_total for p in pesos_combinados]
    else:
        # Fallback de seguridad si algo falla
        pesos_combinados = [1.0 / len(estados_posibles)] * len(estados_posibles)
        
    # Lanzamos el dado estocástico con los pesos adulterados
    siguiente_estado = random.choices(estados_posibles, weights=pesos_combinados, k=1)[0]
    
    return siguiente_estado