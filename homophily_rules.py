import config

def calculate_homophily_score(agent_a, agent_b):
    """
    Calcula compatibilidad entre dos agentes considerando similitud de atributos.
    Retorna puntuación total y razones de compatibilidad.
    """
    score = 0
    match_reasons = []

    # Similitud de edad: +1 si diferencia <10 años, +1 extra si <5 años
    age_diff = abs(agent_a.age - agent_b.age)
    if age_diff <= 10:
        score += 1
        if age_diff <= 5:
            score += 1
            match_reasons.append("Tienen edades muy similares.")
        else:
            match_reasons.append("Tienen edades similares.")

    # Similitud ocupacional: +1 si trabajan en mismo ámbito
    if agent_a.occupation.lower() != "unemployed" and agent_a.occupation.lower() == agent_b.occupation.lower():
        score += 1
        match_reasons.append(f"Ambos trabajan en {agent_a.occupation}.")

    # Intereses compartidos: 1 punto por cada interés común
    interests_a = set([i.strip().lower() for i in agent_a.interests.split(',')])
    interests_b = set([i.strip().lower() for i in agent_b.interests.split(',')])
    
    shared_interests = interests_a.intersection(interests_b)
    
    if shared_interests:
        score += len(shared_interests) 
        interests_str = ", ".join(shared_interests)
        match_reasons.append(f"Comparten intereses: {interests_str}.")

    # Similitud psicológica: +1 por cada rasgo positivo compartido
    if "Sociability +" in agent_a.traits and "Sociability +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos extrovertidos y sociables.")

    if "Friendliness +" in agent_a.traits and "Friendliness +" in agent_b.traits:
        score += 1
        match_reasons.append("Ambos amables y cooperativos.")

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