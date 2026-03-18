import random
import time
from sentence_transformers import util
import llm_client
import config

def recuperar_memorias(personaje, vector_tema, turno_global):
    """Filtra y puntúa los recuerdos del agente basándose en la fórmula del modelo de Stanford."""
    if not personaje.long_term_memory: 
        return []
        
    resultados = []
    for m in personaje.long_term_memory:
        similitud = util.cos_sim(vector_tema, m["vector"]).item()
        distancia = turno_global - m["recencia"]
        recencia_score = 1.0 / (1.0 + distancia * config.MEMORY_DECAY_FACTOR)
        importancia_score = m["importancia"] / config.MAX_IMPORTANCE_SCORE
        
        score = (similitud * config.WEIGHT_SIMILARITY) + \
                (recencia_score * config.WEIGHT_RECENCY) + \
                (importancia_score * config.WEIGHT_IMPORTANCE)
        resultados.append({"texto": m["texto"], "score": score})
        
    return sorted(resultados, key=lambda x: x["score"], reverse=True)[:config.MAX_RETRIEVED_MEMORIES]

def procesar_encuentro(agente, agentes, motor_semantico, turno_global):
    """Busca compañeros en la misma ubicación y detona el diálogo social mediante LLM."""
    lugar = str(agente.current_location_name).strip()
    
    # Buscamos compañeros usando el motor nativo de objetos de Python
    posibles_companeros = [
        a for a in agentes 
        if a != agente  
        and str(a.current_location_name).strip() == lugar
        and lugar != "Casa"
    ]
    
    if posibles_companeros:
        companero = random.choice(posibles_companeros)
        print(f"\n   👀 ¡Encuentro! {agente.name} coincide con {companero.name} en {lugar}.")
        
        tema_interes = agente.interests
        vector_tema = motor_semantico.encode(tema_interes)
        
        mem_agente = recuperar_memorias(agente, vector_tema, turno_global)
        mem_companero = recuperar_memorias(companero, vector_tema, turno_global)
        
        print(f"   ⏳ El motor social procesa el diálogo sobre '{tema_interes}'...")
        charla_json = llm_client.generate_social_dialogue(agente, companero, mem_agente, mem_companero)
        
        print(f"\n   🎭 TEMA: {charla_json.get('tema_de_conversacion', 'General')}")
        for linea in charla_json.get('dialogo', []):
            print(f"   💬 {linea}")
            time.sleep(config.SLEEP_DIALOGUE)  
        print("   " + "-" * 60 + "\n")
    else:
        print(f"   [🚶‍♂️ {agente.name} miró alrededor en {lugar}, pero no vio a nadie para hablar.]")