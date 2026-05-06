import random
import matplotlib.pyplot as plt


# Mapa urbano con 12 ubicaciones diferenciadas por tipo, atractivo por edad y acciones permitidas
MAPA_CIUDAD = {
    # Zonas de trabajo y estudio
    "Oficina_Centro": {
        "coords": (50, 50), "tipo": "OBLIGACIONES",
        "micro_acciones": ["jornada_laboral", "gestiones_personales", "conversacion_con_companeros", "revisar_rrss"], 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 20.0, "25-44": 90.0, "45-64": 60.0, "65+": 0.0}
    },
    "Universidad_Norte": {
        "coords": (50, 90), "tipo": "OBLIGACIONES",
        "micro_acciones": ["jornada_academica", "gestiones_personales", "conversacion_con_companeros", "revisar_rrss"], 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 95.0, "25-44": 30.0, "45-64": 10.0, "65+": 0.0}
    },
    "Instituto_Sur": { 
        "coords": (20, 20), "tipo": "OBLIGACIONES",
        "micro_acciones": ["jornada_academica", "gestiones_personales", "conversacion_con_companeros", "revisar_rrss"], 
        "atractivo_por_edad": {"16-": 100.0, "16-24": 10.0, "25-44": 15.0, "45-64": 10.0, "65+": 0.0}
    },
    "Biblioteca_Municipal": { 
        "coords": (60, 60), "tipo": ["OBLIGACIONES", "OCIO"],
        "micro_acciones": ["gestiones_personales", "revisar_rrss", "actividad_cultural", "lectura", "ver_rrss"], 
        "atractivo_por_edad": {"16-": 40.0, "16-24": 80.0, "25-44": 60.0, "45-64": 30.0, "65+": 20.0}
    },

    # Zonas públicas y de ocio
    "Plaza_Mayor": {
        "coords": (48, 52), "tipo": ["OCIO", "ALIMENTACION"],
        "micro_acciones": ["paseo_recreativo", "conversacion_social", "ver_rrss", "ingesta_ligera", "lectura"],
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-44": 70.0, "45-64": 60.0, "65+": 80.0}
    },
    "Bar_Manolo": {
        "coords": (10, 15), "tipo": ["OCIO", "ALIMENTACION"],
        "micro_acciones": ["ocio_hosteleria", "conversacion_social", "ingesta_en_restauracion", "interaccion_ingesta", "ver_rrss", "ingesta_rrss"], 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 40.0, "25-44": 80.0, "45-64": 90.0, "65+": 70.0}
    },
    "Discoteca_Sur": {
        "coords": (80, 10), "tipo": "OCIO",
        "micro_acciones": ["ocio_hosteleria", "conversacion_social", "ver_rrss"], 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 100.0, "25-44": 50.0, "45-64": 5.0, "65+": 0.0}
    },
    "Centro_Jubilados": { 
        "coords": (70, 70), "tipo": ["OCIO", "ALIMENTACION"],
        "micro_acciones": ["conversacion_social", "ocio_hosteleria", "lectura", "ver_rrss", "actividad_cultural"], 
        "atractivo_por_edad": {"16-": 0.0, "16-24": 0.0, "25-44": 5.0, "45-64": 50.0, "65+": 100.0}
    },
    "Cafeteria_Tranquila": { 
        "coords": (30, 60), "tipo": ["OCIO", "ALIMENTACION"],
        "micro_acciones": ["ocio_hosteleria", "ingesta_en_restauracion", "ingesta_ligera", "interaccion_ingesta", "lectura", "conversacion_social", "ver_rrss", "ingesta_rrss"], 
        "atractivo_por_edad": {"16-": 10.0, "16-24": 30.0, "25-44": 60.0, "45-64": 80.0, "65+": 90.0}
    },
    "Restaurante_Familiar": { 
        "coords": (40, 40), "tipo": "ALIMENTACION",
        "micro_acciones": ["ingesta_en_restauracion", "interaccion_ingesta", "ingesta_ligera", "ingesta_rrss"], 
        "atractivo_por_edad": {"16-": 50.0, "16-24": 40.0, "25-44": 85.0, "45-64": 85.0, "65+": 70.0}
    },
    "Polideportivo": {
        "coords": (20, 80), "tipo": "OCIO",
        "micro_acciones": ["actividad_fisica", "conversacion_social", "ver_rrss"],
        "atractivo_por_edad": {"16-": 80.0, "16-24": 90.0, "25-44": 60.0, "45-64": 30.0, "65+": 10.0}
    },
    "Parque_Central": {
        "coords": (55, 45), "tipo": ["OCIO", "ALIMENTACION"],
        "micro_acciones": ["paseo_recreativo", "actividad_fisica", "conversacion_social", "lectura", "ver_rrss", "ingesta_ligera"], 
        "atractivo_por_edad": {"16-": 90.0, "16-24": 40.0, "25-44": 70.0, "45-64": 60.0, "65+": 90.0}
    },
    "Gimnasio_Centro": { 
        "coords": (70, 30), "tipo": "OCIO",
        "micro_acciones": ["actividad_fisica", "ver_rrss"], 
        "atractivo_por_edad": {"16-": 10.0, "16-24": 85.0, "25-44": 80.0, "45-64": 40.0, "65+": 5.0}
    }
}

def get_places_by_type_and_action(macro_estado, micro_accion):
    """Filtra el mapa aceptando lugares híbridos con una lógica universal."""
    lugares_validos = {}
    for nombre_lugar, info in MAPA_CIUDAD.items():
        tipos_lugar = info.get("tipo", [])

        if isinstance(tipos_lugar, str):
            tipos_lugar = [tipos_lugar]

        # Lógica pura: si el estado está en la lista de tipos y la acción en su lista
        if macro_estado in tipos_lugar and micro_accion in info.get("micro_acciones", []):
            lugares_validos[nombre_lugar] = info

    return lugares_validos

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
        # Probabilidades de tamaño de hogar: 28% solos, 29% parejas, 20% tres, 23% cuatro (https://www.ine.es/dyngs/Prensa/PROH20242039.htm)
        tamano_grupo = random.choices([1, 2, 3, 4], weights=[0.28, 0.29, 0.20, 0.23], k=1)[0]
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
    
    # 2. Dibujar los Lugares Públicos
    colores = {"OBLIGACIONES": "blue", "OCIO": "red", "ALIMENTACION": "orange"}
    marcadores = {"OBLIGACIONES": "s", "OCIO": "*", "ALIMENTACION": "^"}
    
    for place_id, info in MAPA_CIUDAD.items():
        x, y = info["coords"]
        tipos = info["tipo"]
        
        # Si es un lugar con múltiples tipos, cogemos el principal para el color
        tipo_principal = tipos[0] if isinstance(tipos, list) else tipos
        
        # Pinta el punto del lugar
        plt.scatter(x, y, c=colores.get(tipo_principal, "black"), marker=marcadores.get(tipo_principal, "o"), 
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