import random
import time
import llm_client
import config
import homophily_rules

def process_encounter(agent, agents):
    """
    Busca compañeros en la misma ubicación y detona el diálogo social mediante LLM.
    Devuelve True si lograron entablar conversación, o False si fracasaron.
    """
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
                # 5. Generación de CONTEXTO dinámico relacional
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
            
            # [!] NUEVO: INTERRUPCIÓN COGNITIVA
            # Sobrescribimos el estado mental del compañero para que sepa que está charlando
            companion.secondary_state = "CONVERSAR"
            
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
            # FASE 2: EL GUIONISTA LLM (ENRIQUECIDO PHYCHITAL)
            # =====================================================================
            if config.PRINT_LOGS:
                print(f"   El motor social procesa el diálogo...")
            
            # [!] NUEVO: CONTEXTO PHYCHITAL
            # Le explicamos a Gemini el entorno exacto y lo que están haciendo físicamente
            contexto_phygital = (
                f"{context} Además, debes saber que actualmente se encuentran físicamente en "
                f"el lugar llamado '{location}'. Mientras conversan, {agent.name} está realizando la "
                f"acción física de '{agent.primary_state}', y {companion.name} está haciendo '{companion.primary_state}'."
            )
            
            # Le pasamos a Gemini directamente los párrafos de largo plazo actualizados y el contexto rico
            dialogue_json = llm_client.generate_social_dialogue(
                agent, companion, 
                agent.long_term_memory, 
                companion.long_term_memory, 
                contexto_phygital 
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
                
            return True # ¡Éxito! Lograron hablar.
                
        else:
            # Coincidieron físicamente, pero se cayeron mal o falló la probabilidad
            if config.PRINT_LOGS:
                print(f"   [ {agent.name} vio gente en {location}, pero a nadie con quien poder hablar.]")
            return False 
    else:
        # No había literalmente nadie en ese lugar
        if config.PRINT_LOGS:
            print(f"   [ {agent.name} miró alrededor en {location}, pero no vio a nadie en absoluto.]")
        return False