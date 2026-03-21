import csv
import time

# Importamos tus módulos existentes
from agent_ingestor import load_agents_from_csv
import llm_client

def generar_pasados(csv_entrada="users.csv", csv_salida="users_con_biografias.csv"):
    print(f"Abriendo '{csv_entrada}' para cargar la población...")
    
    # Usamos tu ingestor para cargar los perfiles
    agentes = load_agents_from_csv(csv_entrada)
    if not agentes:
        print("No se encontraron agentes. Abortando.")
        return

    print(f"Preparando la escritura de biografías para {len(agentes)} habitantes.")
    print("Este proceso puede tardar un rato para respetar los límites de la API de Google.\n")

    filas_actualizadas = []
    
    # Usamos 'utf-8-sig' por seguridad con los formatos de Excel
    with open(csv_entrada, mode='r', encoding='utf-8-sig') as archivo_in:
        lector = csv.DictReader(archivo_in)
        cabeceras = lector.fieldnames
        
        for fila in lector:
            # Rescatamos el nombre del agente en lugar del ID
            nombre_agente = fila['name']
            
            # Encontramos el objeto agente exacto buscando por su nombre
            agente_obj = next((a for a in agentes if a.name == nombre_agente), None)
            
            if agente_obj:
                print(f"Redactando la vida de {agente_obj.name}...")
                
                # Llamamos a Gemini
                biografia = llm_client.generate_agent_backstory(agente_obj)
                
                # Guardamos el resultado en la fila del Excel
                fila['backstory'] = biografia
            else:
                fila['backstory'] = "Biografía no generada."
                
            filas_actualizadas.append(fila)
            
            # Pausa obligatoria de 3 segundos para evitar colapsar la cuota gratuita de Gemini
            time.sleep(10) 

    # Añadimos la nueva cabecera si es la primera vez que lo corremos
    if 'backstory' not in cabeceras:
        cabeceras.append('backstory')
        
    # Escribimos el nuevo archivo con todo el historial incluido
    with open(csv_salida, mode='w', encoding='utf-8', newline='') as archivo_out:
        escritor = csv.DictWriter(archivo_out, fieldnames=cabeceras)
        escritor.writeheader()
        escritor.writerows(filas_actualizadas)
        
    print(f"\n¡Éxito total! Las biografías han sido forjadas y guardadas en '{csv_salida}'.")

if __name__ == "__main__":
    generar_pasados()