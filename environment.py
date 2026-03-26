import random
import matplotlib.pyplot as plt

MAPA_CIUDAD = {
    # ZONAS DE TRABAJO Y ESTUDIO 
    "Oficina_Centro": {
        "coords": (50, 50), "tipo": "TRABAJAR_ESTUDIAR", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 20.0, "25-44": 90.0, "45-64": 60.0, "65+": 0.0}
    },
    "Universidad_Norte": {
        "coords": (50, 90), "tipo": "TRABAJAR_ESTUDIAR", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 95.0, "25-44": 30.0, "45-64": 10.0, "65+": 0.0}
    },
    "Instituto_Sur": { 
        "coords": (20, 20), "tipo": "TRABAJAR_ESTUDIAR", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 100.0, "16-24": 10.0, "25-44": 15.0, "45-64": 10.0, "65+": 0.0}
    },
    "Biblioteca_Municipal": { 
        "coords": (60, 60), "tipo": "TRABAJAR_ESTUDIAR", "permite_comer": False, 
        "atractivo_por_edad": {"16-": 40.0, "16-24": 80.0, "25-44": 60.0, "45-64": 30.0, "65+": 20.0}
    },

    # ZONAS DE OCIO (Fusionadas)
    "Plaza_Mayor": {
        "coords": (48, 52), "tipo": "OCIO", "permite_comer": True,
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-44": 70.0, "45-64": 60.0, "65+": 80.0}
    },
    "Bar_Manolo": {
        "coords": (10, 15), "tipo": "OCIO", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 40.0, "25-44": 80.0, "45-64": 90.0, "65+": 70.0}
    },
    "Discoteca_Sur": {
        "coords": (80, 10), "tipo": "OCIO", "permite_comer": False, 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 100.0, "25-44": 50.0, "45-64": 5.0, "65+": 0.0}
    },
    "Centro_Jubilados": { 
        "coords": (70, 70), "tipo": "OCIO", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 0.0, "25-44": 5.0, "45-64": 50.0, "65+": 100.0}
    },
    "Cafeteria_Tranquila": { 
        "coords": (30, 60), "tipo": "OCIO", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 10.0, "16-24": 30.0, "25-44": 60.0, "45-64": 80.0, "65+": 90.0}
    },
    "Restaurante_Familiar": { 
        "coords": (40, 40), "tipo": "OCIO", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 50.0, "16-24": 40.0, "25-44": 85.0, "45-64": 85.0, "65+": 70.0}
    },
    "Polideportivo": {
        "coords": (20, 80), "tipo": "OCIO", "permite_comer": False,
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-44": 60.0, "45-64": 30.0, "65+": 10.0}
    },
    "Parque_Central": {
        "coords": (55, 45), "tipo": "OCIO", "permite_comer": True, 
        "atractivo_por_edad": {"16-": 90.0, "16-24": 40.0, "25-44": 70.0, "45-64": 60.0, "65+": 90.0}
    },
    "Gimnasio_Centro": { 
        "coords": (70, 30), "tipo": "OCIO", "permite_comer": False, 
        "atractivo_por_edad": {"16-": 10.0, "16-24": 85.0, "25-44": 80.0, "45-64": 40.0, "65+": 5.0}
    }
}

def get_places_by_type(target_type):
    """Filtra el mapa y devuelve solo los lugares que coinciden con el estado físico solicitado."""
    return {p_id: info for p_id, info in MAPA_CIUDAD.items() if info["tipo"] == target_type}

def assign_homes(agents_list, map_size=100):
    """
    Agrupa a los agentes aleatoriamente y les asigna una coordenada (X, Y) compartida.
    Simula unidades de convivencia familiar o pisos compartidos de 1 a 4 personas.
    """
    agentes_sin_casa = agents_list.copy()
    random.shuffle(agentes_sin_casa)
    
    casas_generadas = {}
    id_casa = 1
    
    while agentes_sin_casa:
        # Probabilidades de tamaño de hogar: 40% solos, 30% parejas, 20% tres, 10% cuatro
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
    Genera un gráfico 2D del mapa de 100x100 mostrando las viviendas y los locales públicos.
    Si se proporciona un agente_destacado, traza sus rutas preferidas y su casa en dorado.
    """
    plt.figure(figsize=(10, 10))
    plt.title("Mapa de la Ciudad Phygital (100x100)", fontsize=16)
    
    # 1. Dibujar todas las Viviendas (Grises)
    x_casas = [info['coords'][0] for info in casas_generadas.values()]
    y_casas = [info['coords'][1] for info in casas_generadas.values()]
    plt.scatter(x_casas, y_casas, c='gray', marker='s', s=30, label='Viviendas', alpha=0.6)
    
    # 2. Dibujar los Lugares Públicos (Adaptado a la nomenclatura Phygital)
    colores = {"TRABAJAR_ESTUDIAR": "blue", "OCIO_PUBLICO": "red", "OCIO_INDIVIDUAL": "green"}
    marcadores = {"TRABAJAR_ESTUDIAR": "s", "OCIO_PUBLICO": "*", "OCIO_INDIVIDUAL": "^"}
    
    for place_id, info in MAPA_CIUDAD.items():
        x, y = info["coords"]
        tipo = info["tipo"]
        
        # Pinta el punto del lugar
        plt.scatter(x, y, c=colores.get(tipo, "black"), marker=marcadores.get(tipo, "o"), 
                    s=200, edgecolors='black', zorder=2)
                    
        # Añade la etiqueta de texto flotante
        plt.annotate(place_id, (x, y), textcoords="offset points", xytext=(0,12), 
                     ha='center', fontsize=9, fontweight='bold', 
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="none"), zorder=3)
        
    # 3. DESTACAR LA VIDA DE UN AGENTE (Si se solicita)
    if agente_destacado:
        hx, hy = agente_destacado.home_coords
        # Pinta su casa de oro
        plt.scatter(hx, hy, c='gold', marker='*', s=400, edgecolors='black', zorder=5)
        plt.annotate(f"Casa de {agente_destacado.name}", (hx, hy), textcoords="offset points", 
                     xytext=(0,-18), ha='center', fontweight='bold', color='goldenrod', zorder=6)
        
        # Traza las líneas hacia los lugares que ha visitado a lo largo de la simulación
        for lugar, visitas in agente_destacado.visited_places.items():
            if lugar in MAPA_CIUDAD:
                lx, ly = MAPA_CIUDAD[lugar]["coords"]
                plt.plot([hx, lx], [hy, ly], color='gold', linestyle='--', linewidth=2.5, alpha=0.8, zorder=1)
                plt.annotate(f"({visitas} visitas)", (lx, ly), textcoords="offset points", 
                             xytext=(0,-15), ha='center', fontsize=9, color='purple', fontweight='bold', zorder=4)

    # Configuraciones visuales del grid
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("Eje X (Coordenadas)")
    plt.ylabel("Eje Y (Coordenadas)")
    plt.tight_layout()
    plt.show()