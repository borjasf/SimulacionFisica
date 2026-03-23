import config

def calculate_homophily_score(agent_a, agent_b):
    """
    Calcula la probabilidad de interacción entre dos agentes basándose en la
    similitud de sus atributos (Selección Homofílica equiponderada).
    Devuelve un booleano, los puntos totales y el contexto narrativo.
    """
    score = 0
    match_reasons = []

    # 0. BONUS DE PERSONALIDAD (Amiability / Sociability)
    # El bonus fraccional proviene directamente de los multiplicadores 
    # de Goldberg matemáticos generados en trait_rules, no de una decisión arbitraria.
    bonus_a = agent_a.homophily_base_bonus / 10.0 
    bonus_b = agent_b.homophily_base_bonus / 10.0
    score += (bonus_a + bonus_b)
    
    if bonus_a > 0 or bonus_b > 0:
        match_reasons.append("Su carácter abierto facilitó el acercamiento.")

    # 1. SIMILITUD DEMOGRÁFICA (Edad)
    diferencia_edad = abs(agent_a.age - agent_b.age)
    if diferencia_edad <= 10:
        score += 1
        if diferencia_edad <= 5:
            score += 1  # Bonus extra si la edad es muy similar
            match_reasons.append("Tienen edades muy similares.")
        else:
            match_reasons.append("Tienen edades similares.")

    # 2. SIMILITUD PROFESIONAL
    if agent_a.occupation.lower() != "unemployed" and agent_a.occupation.lower() == agent_b.occupation.lower():
        score += 1
        match_reasons.append(f"Ambos trabajan en el ámbito de {agent_a.occupation}.")

    # 3. SIMILITUD DE INTERESES 
    intereses_a = set([i.strip().lower() for i in agent_a.interests.split(',')])
    intereses_b = set([i.strip().lower() for i in agent_b.interests.split(',')])
    
    shared_interests = intereses_a.intersection(intereses_b)
    
    if shared_interests:
        # 1 punto por CADA interés compartido. A más intereses, más puntuación natural.
        score += len(shared_interests) 
        intereses_str = ", ".join(shared_interests)
        match_reasons.append(f"Comparten intereses en: {intereses_str}.")

    # 4. SIMILITUD PSICOLÓGICA
    if "Sociability +" in agent_a.traits and "Sociability +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos tienen personalidades muy extrovertidas y sociables.")

    # EVALUACIÓN FINAL
    if match_reasons:
        contexto_llm = "Se han acercado porque " + " ".join(match_reasons)
    else:
        contexto_llm = "No tienen nada obvio en común, pero se han puesto a hablar por casualidad."

    return True, score, contexto_llm