import csv
import os
from datetime import datetime

def export_simulation_data(agentes, turnos_totales, base_folder="resultados_tfg"):
    """
    Agrega estadísticas de todos los agentes y exporta a archivo CSV con timestamp.
    Incluye macro-estados, micro-acciones y lugares visitados.
    """
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Crear nombre de archivo con timestamp día_mes_hora_minuto
    timestamp = datetime.now().strftime("%d_%m_%H_%M")
    filename = f"resultados_{timestamp}.csv"
    filepath = os.path.join(base_folder, filename)
        
    print(f"\nExportando reporte a: '{filepath}'...")

    # Agregadores de estadísticas
    v1_macros, v1_micros = {}, {}
    v2_macros, v2_micros = {}, {}
    global_places = {}

    # Acumular estadísticas de todos los agentes
    for a in agentes:
        # Versión 1: Estadísticas completas
        for estado, count in a.macro_frequencies.items():
            v1_macros[estado] = v1_macros.get(estado, 0) + count
        for macro, micros_dict in a.micro_frequencies.items():
            if macro not in v1_micros: 
                v1_micros[macro] = {}
            for micro, count in micros_dict.items():
                v1_micros[macro][micro] = v1_micros[macro].get(micro, 0) + count

        # Versión 2: Solo transiciones Markov pura
        for estado, count in a.filtered_macro_frequencies.items():
            v2_macros[estado] = v2_macros.get(estado, 0) + count
        for macro, micros_dict in a.filtered_micro_frequencies.items():
            if macro not in v2_micros: 
                v2_micros[macro] = {}
            for micro, count in micros_dict.items():
                v2_micros[macro][micro] = v2_micros[macro].get(micro, 0) + count
                
        # Lugares visitados
        for lugar, visitas in a.visited_places.items():
            global_places[lugar] = global_places.get(lugar, 0) + visitas

    # Escribir CSV con delimitador punto y coma
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        # Usamos punto y coma (;) para que Excel lo separe en columnas automáticamente
        writer = csv.writer(f, delimiter=';')

        # --- BLOQUE 1: METADATOS DE LA EJECUCIÓN ---
        writer.writerow(["=== REPORTE DE SIMULACION TFG ==="])
        writer.writerow(["Identificador", timestamp])
        writer.writerow(["Turnos Totales Simulados", turnos_totales])
        writer.writerow([]) # Fila vacía para separar
        writer.writerow([]) 

        # --- BLOQUE 2: CAPA 1 (Macro-estados) ---
        writer.writerow(["=== CAPA 1: MACRO-ESTADOS ==="])
        writer.writerow(["Version", "Macro_Estado", "Turnos_Absolutos", "Porcentaje"])
        
        v1_total = sum(v1_macros.values())
        for estado, count in sorted(v1_macros.items(), key=lambda x: x[1], reverse=True):
            porcentaje = round((count / v1_total) * 100, 2) if v1_total > 0 else 0
            writer.writerow(["V1_Completa", estado, count, f"{porcentaje}%"])
            
        v2_total = sum(v2_macros.values())
        for estado, count in sorted(v2_macros.items(), key=lambda x: x[1], reverse=True):
            porcentaje = round((count / v2_total) * 100, 2) if v2_total > 0 else 0
            writer.writerow(["V2_Pura", estado, count, f"{porcentaje}%"])
            
        writer.writerow([])
        writer.writerow([])

        # --- BLOQUE 3: CAPA 2 (Micro-acciones) ---
        writer.writerow(["=== CAPA 2: MICRO-ACCIONES ==="])
        writer.writerow(["Version", "Macro_Estado", "Micro_Accion", "Turnos_Absolutos", "Porcentaje_Relativo"])
        
        for macro, micros_dict in v1_micros.items():
            total_en_macro = v1_macros.get(macro, 0)
            for micro, count in sorted(micros_dict.items(), key=lambda x: x[1], reverse=True):
                porcentaje = round((count / total_en_macro) * 100, 2) if total_en_macro > 0 else 0
                writer.writerow(["V1_Completa", macro, micro, count, f"{porcentaje}%"])
                
        for macro, micros_dict in v2_micros.items():
            total_en_macro = v2_macros.get(macro, 0)
            for micro, count in sorted(micros_dict.items(), key=lambda x: x[1], reverse=True):
                porcentaje = round((count / total_en_macro) * 100, 2) if total_en_macro > 0 else 0
                writer.writerow(["V2_Pura", macro, micro, count, f"{porcentaje}%"])

        writer.writerow([])
        writer.writerow([])

        # --- BLOQUE 4: MOTOR ESPACIAL ---
        writer.writerow(["=== MOTOR ESPACIAL: LUGARES VISITADOS ==="])
        writer.writerow(["Lugar", "Visitas_Totales"])
        
        for lugar, visitas in sorted(global_places.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([lugar, visitas])

    print(f"[EXPORTACIÓN] ¡Completada! Archivo maestro generado en la carpeta {base_folder}.")