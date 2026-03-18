# ==============================================================================
# ARCHIVO: homophily_rules.py
# DESCRIPCIÓN: Cálculo de afinidad entre agentes concurrentes.
# REFERENCIA CIENTÍFICA: Bisgin et al. (2012) "A study of homophily on social media".
# ==============================================================================

def calculate_homophily_score(agent_a, agent_b):
    """
    Calcula la probabilidad de interacción entre dos agentes basándose en la
    similitud de sus atributos (Selección Homofílica).
    Devuelve un booleano (si interactúan o no) y el contexto de por qué.
    """
    score = 0
    match_reasons = []

    # 1. SIMILITUD DEMOGRÁFICA (Edad)
    diferencia_edad = abs(agent_a.age - agent_b.age)
    if diferencia_edad <= 5:
        score += 2
        match_reasons.append("Tienen edades muy similares.")
    elif diferencia_edad <= 10:
        score += 1

    # 2. SIMILITUD PROFESIONAL
    if agent_a.occupation != "unemployed" and agent_a.occupation == agent_b.occupation:
        score += 3
        match_reasons.append(f"Ambos trabajan como {agent_a.occupation}.")

    # 3. SIMILITUD DE INTERESES (La métrica más fuerte)
    set_a = set(agent_a.interests)
    set_b = set(agent_b.interests)
    shared_interests = set_a.intersection(set_b)
    
    if shared_interests:
        puntos_intereses = 2 * len(shared_interests)
        score += puntos_intereses
        intereses_str = ", ".join(shared_interests)
        match_reasons.append(f"Comparten intereses en: {intereses_str}.")

    # 4. SIMILITUD PSICOLÓGICA (Ej: Extraversión compatible)
    soc_a = agent_a.physical_rules.get("Sociability", {}).get("label")
    soc_b = agent_b.physical_rules.get("Sociability", {}).get("label")
    
    if soc_a == "High Surgency" and soc_b == "High Surgency":
        score += 1
        match_reasons.append("Ambos tienen personalidades muy extrovertidas.")

    # --- EVALUACIÓN FINAL ---
    # Fijamos un umbral (Threshold). Por ejemplo, si sacan 3 puntos o más, interactúan.
    THRESHOLD = 3
    interact_flag = score >= THRESHOLD
    
    # Generamos el texto de contexto para la Memoria SQL / LLM
    if interact_flag:
        contexto_llm = "Se han acercado porque " + " ".join(match_reasons)
    else:
        contexto_llm = "Se han ignorado (No hay suficiente afinidad)."

    return interact_flag, score, contexto_llm

# ==========================================
# PRUEBA RÁPIDA (Comprobación del algoritmo)
# ==========================================
if __name__ == "__main__":
    from agent_ingestor import load_agents_from_csv
    
    agentes = load_agents_from_csv("users.csv")
    
    # Vamos a forzar a conocerse al Agente 0 (Aaron) y al Agente 1 (Adam)
    agente_1 = agentes[0]
    agente_2 = agentes[1]
    
    print(f"\n--- TEST DE HOMOFILIA ---")
    print(f"Comparando a {agente_1.name} ({agente_1.age} años, {agente_1.interests})")
    print(f"con {agente_2.name} ({agente_2.age} años, {agente_2.interests})\n")
    
    interactuan, puntuacion, contexto = calculate_homophily_score(agente_1, agente_2)
    
    print(f"Puntuación Final: {puntuacion}")
    print(f"¿Interactúan?: {'SÍ' if interactuan else 'NO'}")
    print(f"Contexto generado para el LLM: {contexto}")