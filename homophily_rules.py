import config

def calculate_homophily_score(agent_a, agent_b):
    """
    Calcula la probabilidad de interacción entre dos agentes basándose en la
    similitud de sus atributos (Selección Homofílica equiponderada).
    Devuelve los puntos totales y el contexto narrativo.
    """
    score = 0
    match_reasons = []

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

    # 3. SIMILITUD DE INTERESES (Se piensa que en implementaciones futuras pueden haber más de 1 interés por persona)
    intereses_a = set([i.strip().lower() for i in agent_a.interests.split(',')])
    intereses_b = set([i.strip().lower() for i in agent_b.interests.split(',')])
    
    shared_interests = intereses_a.intersection(intereses_b)
    
    if shared_interests:
        # 1 punto por CADA interés compartido. A más intereses, más puntuación natural.
        score += len(shared_interests) 
        intereses_str = ", ".join(shared_interests)
        match_reasons.append(f"Comparten intereses en: {intereses_str}.")

    # 4. SIMILITUD PSICOLÓGICA
    # Solo suma si AMBOS tienen el rasgo +
    
    # Sociability: +1 solo si ambos
    if "Sociability +" in agent_a.traits and "Sociability +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos tienen personalidades extrovertidas y sociables.")

    # Friendliness: +1 solo si ambos
    if "Friendliness +" in agent_a.traits and "Friendliness +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos tienen actitud amable y cooperativa.")

    # Intellectual: +1 solo si ambos
    if "Intellectual +" in agent_a.traits and "Intellectual +" in agent_b.traits:
        score += 1
        match_reasons.append("Comparten curiosidad intelectual e interés por aprender.")

    # EVALUACIÓN FINAL
    if match_reasons:
        contexto_llm = "Se han acercado porque " + " ".join(match_reasons)
    else:
        contexto_llm = "No tienen nada obvio en común, pero se han puesto a hablar por casualidad."

    # Nota: El score puede ser negativo. Se usa para calcular probabilidad de interacción.
    # En social_engine.py se clampea entre 0.05 (MIN) y 0.95 (MAX)
    return score, contexto_llm