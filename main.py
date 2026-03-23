import time
import sys
import random
import math

# MOTOR LOCAL DE EMBEDDINGS
from sentence_transformers import SentenceTransformer, util
import llm_client
# Importamos nuestros módulos
from agent_ingestor import load_agents_from_csv, load_friendships_from_csv
from markov_engine import get_markov_probabilities, evaluate_virtual_action
import environment
import spatial_engine
import biological_engine
import config
import social_engine

def run_simulation():
    print("Iniciando la inicialización del ecosistema...")
    
    # NUEVO: CARGA DEL MODELO SEMÁNTICO (sentence-transformers) (SOLO UNA VEZ)
    print("Cargando el motor cognitivo local (Embeddings)...")
    # Este proceso dura unos segundos, pero luego será instantáneo
    motor_semantico = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("Motor cognitivo cargado con éxito.")

    # 1. Cargamos los agentes del CSV
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

    # NUEVA LÓGICA DE AMISTAD
    print("Cargando la red social de amistades...")
    load_friendships_from_csv(agentes, "friendships.csv")

    # 2. Asignamos las casas (Coordenadas de origen compartidas)
    print("Generando el entorno urbano...")
    casas_ciudad = environment.assign_homes(agentes)

    # Calculamos las papeletas para la lotería de turnos (Raíz cuadrada + Suavizado de Laplace)
    pesos_actividad = [(math.sqrt(agente.social_activity) + 1) for agente in agentes]

    print("\n--- ¡Comienza el simulador espacial de eventos discretos! (Ctrl+C para detener) ---\n")
    
    turno_global = 1
    
    try:
        while True:
            # 3. Elegimos al agente usando la cola de prioridad ponderada
            agente = random.choices(agentes, weights=pesos_actividad, k=1)[0]
            
            estado_anterior = agente.current_state
            
            # INTEGRACIÓN: MARKOV + BIOLOGICAL 
            
            # A) El agente sufre el desgaste de su último turno
            biological_engine.update_biological_needs(agente)
            
            # B) Pedimos la rutina base al motor de Markov (SIN tirar los dados)
            estados_posibles, probabilidades_rutina = get_markov_probabilities(estado_anterior)

            # APLICAMOS LA PERSONALIDAD A LA RUTINA 
            probabilidades_personalizadas = []
            for i in range(len(estados_posibles)):
                estado_evaluado = estados_posibles[i]
                peso_original = probabilidades_rutina[i]
                # Leemos si el agente tiene un multiplicador para este estado (por defecto 1.0)
                multiplicador = agente.markov_modifiers.get(estado_evaluado, 1.0)
                probabilidades_personalizadas.append(peso_original * multiplicador)
            
            # C) El motor biológico suma la urgencia fisiológica y tira los dados
            nuevo_estado = biological_engine.get_next_state_with_biology(
                agente, 
                probabilidades_personalizadas, # <-- Usamos las probabilidades alteradas por personalidad
                estados_posibles
            )
            
            #UNICAMENTE SEPARA LA ACCION DE RRSS EN USAR, SEGUIR, SALIR PARA AYUDAR A LA PARTE VIRTUAL.
            accion_virtual = evaluate_virtual_action(estado_anterior, nuevo_estado)
            
            # 4. DECISIÓN ESPACIAL (G-EPR: Gravedad + Retorno Preferencial + Edades)
            mensaje_espacial = ""
            lugar_memoria = "su ubicación actual" # <-- 1. Variable por defecto para la memoria
            
            # Si el agente va a un destino público (NUEVOS ESTADOS)
            if nuevo_estado in ["OCIO_SOCIAL_SITIO", "OCIO_INDIVIDUAL"]:
                
                # Filtramos el mapa para darle solo las opciones viables
                lugares_posibles = environment.get_places_by_type(nuevo_estado)
                
                if lugares_posibles:
                # Aplicamos los límites matemáticos por seguridad (rho entre 0 y 1, beta positivo)
                    rho_personalizado = max(0.0, min(1.0, config.BASE_EXPLORATION_RHO + agente.exploration_rho_bonus))
                    beta_personalizado = max(0.1, config.BASE_SPATIAL_BETA * agente.spatial_beta_modifier)

                    # El motor espacial aplica la teoría de la Gravedad, el modelo EPR y el corte demográfico
                    destino_id, es_nuevo = spatial_engine.choose_destination(
                        agent_coords=agente.current_coords,
                        visited_places=agente.visited_places,
                        places_db=lugares_posibles,
                        agent_age_group=agente.age_group, 
                        rho=rho_personalizado, 
                        beta=beta_personalizado 
                    )
                    
                    # Actualizamos la memoria espacial del agente
                    agente.visited_places[destino_id] = agente.visited_places.get(destino_id, 0) + 1
                    agente.current_coords = environment.MAPA_CIUDAD[destino_id]["coords"]
                    agente.current_location_name = destino_id
                    
                    # Formateamos el texto para la consola
                    tipo_visita = " [NUEVO] " if es_nuevo else " [HABITUAL] "
                    mensaje_espacial = f" -> Se desplaza a: {destino_id} ({tipo_visita})"
                    lugar_memoria = destino_id # <-- 2. Guardamos el nombre del lugar público
                    
            # Si la Cadena de Markov decide que descansa en casa (NUEVOS ESTADOS)
            elif nuevo_estado in ["DORMIR", "INACTIVO_RELAX", "INACTIVO_TAREAS_CASA"]:
                if agente.current_coords != agente.home_coords:
                    agente.current_coords = agente.home_coords
                    mensaje_espacial = " -> Vuelve a casa"
                else:
                    mensaje_espacial = " -> Se queda en casa"
                
                agente.current_location_name = "Casa"
                lugar_memoria = "Casa" # <-- 3. Guardamos que está en casa
            
            # Nota: Si el estado es "OCIO_SOCIAL_CONVERSAR" u otros genéricos, 
            # el lugar_memoria se quedará como "su ubicación actual"
            if lugar_memoria != "su ubicación actual":
                agente.id_lugar_actual = lugar_memoria
            
            # Llama a la memoria para acumular, pero ya no procesa el resultado
            agente.update_memory(nuevo_estado, lugar_memoria, turno_global)
            
            # 5. Actualizamos el estado cognitivo
            agente.update_state(nuevo_estado)
            
            # 6. Imprimimos el evento completo por consola (SOLO SI PRINT_LOGS ES TRUE)
            if config.PRINT_LOGS:
                if accion_virtual != "ACCION_FISICA":
                    print(f"[Turno {turno_global}] [VIRTUAL] {agente.name} ({agente.age_group}) -> {accion_virtual} | {nuevo_estado}{mensaje_espacial}")
                else:
                    print(f"[Turno {turno_global}] [FÍSICO]  {agente.name} ({agente.age_group}) -> {nuevo_estado}{mensaje_espacial}")

            # EL ENCUENTRO Y EL DIÁLOGO SOCIAL
            if nuevo_estado == "OCIO_SOCIAL_CONVERSAR":
                social_engine.process_encounter(agente, agentes, motor_semantico, turno_global)

            #PARADA AUTOMÁTICA
            if config.MAX_TURNS > 0 and turno_global > config.MAX_TURNS:
                break # Rompe el bucle a la velocidad de la luz cuando llegue al tope

            turno_global += 1
            
            #Solo pausa si estamos viendo los logs
            if config.PRINT_LOGS:
                time.sleep(config.SLEEP_TICK)
            

    except KeyboardInterrupt:
        print("\n\n [!] Simulación detenida manualmente (Ctrl+C).")
        
    except Exception as e:
        print(f"\n\n [ERROR CRÍTICO] La simulación se ha estrellado en el turno {turno_global}!")
        print(f" Motivo del error: {e}\n")
        import traceback
        traceback.print_exc() #línea exacta del fallo
        
    finally:
        # =================================================================
        # GENERACIÓN DEL INFORME ESTADÍSTICO PARA EL TRIBUNAL
        # =================================================================
        print("\n" + "="*60)
        print("INFORME ESTADÍSTICO DE LA SIMULACIÓN")
        print("="*60)
        print(f"Turnos totales simulados: {turno_global - 1}")
        
        # Métrica 1: BIOLOGÍA Y MARKOV
        global_states = {}
        total_states_logged = 0
        for a in agentes:
            for estado, count in a.state_frequencies.items():
                global_states[estado] = global_states.get(estado, 0) + count
                total_states_logged += count

        print("\n--- DISTRIBUCIÓN DEL TIEMPO (ESTADOS DE MARKOV) ---")
        sorted_states = sorted(global_states.items(), key=lambda x: x[1], reverse=True)
        for estado, count in sorted_states:
            porcentaje = (count / total_states_logged) * 100 if total_states_logged > 0 else 0
            print(f" - {estado}: {porcentaje:.2f}% ({count} turnos totales)")

        # Métrica 2: RED SOCIAL
        total_amigos = sum(len(a.amigos) for a in agentes)
        media_amigos = total_amigos / len(agentes) if agentes else 0
        print("\n--- MÉTRICAS SOCIALES Y HOMOFILIA ---")
        print(f" - Media de amigos por agente: {media_amigos:.2f}")
        
        if agentes:
            extrovertido = max(agentes, key=lambda a: len(a.amigos))
            introvertido = min(agentes, key=lambda a: len(a.amigos))
            print(f" - El más sociable: {extrovertido.name} ({len(extrovertido.amigos)} amigos)")
            print(f" - El menos sociable: {introvertido.name} ({len(introvertido.amigos)} amigos)")

        # Métrica 3: ESPACIAL
        print("\n--- LUGARES MÁS VISITADOS (MODELO ESPACIAL) ---")
        global_places = {}
        for a in agentes:
            for lugar, visitas in a.visited_places.items():
                global_places[lugar] = global_places.get(lugar, 0) + visitas

        sorted_places = sorted(global_places.items(), key=lambda x: x[1], reverse=True)
        for lugar, visitas in sorted_places[:5]: 
            print(f" - {lugar}: {visitas} visitas totales")
        print("="*60 + "\n")

        if agentes:
            top_agente = agentes[0]
            print(f"\nGenerando mapa 2D para {top_agente.name}... (Cierra la ventana gráfica para salir)")
            try:
                environment.plot_city_map(casas_ciudad, agente_destacado=top_agente)
            except Exception:
                pass

        print("\n¡Simulación finalizada!")
        sys.exit(0)

if __name__ == "__main__":
    run_simulation()