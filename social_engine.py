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
    
    potential_companions = [
        a for a in agents 
        if a != agent  
        and str(a.current_location_name).strip() == location
        and (location != "Casa" or a.home_coords == agent.home_coords)
    ]
    
    if potential_companions:
        valid_companions = []
        
        for a in potential_companions:
            son_amigos = str(a.id) in agent.amigos
            
            int_a = set([i.strip().lower() for i in agent.interests.split(',')])
            int_b = set([i.strip().lower() for i in a.interests.split(',')])
            shared = int_a.intersection(int_b)
            
            _, puntuacion, _ = homophily_rules.calculate_homophily_score(agent, a)
            
            if son_amigos:
                probabilidad = config.FRIEND_INTERACTION_PROB  
                puntuacion += config.FRIEND_PRIORITY_BONUS    
            else:
                prob_calculada = puntuacion * config.HOMOPHILY_PROB_MULTIPLIER
                probabilidad = max(config.MIN_INTERACTION_PROB, min(config.MAX_INTERACTION_PROB, prob_calculada))
                
            interactuan = random.random() < probabilidad
            
            if interactuan:
                if son_amigos:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Son amigos y viven juntos. Quieren ponerse al día y hablar sobre su interés común en {temas}." if location == "Casa" else f"Son amigos. Quieren ponerse al día y hablar sobre su interés común en {temas}."
                    else:
                        contexto = "Son amigos y compañeros de casa. Quieren ponerse al día sobre cómo les va la vida." if location == "Casa" else "Son amigos poniéndose al día de forma casual."
                else:
                    if shared:
                        temas = ", ".join(shared)
                        contexto = f"Comparten piso pero no son muy amigos aún. Tienen en común: {temas}." if location == "Casa" else f"Se acaban de cruzar y no tienen mucha confianza, pero a ambos les gusta: {temas}."
                    else:
                        contexto = "Son compañeros de piso charlando de forma casual en casa." if location == "Casa" else "Son conocidos teniendo una charla casual."
                        
                valid_companions.append((a, puntuacion, contexto))

        if valid_companions:
            valid_companions.sort(key=lambda x: x[1], reverse=True)
            companion, score, context = valid_companions[0] 
            
            # INTERRUPCIÓN COGNITIVA FASE 2
            # Guardamos qué hacían para dárselo de contexto al LLM
            agent_action = agent.current_micro_action.replace('_', ' ')
            companion_previous_action = companion.current_micro_action.replace('_', ' ')
            
            # Forzamos la micro-acción del compañero a "conversar" para alinear las estadísticas
            companion.current_micro_action = agent.current_micro_action    
                    
            if config.PRINT_LOGS:
                print(f"\n   ¡Encuentro! {agent.name} coincide con {companion.name} en {location}.")
                print(f"   Afinidad: {score} pts. {context}")
                print(f"   Los agentes ordenan su mente antes de hablar...")
            
            # FASE 1: ACTUALIZACIÓN DE MEMORIA A LARGO PLAZO
            for participante in [agent, companion]:
                acciones_recientes = list(participante.action_buffer)
                
                if acciones_recientes: 
                    if config.PRINT_LOGS:
                        print(f"   [{participante.name} sintetizando sus recuerdos...]")
                    
                    nueva_reflexion = llm_client.generate_long_term_memory(participante, acciones_recientes)
                    
                    if nueva_reflexion and nueva_reflexion != participante.long_term_memory:
                        participante.update_long_term_memory(nueva_reflexion)
                        participante.action_buffer.clear()
                    else:
                        if config.PRINT_LOGS:
                            print(f"   [!] Error de red. {participante.name} retendrá sus recuerdos a corto plazo para más adelante.")

            # FASE 2: EL LLM
            if config.PRINT_LOGS:
                print(f"   El motor social procesa el diálogo...")
            
            contexto_phygital = (
                f"{context} Además, debes saber que actualmente se encuentran físicamente en "
                f"el lugar llamado '{location}'. Justo antes de empezar a hablar, {agent.name} tenía la intención de "
                f"'{agent_action}', y {companion.name} estaba haciendo '{companion_previous_action}'."
            )
            
            dialogue_json = llm_client.generate_social_dialogue(
                agent, companion, 
                agent.long_term_memory, 
                companion.long_term_memory, 
                contexto_phygital 
            )

            # EVOLUCIÓN DE LA RELACIÓN (AFINIDAD CONTINUA)
            # Extraemos el valor del LLM. Si falla o es Mock, usamos +2 por defecto.
            impacto_charla = dialogue_json.get('variacion_relacion', 2) 
            
            puntuacion_homofilia_base = score * 100 # Convertimos el 0.XX a escala 0-100
            
            for (a, b) in [(agent, companion), (companion, agent)]:
                # 1. Si no se conocían, inicializamos su relación basada en la Homofilia
                if str(b.id) not in a.affinity_network:
                    a.affinity_network[str(b.id)] = puntuacion_homofilia_base
                
                # 2. Aplicamos el impacto de la charla evaluado por la IA
                a.affinity_network[str(b.id)] += impacto_charla
                
                # Limitamos los valores matemáticamente entre 0 y 100
                a.affinity_network[str(b.id)] = max(0, min(100, a.affinity_network[str(b.id)]))
                
                # 3. EVALUACIÓN DE UMBRALES (Granovetter)
                afinidad_actual = a.affinity_network[str(b.id)]
                
                if afinidad_actual >= 60: # Umbral para hacerse amigos
                    if str(b.id) not in a.amigos:
                        a.amigos.append(str(b.id))
                        if config.PRINT_LOGS and a == agent:
                            print(f"   [!] ¡{agent.name} y {companion.name} se han hecho amigos (Lazo Fuerte)!")
                            
                elif afinidad_actual < 40: # Umbral para perder la amistad
                    if str(b.id) in a.amigos:
                        a.amigos.remove(str(b.id))
                        if config.PRINT_LOGS and a == agent:
                            print(f"   [!] {agent.name} y {companion.name} se han distanciado y ya no son amigos.")

            # IMPRESIÓN DEL LOG 
            if config.PRINT_LOGS:
                print(f"\n TEMA: {dialogue_json.get('tema_de_conversacion', 'General')}")
                
                signo = "+" if impacto_charla >= 0 else ""
                print(f" IMPACTO RELACIÓN: {signo}{impacto_charla} puntos (Afinidad actual: {int(agent.affinity_network[str(companion.id)])}/100)")
                
                for line in dialogue_json.get('dialogo', []):
                    print(f"    {line}")
                    time.sleep(config.SLEEP_DIALOGUE)  
                print("   " + "-" * 60 + "\n")
                
            return True 
                
        else:
            if config.PRINT_LOGS:
                print(f"   [ {agent.name} vio a sus conocidos en {location}, pero nadie estaba libre o de humor para hablar.]")
            return False 
    else:
        if config.PRINT_LOGS:
            print(f"   [ {agent.name} miró alrededor en {location}, pero no había nadie con quien charlar.]")
        return False