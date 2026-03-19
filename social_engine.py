import random
import time
from sentence_transformers import util
import llm_client
import config

def retrieve_memories(agent, topic_vector, global_turn):
    """Filtra y puntúa los recuerdos del agente basándose en la fórmula del modelo de Stanford."""
    if not agent.long_term_memory: 
        return []
        
    results = []
    for m in agent.long_term_memory:
        
        similarity = util.cos_sim(topic_vector, m["vector"]).item()
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
    
    # Buscamos compañeros usando el motor nativo de objetos de Python
    potential_companions = [
        a for a in agents 
        if a != agent  
        and str(a.current_location_name).strip() == location
        and location != "Casa"
    ]
    
    if potential_companions:
        companion = random.choice(potential_companions)
        print(f"\n  ¡Encuentro! {agent.name} coincide con {companion.name} en {location}.")
        
        interest_topic = agent.interests
        topic_vector = semantic_engine.encode(interest_topic)
        
        agent_memories = retrieve_memories(agent, topic_vector, global_turn)
        companion_memories = retrieve_memories(companion, topic_vector, global_turn)
        
        print(f"   El motor social procesa el diálogo sobre '{interest_topic}'...")
        dialogue_json = llm_client.generate_social_dialogue(agent, companion, agent_memories, companion_memories)
        
        print(f"\n  TEMA: {dialogue_json.get('tema_de_conversacion', 'General')}")
        for line in dialogue_json.get('dialogo', []):
            print(f"   {line}")
            time.sleep(config.SLEEP_DIALOGUE)  
        print("   " + "-" * 60 + "\n")
    else:
        print(f"   [{agent.name} miró alrededor en {location}, pero no vio a nadie para hablar.]")