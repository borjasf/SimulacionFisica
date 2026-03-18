import random
import matplotlib.pyplot as plt

# Diccionario que representa los lugares públicos del mapa 100x100
MAPA_CIUDAD = {
    "Oficina_Centro": {
        "coords": (50, 50), "tipo": "TRABAJAR_ESTUDIAR", 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 20.0, "25-54": 90.0, "55-64": 60.0, "65+": 0.0}
    },
    "Universidad_Norte": {
        "coords": (50, 90), "tipo": "TRABAJAR_ESTUDIAR", 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 95.0, "25-54": 30.0, "55-64": 10.0, "65+": 0.0}
    },
    "Instituto_Sur": { # NUEVO: Concentrará a los menores de 16
        "coords": (20, 20), "tipo": "TRABAJAR_ESTUDIAR", 
        "atractivo_por_edad": {"16-": 100.0, "16-24": 10.0, "25-54": 15.0, "55-64": 10.0, "65+": 0.0}
    },
    "Plaza_Mayor": {
        "coords": (48, 52), "tipo": "OCIO_SOCIAL_SITIO", 
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-54": 70.0, "55-64": 60.0, "65+": 80.0}
    },
    "Bar_Manolo": {
        "coords": (10, 15), "tipo": "OCIO_SOCIAL_SITIO", 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 40.0, "25-54": 80.0, "55-64": 90.0, "65+": 70.0}
    },
    "Discoteca_Sur": {
        "coords": (80, 10), "tipo": "OCIO_SOCIAL_SITIO", 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 100.0, "25-54": 50.0, "55-64": 5.0, "65+": 0.0}
    },
    "Centro_Jubilados": { # NUEVO: Punto caliente para la tercera edad
        "coords": (70, 70), "tipo": "OCIO_SOCIAL_SITIO", 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 0.0, "25-54": 5.0, "55-64": 50.0, "65+": 100.0}
    },
    "Cafeteria_Tranquila": { # NUEVO: Local intermedio para mezclar adultos
        "coords": (30, 60), "tipo": "OCIO_SOCIAL_SITIO", 
        "atractivo_por_edad": {"16-": 10.0, "16-24": 30.0, "25-54": 60.0, "55-64": 80.0, "65+": 90.0}
    },
    "Polideportivo": {
        "coords": (20, 80), "tipo": "OCIO_INDIVIDUAL", 
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-54": 60.0, "55-64": 30.0, "65+": 10.0}
    },
    "Parque_Central": {
        "coords": (55, 45), "tipo": "OCIO_INDIVIDUAL", 
        "atractivo_por_edad": {"16-": 90.0, "16-24": 40.0, "25-54": 70.0, "55-64": 60.0, "65+": 90.0}
    }
}

def get_places_by_type(target_type):
    """Filtra el mapa y devuelve solo los lugares del tipo solicitado."""
    return {p_id: info for p_id, info in MAPA_CIUDAD.items() if info["tipo"] == target_type}

def assign_homes(agents_list, map_size=100):
    """
    Agrupa a los agentes y les asigna una coordenada (X, Y) compartida.
    Simula viviendas de 1 a 4 personas.
    """
    agentes_sin_casa = agents_list.copy()
    random.shuffle(agentes_sin_casa)
    
    casas_generadas = {}
    id_casa = 1
    
    while agentes_sin_casa:
        tamano_grupo = random.choices([1, 2, 3, 4], weights=[0.40, 0.30, 0.20, 0.10], k=1)[0]
        habitantes = agentes_sin_casa[:tamano_grupo]
        agentes_sin_casa = agentes_sin_casa[tamano_grupo:]
        
        coords_casa = (random.randint(0, map_size), random.randint(0, map_size))
        nombres_habitantes = []
        
        for agente in habitantes:
            agente.home_coords = coords_casa
            agente.current_coords = coords_casa 
            nombres_habitantes.append(agente.name)
            
        casas_generadas[f"Casa_{id_casa}"] = {
            "coords": coords_casa,
            "habitantes": nombres_habitantes
        }
        id_casa += 1
        
    print(f"Se han generado {len(casas_generadas)} viviendas para {len(agents_list)} agentes.")
    return casas_generadas

def plot_city_map(casas_generadas, agente_destacado=None):
    """
    Genera un gráfico 2D del mapa de 100x100 mostrando las casas y los locales.
    Si se proporciona un agente_destacado, traza sus rutas y su casa.
    """
    plt.figure(figsize=(10, 10))
    plt.title("Mapa de la Ciudad Virtual (100x100)", fontsize=16)
    
    # 1. Dibujar todas las Casas
    x_casas = [info['coords'][0] for info in casas_generadas.values()]
    y_casas = [info['coords'][1] for info in casas_generadas.values()]
    plt.scatter(x_casas, y_casas, c='gray', marker='s', s=30, label='Viviendas', alpha=0.6)
    
    # 2. Dibujar los Lugares Públicos (Ajustado a los nuevos estados)
    colores = {"TRABAJAR_ESTUDIAR": "blue", "OCIO_SOCIAL_SITIO": "red", "OCIO_INDIVIDUAL": "green"}
    marcadores = {"TRABAJAR_ESTUDIAR": "s", "OCIO_SOCIAL_SITIO": "*", "OCIO_INDIVIDUAL": "^"}
    
    for place_id, info in MAPA_CIUDAD.items():
        x, y = info["coords"]
        tipo = info["tipo"]
        plt.scatter(x, y, c=colores.get(tipo, "black"), marker=marcadores.get(tipo, "o"), s=200, edgecolors='black', zorder=2)
        plt.annotate(place_id, (x, y), textcoords="offset points", xytext=(0,12), ha='center', fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none"), zorder=3)
        
    # --- SECCIÓN: DESTACAR AGENTE ---
    if agente_destacado:
        hx, hy = agente_destacado.home_coords
        plt.scatter(hx, hy, c='gold', marker='*', s=400, edgecolors='black', zorder=5)
        plt.annotate(f"Casa de {agente_destacado.name}", (hx, hy), textcoords="offset points", xytext=(0,-18), ha='center', fontweight='bold', color='goldenrod', zorder=6)
        
        for lugar, visitas in agente_destacado.visited_places.items():
            if lugar in MAPA_CIUDAD:
                lx, ly = MAPA_CIUDAD[lugar]["coords"]
                plt.plot([hx, lx], [hy, ly], color='gold', linestyle='--', linewidth=2.5, alpha=0.8, zorder=1)
                plt.annotate(f"({visitas} visitas)", (lx, ly), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=9, color='purple', fontweight='bold', zorder=4)

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.tight_layout()
    plt.show()