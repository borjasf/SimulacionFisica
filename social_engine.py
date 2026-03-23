import random
import time
from sentence_transformers import util
import llm_client
import config
import homophily_rules

""" def retrieve_memories(agent, topic_vector, global_turn):
    Filtra y puntúa los recuerdos del agente basándose en la fórmula del modelo de Stanford.
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
        
    return sorted(results, key=lambda x: x["score"], reverse=True)[:config.MAX_RETRIEVED_MEMORIES]"""

def process_encounter(agent, agents):
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
        
        # EL FILTRO DE HOMOFILIA, PROBABILIDAD Y AMISTAD
        for a in potential_companions:
            son_amigos = str(a.id) in agent.amigos
            
            # 1. Extraemos los intereses en común (si los hay)
            int_a = set([i.strip().lower() for i in agent.interests.split(',')])
            int_b = set([i.strip().lower() for i in a.interests.split(',')])
            shared = int_a.intersection(int_b)
            
            # 2. Calculamos la puntuación bruta de homofilia 
            _, puntuacion, _ = homophily_rules.calculate_homophily_score(agent, a)
            
            # 3. Asignamos la PROBABILIDAD de interactuar
            if son_amigos:
                probabilidad = config.FRIEND_INTERACTION_PROB  # Probabilidad alta para amigos
                puntuacion += config.FRIEND_PRIORITY_BONUS    # Subimos su nota para que gane si hay varias personas
            else:
                prob_calculada = puntuacion * config.HOMOPHILY_PROB_MULTIPLIER
                probabilidad = max(config.MIN_INTERACTION_PROB, min(config.MAX_INTERACTION_PROB, prob_calculada))
                
            # 4. Tiramos los dados virtuales
            interactuan = random.random() < probabilidad
            
            if interactuan:
                # 5. Generación de CONTEXTO dinámico
                if son_amigos:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Son amigos. Quieren ponerse al día y hablar sobre su interés común en {temas}."
                    else:
                        contexto = "Son amigos. Quieren ponerse al día sobre cómo les va la vida."
                else:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Se acaban de conocer. Han descubierto que tienen en común: {temas}."
                    else:
                        contexto = "Se acaban de conocer por primera vez. Están charlando para presentarse."
                        
                valid_companions.append((a, puntuacion, contexto))

                
        # Si después de evaluar a todos, alguien superó los filtros
        if valid_companions:
            # Ordenamos la lista para hablar con el que tenga mayor puntuación (mejor match)
            valid_companions.sort(key=lambda x: x[1], reverse=True)
            companion, score, context = valid_companions[0] 
            
            # BLOQUEO DE PRINTS
            if config.PRINT_LOGS:
                print(f"\n   ¡Encuentro! {agent.name} coincide con {companion.name} en {location}.")
                print(f"   Afinidad: {score} pts. {context}")
                print(f"   Los agentes ordenan su mente antes de hablar...")
            
            # =====================================================================
            # FASE 1: ACTUALIZACIÓN DE MEMORIA A LARGO PLAZO (LLM-Centric)
            # =====================================================================
            for participante in [agent, companion]:
                # Extraemos TODA la lista cronológica de acciones cortas y vaciamos el búfer
                acciones_recientes = participante.flush_short_term_memory()
                
                if acciones_recientes: # Solo gasta tokens de API si han hecho cosas nuevas
                    if config.PRINT_LOGS:
                        print(f"   [{participante.name} sintetizando sus recuerdos...]")
                    
                    # Gemini unifica la memoria antigua y la reciente en un nuevo párrafo de vida
                    nueva_reflexion = llm_client.generate_long_term_memory(participante, acciones_recientes)
                    
                    if nueva_reflexion:
                        participante.update_long_term_memory(nueva_reflexion)

            # =====================================================================
            # FASE 2: ELIMINADA (Ya no hay embeddings ni búsqueda vectorial)
            # =====================================================================

            # =====================================================================
            # FASE 3: EL GUIONISTA LLM
            # =====================================================================
            if config.PRINT_LOGS:
                print(f"   El motor social procesa el diálogo...")
            
            # Le pasamos a Gemini directamente los párrafos de largo plazo actualizados
            dialogue_json = llm_client.generate_social_dialogue(
                agent, companion, 
                agent.long_term_memory, 
                companion.long_term_memory, 
                context
            )

            # NUEVA LÓGICA: SE HACEN AMIGOS TRAS HABLAR
            if str(companion.id) not in agent.amigos:
                agent.amigos.append(str(companion.id))
            if str(agent.id) not in companion.amigos:
                companion.amigos.append(str(agent.id))

            # BLOQUEO DE PRINTS Y SLEEP
            if config.PRINT_LOGS:
                print(f"\n TEMA: {dialogue_json.get('tema_de_conversacion', 'General')}")
                for line in dialogue_json.get('dialogo', []):
                    print(f"    {line}")
                    time.sleep(config.SLEEP_DIALOGUE)  
                print("   " + "-" * 60 + "\n")
                
        else:
            # Coincidieron físicamente, pero se cayeron mal
            if config.PRINT_LOGS:
                print(f"   [ {agent.name} vio gente en {location}, pero a nadie con quien poder hablar.]")
    else:
        if config.PRINT_LOGS:
            print(f"   [ {agent.name} miró alrededor en {location}, pero no vio a nadie en absoluto.]")