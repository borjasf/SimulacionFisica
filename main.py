import time
import sys
import random
import math

# MOTOR LOCAL DE EMBEDDINGS
from sentence_transformers import SentenceTransformer, util
import llm_client
# Importamos nuestros módulos
from agent_ingestor import load_agents_from_csv
from markov_engine import get_markov_probabilities, evaluate_virtual_action
import environment
import spatial_engine
import biological_engine
import config
import social_engine

def run_simulation():
    print("Iniciando la inicialización del ecosistema...")
    
    # NUEVO: CARGA DEL MODELO SEMÁNTICO (SOLO UNA VEZ)
    print("Cargando el motor cognitivo local (Embeddings)...")
    # Este proceso dura unos segundos, pero luego será instantáneo
    motor_semantico = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("Motor cognitivo cargado con éxito.")

    # 1. Cargamos los agentes del CSV
    agentes = load_agents_from_csv("users.csv")
    if not agentes:
        print("No hay agentes. Saliendo...")
        sys.exit()

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
            
            # --- INTEGRACIÓN: MARKOV + BIOLOGICAL ---
            
            # A) El agente sufre el desgaste de su último turno
            biological_engine.update_biological_needs(agente)
            
            # B) Pedimos la rutina base al motor de Markov (SIN tirar los dados)
            estados_posibles, probabilidades_rutina = get_markov_probabilities(estado_anterior)

            # --- NUEVO: APLICAMOS LA PERSONALIDAD A LA RUTINA ---
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
                    tipo_visita = "🌟 NUEVO" if es_nuevo else "🔄 HABITUAL"
                    mensaje_espacial = f" -> Se desplaza a: {destino_id} ({tipo_visita})"
                    lugar_memoria = destino_id # <-- 2. Guardamos el nombre del lugar público
                    
            # Si la Cadena de Markov decide que descansa en casa (NUEVOS ESTADOS)
            elif nuevo_estado in ["DORMIR", "INACTIVO_RELAX", "INACTIVO_TAREAS_CASA"]:
                if agente.current_coords != agente.home_coords:
                    agente.current_coords = agente.home_coords
                    mensaje_espacial = " -> 🏠 Vuelve a casa"
                else:
                    mensaje_espacial = " -> 🏠 Permanece en casa"
                
                agente.current_location_name = "Casa"
                lugar_memoria = "Casa" # <-- 3. Guardamos que está en casa
            
            # Nota: Si el estado es "OCIO_SOCIAL_CONVERSAR" u otros genéricos, 
            # el lugar_memoria se quedará como "su ubicación actual"
            # ---> AÑADE ESTAS DOS LÍNEAS AQUÍ <---
            if lugar_memoria != "su ubicación actual":
                agente.id_lugar_actual = lugar_memoria
            
            # update_memory nos devuelve True si el búfer llegó a 10
            # Le pasamos el turno_global y el motor_semantico local
            toca_reflexionar = agente.update_memory(nuevo_estado, lugar_memoria, turno_global, motor_semantico)
            
            if toca_reflexionar:
                print(f"\n🧠 [REFLEXIÓN] {agente.name} está reflexionando sobre sus últimas experiencias...")
                
                # 1. Gemini resume las 10 acciones crudas
                reflexion = llm_client.generate_daily_reflection(agente, agente.action_buffer)
                
                # 2. El modelo local vectoriza la reflexión
                texto_a_vectorizar = reflexion["resumen_narrativo"]
                vector = motor_semantico.encode(texto_a_vectorizar)
                
                # 3. Guardamos el recuerdo a largo plazo pasándole el turno
                agente.save_reflection(reflexion, vector, turno_global)
                
                print(f"   💡 Pensamiento: '{reflexion['resumen_narrativo']}'")
                print(f"   📊 Importancia: {reflexion['importancia']}/10 | Tema: {reflexion['tema_central']}\n")
            
            
            # 5. Actualizamos el estado cognitivo
            agente.update_state(nuevo_estado)
            
            # 6. Imprimimos el evento completo por consola (La memoria del agente NO se imprime)
            if accion_virtual != "ACCION_FISICA":
                print(f"[Turno {turno_global}] 📱 [VIRTUAL] {agente.name} ({agente.age_group}) -> {accion_virtual} | {nuevo_estado}{mensaje_espacial}")
            else:
                print(f"[Turno {turno_global}] 🚶 [FÍSICO]  {agente.name} ({agente.age_group}) -> {nuevo_estado}{mensaje_espacial}")

            # --- EL ENCUENTRO Y EL DIÁLOGO SOCIAL ---
            if nuevo_estado == "OCIO_SOCIAL_CONVERSAR":
                social_engine.process_encounter(agente, agentes, motor_semantico, turno_global)

            turno_global += 1
            time.sleep(config.SLEEP_TICK) # Pausa del bucle normal
            
    except KeyboardInterrupt:
        print("\n\n Simulación detenida manualmente.")
        print("\n=== EJEMPLO DE MEMORIA ESPACIAL A LARGO PLAZO ===")
        # Mostramos los lugares que ha visitado el agente más activo
        top_agente = agentes[0]
        print(f"Lugares descubiertos por {top_agente.name}:")
        for lugar, visitas in top_agente.visited_places.items():
            print(f" - {lugar}: {visitas} visitas")
        
        print("\nGenerando mapa... (Cierra la ventana gráfica para salir del todo)")
        try:
            environment.plot_city_map(casas_ciudad, agente_destacado=top_agente)
        except KeyboardInterrupt:
            pass
        finally:
            print("\n¡Simulación finalizada correctamente!")
            sys.exit(0)

if __name__ == "__main__":
    run_simulation()