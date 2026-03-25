import time
import sys
import random
import math
import traceback

import llm_client
# Importamos nuestros módulos
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
    
    # 1. Cargamos los agentes del CSV
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

    # (OPCIONAL) TU AGENTE DE CONTROL PARA PRUEBAS
    # Comenta este bloque si quieres usar los agentes reales del CSV
    """ agentes = [
        Agent(
            agent_id=999, name="Sujeto_Control", social_activity=50, 
            traits_list=[], age=30, gender="male", occupation="Oficinista", 
            qualification="Grado", interests="Nada"
        )
    ]"""

    # LISTA DE AGENTES ESTRATÉGICOS PARA EL TEST DE TURÍNG PHYGITAL
    agentes = [
        Agent(
            agent_id=1, name="James", social_activity=80, 
            traits_list=["Sociability +", "Neuroticism +", "Openness +"], 
            age=20, gender="male", occupation="Estudiante de Ingeniería", 
            qualification="Grado", interests="Física, Videojuegos, Café"
        ),
        Agent(
            agent_id=2, name="Benjamin", social_activity=40, 
            traits_list=["Sociability -", "Conscientiousness +", "Amiability +"], 
            age=45, gender="male", occupation="Arquitecto", 
            qualification="Máster", interests="Diseño, Lectura, Silencio"
        ),
        Agent(
            agent_id=3, name="Clara", social_activity=70, 
            traits_list=["Sociability +", "Openness +", "Amiability -"], 
            age=28, gender="female", occupation="Artista Freelance", 
            qualification="Grado", interests="Pintura, Museos, Redes Sociales"
        ),
        Agent(
            agent_id=4, name="Ricardo", social_activity=30, 
            traits_list=["Sociability -", "Conscientiousness +", "Neuroticism -"], 
            age=68, gender="male", occupation="Jubilado", 
            qualification="Doctorado", interests="Ajedrez, Pasear"
        ),
        Agent(
            agent_id=5, name="Elena", social_activity=90, 
            traits_list=["Sociability +", "Amiability +", "Conscientiousness -"], 
            age=24, gender="female", occupation="Camarera", 
            qualification="Bachillerato", interests="Música, Conciertos, Viajar"
        ),
        Agent(
            agent_id=6, name="Lucas", social_activity=55, 
            traits_list=["Neuroticism +", "Conscientiousness -", "Openness -"], 
            age=32, gender="male", occupation="Administrativo", 
            qualification="FP", interests="Series, Descansar, Fútbol"
        )
    ]

    # NUEVA LÓGICA DE AMISTAD
    print("Cargando la red social de amistades...")
    load_friendships_from_csv(agentes, "friendships.csv")

    # 2. Asignamos las casas (Coordenadas de origen compartidas)
    print("Generando el entorno urbano...")
    casas_ciudad = environment.assign_homes(agentes)

    # Calculamos las papeletas para la lotería de turnos (Raíz cuadrada + Suavizado de Laplace)
    pesos_actividad = [(math.sqrt(agente.social_activity) + 1) for agente in agentes]

    print("\n--- ¡Comienza el simulador espacial Phygital! (Ctrl+C para detener) ---\n")
    
    turno_global = 1
    
    try:
        while True:
            # 3. Elegimos al agente usando la cola de prioridad ponderada
            agente = random.choices(agentes, weights=pesos_actividad, k=1)[0]
            
            estado_anterior_primario = agente.primary_state
            
            
            # INTEGRACIÓN MARKOV + BIOLOGÍA (ESTADO PRIMARIO)
            
            # A) El agente sufre el desgaste de su último turno físico
            biological_engine.update_biological_needs(agente)
            
            # B) Pedimos la rutina base al motor de Markov físico
            estados_posibles, probabilidades_rutina = markov_engine.get_markov_probabilities(estado_anterior_primario)

            # C) Aplicamos la personalidad a la rutina
            probabilidades_personalizadas = []
            for i in range(len(estados_posibles)):
                estado_evaluado = estados_posibles[i]
                peso_original = probabilidades_rutina[i]
                multiplicador = agente.markov_modifiers.get(estado_evaluado, 1.0)
                probabilidades_personalizadas.append(peso_original * multiplicador)
            
            # D) El motor biológico suma la urgencia fisiológica y tira los dados
            nuevo_estado_primario = biological_engine.get_next_state_with_biology(
                agente, 
                probabilidades_personalizadas, 
                estados_posibles
            )
            
        
            # DECISIÓN ESPACIAL (G-EPR)
        
            mensaje_espacial = ""
            lugar_memoria = "su ubicación actual"
            
            # Si el agente va a un destino público (NUEVOS ESTADOS FÍSICOS)
            if nuevo_estado_primario in ["OCIO_PUBLICO", "OCIO_INDIVIDUAL", "TRABAJAR_ESTUDIAR"]:
                
                lugares_posibles = environment.get_places_by_type(nuevo_estado_primario)
                
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
                    
            # ¡NUEVA LÓGICA! Si el motor biológico exige COMER o BEBER
            elif nuevo_estado_primario == "COMER_BEBER":
                lugar_actual = str(agente.current_location_name).strip()
                
                # 1. Si ya está en casa, come allí directamente
                if lugar_actual == "Casa":
                    mensaje_espacial = " -> Come en casa"
                    lugar_memoria = "Casa"
                
                # 2. Si está en la calle, leemos el diccionario para ver si le dejan comer
                else:
                    # Usamos .get() por seguridad (si el lugar no existe, asumimos True por defecto)
                    info_lugar = environment.MAPA_CIUDAD.get(lugar_actual, {})
                    permite_comer = info_lugar.get("permite_comer", True)
                    
                    if permite_comer:
                        mensaje_espacial = f" -> Aprovecha para comer aquí ({lugar_actual})"
                        lugar_memoria = lugar_actual
                    else:
                        # Le echan o no puede comer (ej. Gimnasio). Se va a casa.
                        agente.current_coords = agente.home_coords
                        agente.current_location_name = "Casa"
                        mensaje_espacial = f" -> Vuelve a casa para comer (en {lugar_actual} no se puede)"
                        lugar_memoria = "Casa"
                        
            # Si la Cadena de Markov decide que descansa en casa
            elif nuevo_estado_primario in ["DORMIR", "INACTIVO_RELAX", "INACTIVO_TAREAS_CASA"]:
                if agente.current_coords != agente.home_coords:
                    agente.current_coords = agente.home_coords
                    mensaje_espacial = " -> Vuelve a casa"
                else:
                    mensaje_espacial = " -> Se queda en casa"
                
                agente.current_location_name = "Casa"
                lugar_memoria = "Casa"
            
            if lugar_memoria != "su ubicación actual":
                agente.id_lugar_actual = lugar_memoria
            
            # ESTADO SECUNDARIO / MULTITAREA
            
            # <-- AQUÍ ESTÁ EL CAMBIO CLAVE -->
            nuevo_estado_secundario = markov_engine.evaluate_secondary_state(agente, nuevo_estado_primario)
            
            # Si el motor secundario dictamina que quiere charlar
            if nuevo_estado_secundario == "CONVERSAR":
                # social_engine procesa todo y devuelve True si hubo diálogo real
                hablaron = social_engine.process_encounter(agente, agentes)
                
                # Si no había nadie con quien hablar, revierte su estado mental
                if not hablaron:
                    nuevo_estado_secundario = "NINGUNO"

            # Evaluamos si hace uso virtual (RRSS)
            accion_virtual = markov_engine.evaluate_virtual_action(agente.secondary_state, nuevo_estado_secundario)
            
        
            # ACTUALIZACIÓN DE MEMORIA Y LOGS
        
            
            agente.update_memory(nuevo_estado_primario, nuevo_estado_secundario, lugar_memoria, turno_global)
            agente.update_state(nuevo_estado_primario, nuevo_estado_secundario)
            
            if config.PRINT_LOGS:
                # Añadimos el estado secundario a la consola visualmente si está haciendo algo
                texto_sec = f" [+ {nuevo_estado_secundario}]" if nuevo_estado_secundario != "NINGUNO" else ""
                
                if accion_virtual != "ACCION_FISICA":
                    print(f"[Turno {turno_global}] [VIRTUAL] {agente.name} ({agente.age_group}) -> {accion_virtual} | {nuevo_estado_primario}{mensaje_espacial}{texto_sec}")
                else:
                    print(f"[Turno {turno_global}] [FÍSICO]  {agente.name} ({agente.age_group}) -> {nuevo_estado_primario}{mensaje_espacial}{texto_sec}")

            # PARADA AUTOMÁTICA
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
        # =================================================================
        # GENERACIÓN DEL INFORME ESTADÍSTICO
        # =================================================================
        print("\n" + "="*60)
        print("INFORME ESTADÍSTICO DE LA SIMULACIÓN")
        print("="*60)
        print(f"Turnos totales simulados: {turno_global - 1}")
        
        global_states = {}
        total_states_logged = 0
        for a in agentes:
            # Aquí leemos state_frequencies, que ahora guarda las tareas primarias
            for estado, count in a.state_frequencies.items():
                global_states[estado] = global_states.get(estado, 0) + count
                total_states_logged += count

        print("\n--- DISTRIBUCIÓN DEL TIEMPO (ESTADO FÍSICO) ---")
        sorted_states = sorted(global_states.items(), key=lambda x: x[1], reverse=True)
        for estado, count in sorted_states:
            porcentaje = (count / total_states_logged) * 100 if total_states_logged > 0 else 0
            print(f" - {estado}: {porcentaje:.2f}% ({count} turnos totales)")

        total_amigos = sum(len(a.amigos) for a in agentes)
        media_amigos = total_amigos / len(agentes) if agentes else 0
        print("\n--- MÉTRICAS SOCIALES Y HOMOFILIA ---")
        print(f" - Media de amigos por agente: {media_amigos:.2f}")
        
        if agentes:
            extrovertido = max(agentes, key=lambda a: len(a.amigos))
            introvertido = min(agentes, key=lambda a: len(a.amigos))
            print(f" - El más sociable: {extrovertido.name} ({len(extrovertido.amigos)} amigos)")
            print(f" - El menos sociable: {introvertido.name} ({len(introvertido.amigos)} amigos)")

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