import random
import time
from sentence_transformers import util
import llm_client
import config
import homophily_rules

def retrieve_memories(agent, topic_vector, global_turn):
    """Filtra y puntúa los recuerdos del agente basándose en la fórmula del modelo de Stanford."""
    if not agent.long_term_memory: 
        return []
        
    results = []
    for m in agent.long_term_memory:
        
        # CALCULO DE RELEVANCIA DE CADA RECUERDO, topic_vector son los intereses de la gente y m es un recuerdo individual
        similarity = util.cos_sim(topic_vector, m["vector"]).item() #item() para obtener el valor numérico solamente.
        distance = global_turn - m["recencia"]
        recency_score = 1.0 / (1.0 + distance * config.MEMORY_DECAY_FACTOR)
        importance_score = m["importancia"] / config.MAX_IMPORTANCE_SCORE
        
        score = (similarity * config.WEIGHT_SIMILARITY) + \
                (recency_score * config.WEIGHT_RECENCY) + \
                (importance_score * config.WEIGHT_IMPORTANCE)
        results.append({"texto": m["texto"], "score": score})
        
    return sorted(results, key=lambda x: x["score"], reverse=True)[:config.MAX_RETRIEVED_MEMORIES]

def process_encounter(agent, agents, semantic_engine, global_turn):
    """Busca compañeros en la misma ubicación y detona el diálogo social mediante LLM."""
    location = str(agent.current_location_name).strip()
    
    # Buscamos a todas las personas en la misma sala
    potential_companions = [
        a for a in agents 
        if a != agent  
        and str(a.current_location_name).strip() == location
        and location != "Casa"
    ]
    
    if potential_companions:
        valid_companions = []
        
        # EL FILTRO DE HOMOFILIA: Evaluamos a todos los candidatos
        for a in potential_companions:
            interactuan, puntuacion, contexto = homophily_rules.calculate_homophily_score(agent, a)
            if interactuan:
                valid_companions.append((a, puntuacion, contexto))
                
        # Si después de evaluar a todos, alguien superó el Threshold de config.py
        if valid_companions:
            # Ordenamos la lista para hablar con el que tenga mayor puntuación (mejor match)
            valid_companions.sort(key=lambda x: x[1], reverse=True)
            companion, score, context = valid_companions[0] 
            
            print(f"\n   ¡Encuentro! {agent.name} coincide con {companion.name} en {location}.")
            print(f"   Afinidad: {score} pts. {context}")
            
            # =====================================================================
            # FASE 1: CREACIÓN DE REFLEXIÓN (Sin similitud, usando solo el Top 5)
            # =====================================================================
            print(f"   Los agentes ordenan su mente antes de hablar...")
            for participante in [agent, companion]:
                # Como bien has apuntado, ya no pasamos el turno_global, solo el limit=5
                top_acciones = participante.get_top_recent_actions(limit=5)
                
                if top_acciones: # Si el búfer no está vacío
                    reflexion_json = llm_client.generate_daily_reflection(participante, top_acciones)
                    if reflexion_json:
                        # Vectorizamos y guardamos la reflexión en el disco duro a largo plazo
                        vector = semantic_engine.encode(reflexion_json["resumen_narrativo"])
                        participante.save_reflection(reflexion_json, vector, global_turn)

            # =====================================================================
            # FASE 2: RECUPERACIÓN DEL PASADO (Con fórmula de similitud)
            # =====================================================================
            # CAMBIO CLAVE: Ya no buscamos los intereses generales del agente,
            # buscamos en la memoria usando el "context" del encuentro como vector
            interest_topic = context 
            topic_vector = semantic_engine.encode(interest_topic)
            
            agent_memories = retrieve_memories(agent, topic_vector, global_turn)
            companion_memories = retrieve_memories(companion, topic_vector, global_turn)
            
            # =====================================================================
            # FASE 3: EL GUIONISTA LLM
            # =====================================================================
            print(f"   El motor social procesa el diálogo...")
            
            # CAMBIO CLAVE: Añadimos 'agent.last_reflection' y 'companion.last_reflection'
            # para inyectarle al prompt cómo se sienten exactamente en este momento
            dialogue_json = llm_client.generate_social_dialogue(
                agent, companion, 
                agent.last_reflection, companion.last_reflection, 
                agent_memories, companion_memories, context
            )

            print(f"\n TEMA: {dialogue_json.get('tema_de_conversacion', 'General')}")
            for line in dialogue_json.get('dialogo', []):
                print(f"    {line}")
                time.sleep(config.SLEEP_DIALOGUE)  
            print("   " + "-" * 60 + "\n")
        else:
            # Coincidieron físicamente, pero se cayeron mal
            print(f"   [ {agent.name} vio gente en {location}, pero a nadie con quien poder hablar.]")
    else:
        print(f"   [ {agent.name} miró alrededor en {location}, pero no vio a nadie en absoluto.]")