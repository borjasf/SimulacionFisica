import config

def calculate_homophily_score(agent_a, agent_b):
    """
    Calcula la probabilidad de interacción entre dos agentes basándose en la
    similitud de sus atributos (Selección Homofílica).
    Devuelve un booleano (si interactúan o no) y el contexto de por qué.
    """
    score = 0
    match_reasons = []

    # 0. BONUS DE PERSONALIDAD (Amiability / Sociability)
    # Los agentes extrovertidos/amables parten con ventaja para conocer gente
    bonus_a = agent_a.homophily_base_bonus / 10.0 # Escalamos el bonus para no romper el umbral
    bonus_b = agent_b.homophily_base_bonus / 10.0
    score += (bonus_a + bonus_b)
    
    if bonus_a > 0 or bonus_b > 0:
        match_reasons.append("Su carácter abierto facilitó el acercamiento.")

    # 1. SIMILITUD DEMOGRÁFICA (Edad)
    diferencia_edad = abs(agent_a.age - agent_b.age)
    if diferencia_edad <= 5:
        score += 2
        match_reasons.append("Tienen edades muy similares.")
    elif diferencia_edad <= 10:
        score += 1

    # 2. SIMILITUD PROFESIONAL
    if agent_a.occupation.lower() != "unemployed" and agent_a.occupation.lower() == agent_b.occupation.lower():
        score += 3
        match_reasons.append(f"Ambos trabajan en el ámbito de {agent_a.occupation}.")

    # 3. SIMILITUD DE INTERESES (La métrica más fuerte)
    # Convertimos los strings de intereses ("Deportes, Lectura") en conjuntos limpios
    intereses_a = set([i.strip().lower() for i in agent_a.interests.split(',')])
    intereses_b = set([i.strip().lower() for i in agent_b.interests.split(',')])
    
    shared_interests = intereses_a.intersection(intereses_b)
    
    if shared_interests:
        puntos_intereses = 2 * len(shared_interests)
        score += puntos_intereses
        intereses_str = ", ".join(shared_interests)
        match_reasons.append(f"Comparten intereses en: {intereses_str}.")

    # 4. SIMILITUD PSICOLÓGICA (Ej: Extraversión compatible)
    if "Sociability +" in agent_a.traits and "Sociability +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos tienen personalidades muy extrovertidas y sociables.")

    # --- EVALUACIÓN FINAL ---
    # Ya no uso THRESHOLD rígido. Devolvemos los puntos y dejamos que social_engine calcule la probabilidad.
    if match_reasons:
        contexto_llm = "Se han acercado porque " + " ".join(match_reasons)
    else:
        contexto_llm = "No tienen nada obvio en común, pero se han puesto a hablar por casualidad."

    # Devolvemos True por defecto (el filtro real lo pasa social_engine), la puntuación y el texto.
    return True, score, contexto_llm