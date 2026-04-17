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
import data_exporter

from agent import Agent

def run_simulation():
    print("Iniciando la inicialización del ecosistema...")
    
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

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
            
            # 2. HILO COGNITIVO (Con sistema de Memoria de Intenciones)
            if agente.pending_micro_action:
                # Si acaba de llegar de un viaje, ejecuta su intención original al 100%
                nuevo_macro_estado = agente.pending_macro_state
                nueva_micro_accion = agente.pending_micro_action
                
                # Limpiamos la intención para el futuro
                agente.pending_macro_state = None
                agente.pending_micro_action = None
            else:
                # Si no estaba viajando, la ruleta de Markov decide qué hacer
                estados_posibles, probabilidades_rutina = markov_engine.get_markov_probabilities(estado_anterior_macro)

                probabilidades_personalizadas = []
                for i in range(len(estados_posibles)):
                    estado_evaluado = estados_posibles[i]
                    peso_original = probabilidades_rutina[i]
                    multiplicador = agente.markov_modifiers.get(estado_evaluado, 1.0)
                    probabilidades_personalizadas.append(peso_original * multiplicador)
                
                nuevo_macro_estado = biological_engine.get_next_state_with_biology(
                    agente, probabilidades_personalizadas, estados_posibles
                )
                nueva_micro_accion = markov_engine.choose_micro_action(agente, nuevo_macro_estado)

            # 3. DECISIÓN ESPACIAL Y DESPLAZAMIENTO (LA INTERCEPCIÓN)
            mensaje_espacial = ""
            lugar_memoria = "su ubicación actual"
            lugar_actual = str(agente.current_location_name).strip()
            
            acciones_domesticas = [
                "ingesta_en_hogar", "mantenimiento_del_hogar", "conversacion_con_convivientes", 
                "consumo_audiovisual", "ocio_digital_activo"
            ]
            
            # Acciones híbridas (las hacen donde estén: si están en casa se quedan, si están fuera buscan local)
            acciones_hibridas = ["ver_rrss", "ingesta_rrss", "lectura", "gestiones_personales"]

            # Evaluamos si la rutina exige que el agente esté en casa
            es_motivo_casero = (
                nuevo_macro_estado in ["TAREAS_DOMESTICAS", "DESCANSO"] or 
                nueva_micro_accion in acciones_domesticas or
                (nueva_micro_accion in acciones_hibridas and lugar_actual == "Casa")
            )
            
            # A) Bloque Doméstico
            if es_motivo_casero:
                if agente.current_coords != agente.home_coords:
                    # INTERCEPCIÓN: Guardamos lo que iba a hacer y lo mandamos de viaje a casa
                    agente.pending_macro_state = nuevo_macro_estado
                    agente.pending_micro_action = nueva_micro_accion
                    
                    agente.current_coords = agente.home_coords
                    agente.current_location_name = "Casa"
                    
                    nueva_micro_accion = "desplazamiento_urbano"
                    mensaje_espacial = " -> Viajando hacia casa"
                    lugar_memoria = "de camino a casa"
                else:
                    mensaje_espacial = " -> Se queda en casa"
                    agente.current_location_name = "Casa"
                    lugar_memoria = "Casa"
                    
            # B) Bloque Público
            else:
                info_lugar = environment.MAPA_CIUDAD.get(lugar_actual, {})
                tipos_actuales = info_lugar.get("tipo", [])
                if isinstance(tipos_actuales, str): tipos_actuales = [tipos_actuales]
                
                tipo_coincide = nuevo_macro_estado in tipos_actuales
                accion_soportada = nueva_micro_accion in info_lugar.get("micro_acciones", [])
                
                if lugar_actual != "Casa" and tipo_coincide and accion_soportada:
                    mensaje_espacial = f" -> Continúa aquí ({lugar_actual})"
                    lugar_memoria = lugar_actual
                else:
                    lugares_posibles = environment.get_places_by_type_and_action(nuevo_macro_estado, nueva_micro_accion)
                    
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
                        
                        # INTERCEPCIÓN: Guardamos lo que iba a hacer y lo mandamos de viaje al nuevo destino
                        agente.pending_macro_state = nuevo_macro_estado
                        agente.pending_micro_action = nueva_micro_accion
                        
                        agente.current_coords = environment.MAPA_CIUDAD[destino_id]["coords"]
                        agente.current_location_name = destino_id
                        
                        nueva_micro_accion = "desplazamiento_urbano"
                        tipo_visita = " [NUEVO] " if es_nuevo else " [HABITUAL] "
                        mensaje_espacial = f" -> Viajando hacia: {destino_id} ({tipo_visita})"
                        lugar_memoria = f"de camino a {destino_id}"
                        
                    else:
                        mensaje_espacial = f" -> Pasea por la calle"
                        lugar_memoria = "la calle"
                        agente.current_location_name = "Calle"
                        
                        agente.pending_macro_state = nuevo_macro_estado
                        agente.pending_micro_action = nueva_micro_accion
                        nueva_micro_accion = "desplazamiento_urbano"

            if lugar_memoria != "su ubicación actual" and lugar_memoria != "la calle":
                agente.id_lugar_actual = lugar_memoria

            # 4. MOTOR SOCIAL Y DE COLISIONES
            # Sólo interactúan o usan RRSS si NO se están desplazando
            acciones_conversacion = ["conversacion_social", "conversacion_con_companeros", "conversacion_con_convivientes", "interaccion_ingesta"]
            if nueva_micro_accion in acciones_conversacion:
                hablaron = social_engine.process_encounter(agente, agentes)
                
                # Si no había nadie con quien hablar, buscamos un "fallback" lógico
                if not hablaron:
                    if nuevo_macro_estado == "OCIO": nueva_micro_accion = "ver_rrss"
                    elif nuevo_macro_estado == "TAREAS_DOMESTICAS": nueva_micro_accion = "ver_rrss"
                    elif nuevo_macro_estado == "ALIMENTACION": nueva_micro_accion = "ingesta_rrss"
                    elif nuevo_macro_estado == "OBLIGACIONES": nueva_micro_accion = "revisar_rrss"

            resumen_virtual = ""
            if nueva_micro_accion in ["ver_rrss", "revisar_rrss", "ingesta_rrss"]:
                resumen_virtual = markov_engine.simulate_rrss_session()

            # 5. ACTUALIZACIÓN DE MEMORIA Y LOGS
            agente.update_memory(nuevo_macro_estado, nueva_micro_accion, lugar_memoria, turno_global, virtual_summary=resumen_virtual)
            # Avisamos al agente si este turno fue un evento implícito
            es_implicito = (nueva_micro_accion == "desplazamiento_urbano")
            agente.update_state(nuevo_macro_estado, nueva_micro_accion, is_implicit=es_implicito)
            
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
        print("\n" + "="*80)
        print("INFORME ESTADÍSTICO JERÁRQUICO (Fase 1 & 2)")
        print("="*80)
        print(f"Turnos totales simulados: {turno_global - 1}")
        
        v1_macros, v1_micros = {}, {}
        v2_macros, v2_micros = {}, {}
        v1_total, v2_total = 0, 0

        for a in agentes:
            # Acumular Versión 1 (Completa)
            for estado, count in a.macro_frequencies.items():
                v1_macros[estado] = v1_macros.get(estado, 0) + count
                v1_total += count
            for macro, micros_dict in a.micro_frequencies.items():
                if macro not in v1_micros: v1_micros[macro] = {}
                for micro, count in micros_dict.items():
                    v1_micros[macro][micro] = v1_micros[macro].get(micro, 0) + count

            # Acumular Versión 2 (Pura de Markov)
            for estado, count in a.filtered_macro_frequencies.items():
                v2_macros[estado] = v2_macros.get(estado, 0) + count
                v2_total += count
            for macro, micros_dict in a.filtered_micro_frequencies.items():
                if macro not in v2_micros: v2_micros[macro] = {}
                for micro, count in micros_dict.items():
                    v2_micros[macro][micro] = v2_micros[macro].get(micro, 0) + count

        def imprimir_bloque(titulo, macros, micros, total):
            print(f"\n{titulo}")
            print("-" * len(titulo))
            print("--- DISTRIBUCIÓN DE CAPA 1 (Macro-estados) ---")
            sorted_macros = sorted(macros.items(), key=lambda x: x[1], reverse=True)
            for estado, count in sorted_macros:
                porcentaje = (count / total) * 100 if total > 0 else 0
                print(f" - {estado}: {porcentaje:.2f}% ({count} turnos)")

            print("\n--- DISTRIBUCIÓN DE CAPA 2 (Micro-acciones por Estado) ---")
            for macro, dict_micros in micros.items():
                turnos_en_este_macro = macros.get(macro, 0)
                if turnos_en_este_macro > 0:
                    print(f" * Dentro de {macro} ({turnos_en_este_macro} turnos):")
                    sorted_micros = sorted(dict_micros.items(), key=lambda x: x[1], reverse=True)
                    for micro_name, micro_count in sorted_micros:
                        if micro_count > 0:
                            porcentaje_relativo = (micro_count / turnos_en_este_macro) * 100
                            print(f"      > {micro_name.replace('_', ' ')}: {porcentaje_relativo:.2f}%")

        imprimir_bloque("VERSIÓN 1: ESTADÍSTICAS COMPLETAS (Incluye estado inicial y desplazamientos)", v1_macros, v1_micros, v1_total)
        imprimir_bloque("VERSIÓN 2: ESTADÍSTICAS PURAS DE MARKOV (Excluye rutinas implícitas)", v2_macros, v2_micros, v2_total)

        total_amigos = sum(len(a.amigos) for a in agentes)
        media_amigos = total_amigos / len(agentes) if agentes else 0
        
        print("\n" + "="*80)
        print("MÉTRICAS SOCIALES Y ESPACIALES")
        print("="*80)
        print(f" - Media de amigos por agente: {media_amigos:.2f}")

        print("\n--- LUGARES MÁS VISITADOS ---")
        global_places = {}
        for a in agentes:
            for lugar, visitas in a.visited_places.items():
                global_places[lugar] = global_places.get(lugar, 0) + visitas

        sorted_places = sorted(global_places.items(), key=lambda x: x[1], reverse=True)
        for lugar, visitas in sorted_places[:5]: 
            print(f" - {lugar}: {visitas} visitas")
        print("="*80 + "\n")

        data_exporter.export_simulation_data(agentes, turno_global - 1)

        sys.exit(0)

if __name__ == "__main__":
    run_simulation()