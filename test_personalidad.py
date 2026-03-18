# ==============================================================================
# ARCHIVO: test_personalidad.py
# DESCRIPCIÓN: Prueba de estrés de 10.000 turnos para validar el impacto de 
# los rasgos de Goldberg sobre la Cadena de Markov base.
# ==============================================================================

from agent import Agent
import biological_engine
from markov_engine import get_markov_probabilities, TRANSITION_MATRIX

def simular_vida(agente, turnos=10000):
    # Generamos la lista de estados dinámicamente desde la matriz
    estados_posibles = list(TRANSITION_MATRIX.keys())
    
    # Diccionario para contar cuántas veces cae en cada estado
    conteo_estados = {estado: 0 for estado in estados_posibles}
    
    for _ in range(turnos):
        estado_anterior = agente.current_state
        
        # 1. Desgaste biológico
        biological_engine.update_biological_needs(agente)
        
        # 2. Obtener probabilidades base
        estados, prob_base = get_markov_probabilities(estado_anterior)
        
        # 3. Aplicar sesgo de personalidad (Goldberg)
        prob_personalizadas = []
        for i in range(len(estados)):
            est = estados[i]
            peso = prob_base[i]
            mult = agente.markov_modifiers.get(est, 1.0)
            prob_personalizadas.append(peso * mult)
            
        # 4. Decisión final integrando biología (Déficit)
        nuevo_estado = biological_engine.get_next_state_with_biology(
            agente, prob_personalizadas, estados
        )
        
        # 5. Actualizar agente y contar
        agente.update_state(nuevo_estado)
        conteo_estados[nuevo_estado] += 1
        
    # Imprimir resultados
    print(f"\n=== RESULTADOS PARA: {agente.name} ({turnos} turnos) ===")
    print(f"Rasgos: {agente.traits}")
    print("-" * 50)
    
    # Ordenamos de mayor a menor porcentaje
    estados_ordenados = sorted(conteo_estados.items(), key=lambda x: x[1], reverse=True)
    
    for estado, cantidad in estados_ordenados:
        porcentaje = (cantidad / turnos) * 100
        print(f"{estado.ljust(25)}: {porcentaje:>5.2f}% ({cantidad} turnos)")

if __name__ == "__main__":
    # Creamos un agente extremadamente RESPONSABLE e INTROVERTIDO
    carlos = Agent(
        agent_id="A1", 
        name="Carlos (El Rutinario)", 
        social_activity=0.2, 
        traits_list=["Conscientiousness +", "Sociability -", "Openness -"], 
        age=40
    )
    
    # Creamos una agente CAÓTICA, EXTROVERTIDA y NEURÓTICA
    ana = Agent(
        agent_id="A2", 
        name="Ana (La Inestable)", 
        social_activity=0.9, 
        traits_list=["Conscientiousness -", "Neuroticism +", "Sociability +", "Openness +"], 
        age=22
    )
    
    print("Iniciando simulación aislada de 10.000 turnos...")
    simular_vida(carlos, 10000)
    simular_vida(ana, 10000)