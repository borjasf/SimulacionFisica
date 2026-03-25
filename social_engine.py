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
    
    # 1. Buscamos a personas en la misma ubicación física
    # Si están en "Casa", comprobamos que compartan las mismas coordenadas (viven juntos)
    potential_companions = [
        a for a in agents 
        if a != agent  
        and str(a.current_location_name).strip() == location
        and (location != "Casa" or a.home_coords == agent.home_coords)
    ]
    
    if potential_companions:
        valid_companions = []
        
        # EL FILTRO DE HOMOFILIA, PROBABILIDAD Y AMISTAD
        for a in potential_companions:
            son_amigos = str(a.id) in agent.amigos
            
            # Extraemos los intereses en común (si los hay)
            int_a = set([i.strip().lower() for i in agent.interests.split(',')])
            int_b = set([i.strip().lower() for i in a.interests.split(',')])
            shared = int_a.intersection(int_b)
            
            # Calculamos la puntuación bruta de homofilia 
            _, puntuacion, _ = homophily_rules.calculate_homophily_score(agent, a)
            
            # Asignamos la PROBABILIDAD de interactuar
            if son_amigos:
                probabilidad = config.FRIEND_INTERACTION_PROB  
                puntuacion += config.FRIEND_PRIORITY_BONUS    
            else:
                prob_calculada = puntuacion * config.HOMOPHILY_PROB_MULTIPLIER
                probabilidad = max(config.MIN_INTERACTION_PROB, min(config.MAX_INTERACTION_PROB, prob_calculada))
                
            # Tiramos los dados virtuales
            interactuan = random.random() < probabilidad
            
            if interactuan:
                # Generación de CONTEXTO dinámico relacional
                if son_amigos:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Son amigos y viven juntos. Quieren ponerse al día y hablar sobre su interés común en {temas}."
                    else:
                        contexto = "Son amigos y compañeros de casa. Quieren ponerse al día sobre cómo les va la vida."
                else:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Comparten piso pero no son muy amigos aún. Tienen en común: {temas}."
                    else:
                        contexto = "Son compañeros de piso charlando de forma casual en casa."
                        
                valid_companions.append((a, puntuacion, contexto))

                
        # Si después de evaluar a todos, alguien superó los filtros
        if valid_companions:
            # Ordenamos la lista para hablar con el que tenga mayor puntuación (mejor match)
            valid_companions.sort(key=lambda x: x[1], reverse=True)
            companion, score, context = valid_companions[0] 
            
            # INTERRUPCIÓN COGNITIVA
            companion.secondary_state = "CONVERSAR"
            
            if config.PRINT_LOGS:
                print(f"\n   ¡Encuentro! {agent.name} coincide con {companion.name} en {location}.")
                print(f"   Afinidad: {score} pts. {context}")
                print(f"   Los agentes ordenan su mente antes de hablar...")
            
            # FASE 1: ACTUALIZACIÓN DE MEMORIA A LARGO PLAZO

            for participante in [agent, companion]:
                # 1. Copiamos la lista de acciones sin vaciar el búfer original
                acciones_recientes = list(participante.short_term_memory)
                
                if acciones_recientes: 
                    if config.PRINT_LOGS:
                        print(f"   [{participante.name} sintetizando sus recuerdos...]")
                    
                    # 2. Llamamos a la API
                    nueva_reflexion = llm_client.generate_long_term_memory(participante, acciones_recientes)
                    
                    # 3. Validamos el éxito: En llm_client.py, si falla devuelve la memoria antigua.
                    # Por tanto, si la nueva reflexión es diferente a la antigua, la API funcionó bien.
                    if nueva_reflexion and nueva_reflexion != participante.long_term_memory:
                        participante.update_long_term_memory(nueva_reflexion)
                        
                        # 4. SOLO AHORA vaciamos los recuerdos a corto plazo
                        participante.short_term_memory.clear()
                    else:
                        if config.PRINT_LOGS:
                            print(f"   [!] Error de red. {participante.name} retendrá sus recuerdos a corto plazo para más adelante.")

            # FASE 2: EL LLM
            if config.PRINT_LOGS:
                print(f"   El motor social procesa el diálogo...")
            
            contexto_phygital = (
                f"{context} Además, debes saber que actualmente se encuentran físicamente en "
                f"el lugar llamado '{location}'. Mientras conversan, {agent.name} está realizando la "
                f"acción física de '{agent.primary_state}', y {companion.name} está haciendo '{companion.primary_state}'."
            )
            
            dialogue_json = llm_client.generate_social_dialogue(
                agent, companion, 
                agent.long_term_memory, 
                companion.long_term_memory, 
                contexto_phygital 
            )

            # SE HACEN AMIGOS TRAS HABLAR
            if str(companion.id) not in agent.amigos:
                agent.amigos.append(str(companion.id))
            if str(agent.id) not in companion.amigos:
                companion.amigos.append(str(agent.id))

            if config.PRINT_LOGS:
                print(f"\n TEMA: {dialogue_json.get('tema_de_conversacion', 'General')}")
                for line in dialogue_json.get('dialogo', []):
                    print(f"    {line}")
                    time.sleep(config.SLEEP_DIALOGUE)  
                print("   " + "-" * 60 + "\n")
                
            return True 
                
        else:
            if config.PRINT_LOGS:
                print(f"   [ {agent.name} vio a sus convivientes en {location}, pero nadie estaba libre o de humor para hablar.]")
            return False 
    else:
        if config.PRINT_LOGS:
            print(f"   [ {agent.name} miró alrededor en {location}, pero no había nadie con quien charlar.]")
        return False