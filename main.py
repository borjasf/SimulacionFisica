import time
import sys
import random
import math
import traceback

import llm_client
from agent_ingestor import load_agents_from_csv, load_friendships_from_csv
import markov_engine
import environment
import spatial_engine
import biological_engine
import config
import social_engine

from agent import Agent

def run_simulation():
    print("Iniciando la inicialización del ecosistema...")
    
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

    # TUS AGENTES CLONES PARA LA PRUEBA DE VACÍO
    agentes = []
    for i in range(50):
        agentes.append(
            Agent(
                agent_id=i, name=f"Clon_{i}", social_activity=50, 
                traits_list=[], age=30, gender="male", occupation="Oficinista", 
                qualification="Grado", interests="Nada"
            )
        )

    print("Cargando la red social de amistades...")
    load_friendships_from_csv(agentes, "friendships.csv")

    print("Generando el entorno urbano...")
    casas_ciudad = environment.assign_homes(agentes)

    pesos_actividad = [(math.sqrt(agente.social_activity) + 1) for agente in agentes]

    print("\n--- ¡Comienza el simulador espacial Phygital! (Ctrl+C para detener) ---\n")
    
    turno_global = 1
    
    try:
        while True:
            agente = random.choices(agentes, weights=pesos_actividad, k=1)[0]
            
            estado_anterior_macro = agente.current_macro_state
            
            # 1. HILO FÍSICO: CAPA 1 (MACRO-ESTADO) Y BIOLOGÍA
            biological_engine.update_biological_needs(agente)
            
            estados_posibles, probabilidades_rutina = markov_engine.get_markov_probabilities(estado_anterior_macro)

            probabilidades_personalizadas = []
            for i in range(len(estados_posibles)):
                estado_evaluado = estados_posibles[i]
                peso_original = probabilidades_rutina[i]
                multiplicador = agente.markov_modifiers.get(estado_evaluado, 1.0)
                probabilidades_personalizadas.append(peso_original * multiplicador)
            
            nuevo_macro_estado = biological_engine.get_next_state_with_biology(
                agente, 
                probabilidades_personalizadas, 
                estados_posibles
            )
            
            # 2. HILO COGNITIVO: CAPA 2 (MICRO-ACCIÓN)
            nueva_micro_accion = markov_engine.choose_micro_action(agente, nuevo_macro_estado)

            resumen_virtual = ""
            if nueva_micro_accion in ["usar_rrss", "ver_las_rrss"]:
                resumen_virtual = markov_engine.simulate_rrss_session()
            
            # 3. MOTOR SOCIAL Y DE COLISIONES
            if nueva_micro_accion in ["conversar", "charlar_mientras_comes"]:
                hablaron = social_engine.process_encounter(agente, agentes)
                
                # Si no había nadie con quien hablar, buscamos un "fallback" lógico
                if not hablaron:
                    if nuevo_macro_estado == "OCIO": nueva_micro_accion = "dar_una_vuelta"
                    elif nuevo_macro_estado == "CASA": nueva_micro_accion = "ver_la_television"
                    elif nuevo_macro_estado == "COMER_BEBER": nueva_micro_accion = "comer_fuera"

            # 4. DECISIÓN ESPACIAL (G-EPR)
            mensaje_espacial = ""
            lugar_memoria = "su ubicación actual"
            
            # A) Búsqueda activa de destino público
            if nuevo_macro_estado in ["OCIO", "TRABAJAR_ESTUDIAR"]:
                lugares_posibles = environment.get_places_by_type(nuevo_macro_estado)
                
                if lugares_posibles:
                    rho_personalizado = max(0.0, min(1.0, config.BASE_EXPLORATION_RHO + agente.exploration_rho_bonus))
                    beta_personalizado = max(0.1, config.BASE_SPATIAL_BETA * agente.spatial_beta_modifier)

                    destino_id, es_nuevo = spatial_engine.choose_destination(
                        agent_coords=agente.current_coords,
                        visited_places=agente.visited_places,
                        places_db=lugares_posibles,
                        agent_age_group=agente.age_group, 
                        rho=rho_personalizado, 
                        beta=beta_personalizado 
                    )
                    
                    agente.visited_places[destino_id] = agente.visited_places.get(destino_id, 0) + 1
                    agente.current_coords = environment.MAPA_CIUDAD[destino_id]["coords"]
                    agente.current_location_name = destino_id
                    
                    tipo_visita = " [NUEVO] " if es_nuevo else " [HABITUAL] "
                    mensaje_espacial = f" -> Se desplaza a: {destino_id} ({tipo_visita})"
                    lugar_memoria = destino_id 
                    
            # B) Lógica combinada para COMER_BEBER según la micro-acción
            elif nuevo_macro_estado == "COMER_BEBER":
                if nueva_micro_accion == "comer_en_casa":
                    agente.current_coords = agente.home_coords
                    agente.current_location_name = "Casa"
                    mensaje_espacial = " -> Vuelve a casa para comer"
                    lugar_memoria = "Casa"
                else:
                    lugar_actual = str(agente.current_location_name).strip()
                    info_lugar = environment.MAPA_CIUDAD.get(lugar_actual, {})
                    permite_comer = info_lugar.get("permite_comer", True)
                    
                    if lugar_actual != "Casa" and permite_comer:
                        mensaje_espacial = f" -> Aprovecha para comer aquí ({lugar_actual})"
                        lugar_memoria = lugar_actual
                    else:
                        # Si está en casa o en un sitio donde no dejan comer (ej. Gimnasio), sale a un local de OCIO
                        lugares_comida = {k: v for k, v in environment.get_places_by_type("OCIO").items() if v.get("permite_comer", True)}
                        if lugares_comida:
                            destino_id, _ = spatial_engine.choose_destination(
                                agent_coords=agente.current_coords, visited_places=agente.visited_places,
                                places_db=lugares_comida, agent_age_group=agente.age_group, rho=0.5, beta=1.0)
                            
                            agente.visited_places[destino_id] = agente.visited_places.get(destino_id, 0) + 1
                            agente.current_coords = environment.MAPA_CIUDAD[destino_id]["coords"]
                            agente.current_location_name = destino_id
                            mensaje_espacial = f" -> Sale a comer a: {destino_id}"
                            lugar_memoria = destino_id
                        
            # C) Lógica de repliegue al hogar
            elif nuevo_macro_estado in ["DORMIR", "CASA"]:
                if agente.current_coords != agente.home_coords:
                    agente.current_coords = agente.home_coords
                    mensaje_espacial = " -> Vuelve a casa"
                else:
                    mensaje_espacial = " -> Se queda en casa"
                
                agente.current_location_name = "Casa"
                lugar_memoria = "Casa"
            
            if lugar_memoria != "su ubicación actual":
                agente.id_lugar_actual = lugar_memoria
        
            # 5. ACTUALIZACIÓN DE MEMORIA Y LOGS
            agente.update_memory(nuevo_macro_estado, nueva_micro_accion, lugar_memoria, turno_global, virtual_summary=resumen_virtual)
            agente.update_state(nuevo_macro_estado, nueva_micro_accion)
            
            if config.PRINT_LOGS:
                if resumen_virtual:
                    print(f"[Turno {turno_global}] [VIRTUAL] {agente.name} -> En {lugar_memoria}: {resumen_virtual}")
                else:
                    print(f"[Turno {turno_global}] [FÍSICO]  {agente.name} -> {nuevo_macro_estado} ({nueva_micro_accion.replace('_', ' ')})){mensaje_espacial}")

            if config.MAX_TURNS > 0 and turno_global >= config.MAX_TURNS:
                break 

            turno_global += 1
            if config.PRINT_LOGS:
                time.sleep(config.SLEEP_TICK)
            
    except KeyboardInterrupt:
        print("\n\n [!] Simulación detenida manualmente (Ctrl+C).")
        
    except Exception as e:
        print(f"\n\n [ERROR CRÍTICO] La simulación se ha estrellado en el turno {turno_global}!")
        print(f" Motivo del error: {e}\n")
        traceback.print_exc()
        
    finally:
        # INFORME ESTADÍSTICO DE CAPA 1 Y CAPA 2
        print("\n" + "="*60)
        print("INFORME ESTADÍSTICO JERÁRQUICO (Fase 1 & 2)")
        print("="*60)
        print(f"Turnos totales simulados: {turno_global - 1}")
        
        global_macros = {}
        global_micros = {}
        total_turns = 0

        for a in agentes:
            for estado, count in a.macro_frequencies.items():
                global_macros[estado] = global_macros.get(estado, 0) + count
                total_turns += count
                
            for macro, micros_dict in a.micro_frequencies.items():
                if macro not in global_micros:
                    global_micros[macro] = {}
                for micro, count in micros_dict.items():
                    global_micros[macro][micro] = global_micros[macro].get(micro, 0) + count

        print("\n--- DISTRIBUCIÓN DE CAPA 1 (Macro-estados) ---")
        sorted_macros = sorted(global_macros.items(), key=lambda x: x[1], reverse=True)
        for estado, count in sorted_macros:
            porcentaje = (count / total_turns) * 100 if total_turns > 0 else 0
            print(f" - {estado}: {porcentaje:.2f}% ({count} turnos totales)")

        print("\n--- DISTRIBUCIÓN DE CAPA 2 (Micro-acciones por Estado) ---")
        for macro, dict_micros in markov_engine.MICRO_ACTIONS.items():
            turnos_en_este_macro = global_macros.get(macro, 0)
            if turnos_en_este_macro > 0:
                print(f" * Dentro de {macro} ({turnos_en_este_macro} turnos):")
                
                # Extraemos solo las micro-acciones pertenecientes a este macro-estado
                micros_de_este_macro = global_micros.get(macro, {})
                sorted_micros = sorted(micros_de_este_macro.items(), key=lambda x: x[1], reverse=True)
                
                for micro_name, micro_count in sorted_micros:
                    if micro_count > 0:
                        porcentaje_relativo = (micro_count / turnos_en_este_macro) * 100
                        print(f"      > {micro_name.replace('_', ' ')}: {porcentaje_relativo:.2f}%")

        total_amigos = sum(len(a.amigos) for a in agentes)
        media_amigos = total_amigos / len(agentes) if agentes else 0
        print("\n--- MÉTRICAS SOCIALES ---")
        print(f" - Media de amigos por agente: {media_amigos:.2f}")

        print("\n--- LUGARES MÁS VISITADOS ---")
        global_places = {}
        for a in agentes:
            for lugar, visitas in a.visited_places.items():
                global_places[lugar] = global_places.get(lugar, 0) + visitas

        sorted_places = sorted(global_places.items(), key=lambda x: x[1], reverse=True)
        for lugar, visitas in sorted_places[:5]: 
            print(f" - {lugar}: {visitas} visitas")
        print("="*60 + "\n")

        sys.exit(0)

if __name__ == "__main__":
    run_simulation()