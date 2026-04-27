import math
import random

import config

def euclidean_distance(coord1, coord2):
    """Calcula la distancia euclidiana entre dos puntos en el plano."""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def calculate_exploration_probability(S, rho=config.BASE_EXPLORATION_RHO, gamma=config.BASE_GAMMA):
    """
    Calcula probabilidad de exploración usando modelo G-EPR.
    P = rho * S^(-gamma), donde S es cantidad de lugares conocidos.
    """
    if S == 0:
        return 1.0  # Si no hay lugares conocidos, explora con certeza
    return rho * (S ** -gamma)

def choose_destination(agent_coords, visited_places, places_db, agent_age_group, rho=config.BASE_EXPLORATION_RHO, gamma=config.BASE_GAMMA, beta=config.BASE_SPATIAL_BETA):
    """
    Elige destino del agente combinando exploración/retorno preferencial.
    Aplica atractivo edad-específico para lugares nuevos.
    Retorna (lugar_id, es_exploración).
    """
    # Filtrar lugares conocidos que existen en la base de datos
    known_places = {place_id: count for place_id, count in visited_places.items() if place_id in places_db}
    S = len(known_places)
    
    # Decidir entre exploración o retorno preferencial
    p_explore = calculate_exploration_probability(S, rho, gamma)
    is_exploring = random.random() < p_explore
    candidates = {}

    if not is_exploring and S > 0:
        # Retorno preferencial: vuelve a lugares conocidos ponderados por visitas y distancia
        for place_id, visit_count in known_places.items():
            place_info = places_db[place_id]
            dist = euclidean_distance(agent_coords, place_info['coords'])
            dist = max(dist, 0.1)  # Evitar división por cero
            
            # Peso = Visitas / (Distancia ^ Beta)
            weight = (visit_count + 1) / (dist ** beta)
            candidates[place_id] = weight
    else:
        # Exploración: busca lugares nuevos atractivos según su edad
        is_exploring = True 
        
        for place_id, place_info in places_db.items():
            if place_id not in known_places:
                # Obtener atractivo específico para edad del agente
                atractivo_real = place_info['atractivo_por_edad'].get(agent_age_group, 0.1)
                
                # Saltar lugares prohibidos o sin atractivo para su edad
                if atractivo_real <= 0:
                    continue
                    
                dist = euclidean_distance(agent_coords, place_info['coords'])
                dist = max(dist, 0.1)
                
                # Peso = Atractivo / (Distancia ^ Beta)
                weight = atractivo_real / (dist ** beta)
                candidates[place_id] = weight
        
        # Fallback: si no hay lugares nuevos aptos, retorna a lugares conocidos
        if not candidates:
            if S > 0:
                for place_id, visit_count in known_places.items():
                    place_info = places_db[place_id]
                    dist = max(euclidean_distance(agent_coords, place_info['coords']), 0.1)
                    candidates[place_id] = visit_count / (dist ** beta)
                is_exploring = False
            else:
                # Sin lugares conocidos ni nuevos: volver a casa
                return "Casa", False
    
    places_list = list(candidates.keys())
    weights_list = list(candidates.values())
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