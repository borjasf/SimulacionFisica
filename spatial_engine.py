import math
import random

import config

def euclidean_distance(coord1, coord2):
    """Calcula la distancia en línea recta entre dos coordenadas (X, Y)."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2) #Teorema de Pitágoras

def calculate_exploration_probability(S, rho=config.BASE_EXPLORATION_RHO, gamma=config.BASE_GAMMA):
    """Aplica la fórmula EPR: P_new = rho * S^(-gamma)"""
    if S == 0:
        return 1.0  # Si no conoce ningún sitio de ESTE TIPO, explora al 100%
    return rho * (S ** -gamma)

# Se ponen las constantes por defecto en la función, pero podrían ser modificadas por rasgos de personalidad en main.py mediante las fórmulas de trait_rules.py.
def choose_destination(agent_coords, visited_places, places_db, agent_age_group, rho=config.BASE_EXPLORATION_RHO, gamma=config.BASE_GAMMA, beta=config.BASE_SPATIAL_BETA):
    """
    Decide el siguiente lugar al que irá el agente basándose en EPR, Gravedad y Edad (INE).
    """
    # 1. FILTRO DE MEMORIA: Nos quedamos solo con los sitios visitados que encajan
    known_places = {place_id: count for place_id, count in visited_places.items() if place_id in places_db}
    S = len(known_places)
    
    p_explore = calculate_exploration_probability(S, rho, gamma)
    is_exploring = random.random() < p_explore
    candidates = {}

    if not is_exploring and S > 0:
        # FASE RETORNO PREFERENCIAL
        for place_id, visit_count in known_places.items():
            place_info = places_db[place_id]
            dist = euclidean_distance(agent_coords, place_info['coords'])
            dist = max(dist, 0.1) # Evitar división por cero
            
            # W = Visitas / (Distancia ^ Beta)
            weight = (visit_count + 1) / (dist ** beta)
            candidates[place_id] = weight
    else:
        # FASE EXPLORACIÓN (Modelo de Gravedad cruzado con EDAD)
        is_exploring = True 
        
        for place_id, place_info in places_db.items():
            if place_id not in known_places:
                # Extraemos el atractivo específico para la edad de este agente
                atractivo_real = place_info['atractivo_por_edad'].get(agent_age_group, 0.1)
                
                # Si el lugar está prohibido o tiene 0 atractivo para su edad, lo saltamos
                if atractivo_real <= 0:
                    continue
                    
                dist = euclidean_distance(agent_coords, place_info['coords'])
                dist = max(dist, 0.1)
                
                # W = Atractivo_por_edad / (Distancia ^ Beta)
                weight = atractivo_real / (dist ** beta)
                candidates[place_id] = weight
        
        # Fallback de seguridad: Si intentó explorar pero no hay lugares nuevos aptos...
        if not candidates:
            if S > 0:
                # 1. Si conoce lugares, cambiamos su mentalidad a "Retorno" y calculamos pesos
                for place_id, visit_count in known_places.items():
                    place_info = places_db[place_id]
                    dist = max(euclidean_distance(agent_coords, place_info['coords']), 0.1)
                    candidates[place_id] = visit_count / (dist ** beta)
                is_exploring = False
            else:
                # 2. Si NO conoce ningún lugar y tampoco hay lugares aptos en toda la ciudad...
                # (Es un caso extremo, ej. un niño en una ciudad solo de discotecas)
                # Retornamos "Casa" como destino válido (será manejado en main.py con home_coords)
                return "Casa", False
    # 2. Selección del destino mediante Ruleta Proporcional
    places_list = list(candidates.keys())
    weights_list = list(candidates.values())
    
    chosen_place_id = random.choices(places_list, weights=weights_list, k=1)[0]
    
    return chosen_place_id, is_exploring