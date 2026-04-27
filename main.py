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

# Configurar reproducibilidad si está activada
if config.RANDOM_SEED is not None:
    random.seed(config.RANDOM_SEED)

def run_simulation():
    """
    Ejecuta la simulación multi-agente.
    Integra todos los motores: biológico, Markov, espacial y social.
    """
    print("Iniciando la inicialización del ecosistema...")
    
    # Cargar agentes desde CSV
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

    # Cargar red de amistades pre-existentes
    print("Cargando la red social de amistades...")
    load_friendships_from_csv(agentes, "friendships.csv")

    # Asignar hogares aleatorios a cada agente
    print("Generando el entorno urbano...")
    environment.assign_homes(agentes)

    # Pesos de selección: agentes más sociables se seleccionan más frecuentemente
    pesos_actividad = [(math.sqrt(agente.social_activity) + 1) for agente in agentes]

    print("\n--- Simulador iniciado (Ctrl+C para detener) ---\n")
    
    turno_global = 1
    
    try:
        while True:
            # Seleccionar agente proporcionalmente a su sociabilidad
            agente = random.choices(agentes, weights=pesos_actividad, k=1)[0]
            
            estado_anterior_macro = agente.current_macro_state
            
            # Motor biológico: actualizar necesidades fisiológicas
            biological_engine.update_biological_needs(agente)
            
            # Motor de decisión: determinar macro-estado y micro-acción
            # Si el agente estaba viajando, ejecutar su intención original
            if agente.pending_micro_action:
                nuevo_macro_estado = agente.pending_macro_state
                nueva_micro_accion = agente.pending_micro_action
                agente.pending_macro_state = None
                agente.pending_micro_action = None
            else:
                # Aplicar transición de Markov modulada por necesidades biológicas
                estados_posibles, probabilidades_rutina = markov_engine.get_markov_probabilities(estado_anterior_macro)

                # Personalizar probabilidades según rasgos del agente
                probabilidades_personalizadas = []
                for i in range(len(estados_posibles)):
                    estado_evaluado = estados_posibles[i]
                    peso_original = probabilidades_rutina[i]
                    multiplicador = agente.markov_modifiers.get(estado_evaluado, 1.0)
                    probabilidades_personalizadas.append(peso_original * multiplicador)
                
                # Decisión de macro-estado considerando urgencias biológicas
                nuevo_macro_estado = biological_engine.get_next_state_with_biology(
                    agente, probabilidades_personalizadas, estados_posibles
                )

                # Elegir micro-acción según motor configurado (Markov o LLM)
                if config.DECISION_ENGINE == "MARKOV":
                    nueva_micro_accion = markov_engine.choose_micro_action(agente, nuevo_macro_estado)
                
                elif config.DECISION_ENGINE == "LLM":
                    opciones_validas = list(markov_engine.MICRO_ACCIONES[nuevo_macro_estado].keys())
                    nueva_micro_accion = llm_client.decide_micro_action(agente, nuevo_macro_estado, opciones_validas)
                    # Fallback: si LLM devuelve acción inválida, usar Markov
                    if nueva_micro_accion not in opciones_validas:
                        nueva_micro_accion = markov_engine.choose_micro_action(agente, nuevo_macro_estado)
                
                else:
                    print(f"[Aviso] Motor de decisión inválido. Usando MARKOV.")
                    nueva_micro_accion = markov_engine.choose_micro_action(agente, nuevo_macro_estado)

            # Motor espacial: decidir destino con exploración/retorno preferencial
            mensaje_espacial = ""
            lugar_memoria = "su ubicación actual"
            lugar_actual = str(agente.current_location_name).strip()
            
            # Acciones que requieren desplazamiento
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
                        
                        # INTERCEPCIÓN: Guardamos lo que iba a hacer y lo mandamos de viaje al nuevo destino
                        agente.pending_macro_state = nuevo_macro_estado
                        agente.pending_micro_action = nueva_micro_accion
                        
                        if destino_id == "Casa":
                            # Si el motor espacial devuelve "Casa", usa home_coords del agente
                            agente.current_coords = agente.home_coords
                            agente.current_location_name = "Casa"
                            nueva_micro_accion = "desplazamiento_urbano"
                            mensaje_espacial = " -> Viajando hacia casa"
                            lugar_memoria = "de camino a casa"
                        elif destino_id is None:
                            # Si spatial_engine no puede encontrar destino válido, el agente pasea por la calle
                            mensaje_espacial = f" -> Pasea por la calle"
                            lugar_memoria = "la calle"
                            agente.current_location_name = "Calle"
                            nueva_micro_accion = "desplazamiento_urbano"
                        else:
                            # Destino válido en MAPA_CIUDAD
                            agente.visited_places[destino_id] = agente.visited_places.get(destino_id, 0) + 1
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
                    elif nuevo_macro_estado == "TAREAS_DOMESTICAS": nueva_micro_accion = "mantenimiento_del_hogar"
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
        # RECOLECCIÓN DE ESTADÍSTICAS PURAS (Sin desplazamientos ni DORMIR inicial)
        print("\n")
        print("="*80)
        print("INFORME FINAL DE SIMULACIÓN")
        print("="*80)
        print(f"Turnos totales: {turno_global - 1} | Agentes: {len(agentes)}")
        
        macros, micros = {}, {}
        total = 0
        desplazamientos = 0

        for a in agentes:
            # Acumular estadísticas puras de Markov
            for estado, count in a.filtered_macro_frequencies.items():
                macros[estado] = macros.get(estado, 0) + count
                total += count
            for macro, micros_dict in a.filtered_micro_frequencies.items():
                if macro not in micros: micros[macro] = {}
                for micro, count in micros_dict.items():
                    micros[macro][micro] = micros[macro].get(micro, 0) + count
                    if micro == "desplazamiento_urbano":
                        desplazamientos += count

        # SECCIÓN 1: DISTRIBUCIÓN DE MACRO-ESTADOS
        print("\nMACRO-ESTADOS (Distribución de Actividades)")
        sorted_macros = sorted(macros.items(), key=lambda x: x[1], reverse=True)
        for estado, count in sorted_macros:
            porcentaje = (count / total) * 100 if total > 0 else 0
            barra = "█" * int(porcentaje / 2)
            print(f"  {estado:20s} {porcentaje:6.1f}%  {barra} {count} turnos")

        # SECCIÓN 2: MICRO-ACCIONES POR MACRO-ESTADO
        print("\nMICRO-ACCIONES (Detalles por Actividad)")
        for macro in sorted(micros.keys()):
            dict_micros = micros[macro]
            turnos_en_macro = macros.get(macro, 0)
            if turnos_en_macro > 0:
                print(f"\n  {macro}:")
                sorted_micros = sorted(dict_micros.items(), key=lambda x: x[1], reverse=True)
                for micro_name, micro_count in sorted_micros:
                    if micro_count > 0:
                        porcentaje = (micro_count / turnos_en_macro) * 100
                        print(f"    {micro_name:30s} {porcentaje:6.1f}%")

        # SECCIÓN 3: MOVILIDAD ESPACIAL
        print("\nMOVILIDAD ESPACIAL")
        pct_desplazamiento = (desplazamientos / total) * 100 if total > 0 else 0
        pct_sedentario = 100 - pct_desplazamiento
        print(f"  Desplazamientos:        {pct_desplazamiento:6.1f}%")
        print(f"  Permanencia en lugar:   {pct_sedentario:6.1f}%")

        # SECCIÓN 4: MÉTRICAS SOCIALES
        total_amigos = sum(len(a.amigos) for a in agentes)
        media_amigos = total_amigos / len(agentes) if agentes else 0
        
        print("\nMÉTRICAS SOCIALES")
        print(f"  Amigos promedio/agente: {media_amigos:6.2f}")
        print(f"  Total conexiones:       {total_amigos}")

        # SECCIÓN 5: LUGARES MÁS VISITADOS
        global_places = {}
        for a in agentes:
            for lugar, visitas in a.visited_places.items():
                global_places[lugar] = global_places.get(lugar, 0) + visitas

        print("\nLUGARES MÁS VISITADOS")
        sorted_places = sorted(global_places.items(), key=lambda x: x[1], reverse=True)
        for i, (lugar, visitas) in enumerate(sorted_places[:8], 1):
            print(f"  {i}. {lugar:25s} {visitas:6d} visitas")

        data_exporter.export_simulation_data(agentes, turno_global - 1)

        sys.exit(0)

if __name__ == "__main__":
    run_simulation()