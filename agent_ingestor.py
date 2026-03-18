import csv
import ast
from agent import Agent

def load_agents_from_csv(filepath):
    """
    Lee el archivo users.csv, crea las instancias de Agent y las devuelve 
    ordenadas por su nivel de social_activity (de mayor a menor).
    """
    agents_list = []
    
    try:
        # Abrimos el CSV
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                agent_id = row.get('id', row.get('user_account_id', 'unknown')) 
                name = row.get('name', 'SinNombre')
                
                # EXTRACCIÓN DE EDAD
                try:
                    age = int(row.get('age', 30)) # 30 por defecto
                except ValueError:
                    age = 30
                
                # EXTRACCIÓN DE SOCIAL ACTIVITY
                try:
                    social_activity = float(row.get('social_activity', 0.0)) # 0.0 por defecto
                except ValueError:
                    social_activity = 0.0

                # EXTRACCIÓN DE RASGOS (lista en string)
                traits_raw = row.get('traits', "[]")
                try:
                    traits_list = ast.literal_eval(traits_raw)
                except (ValueError, SyntaxError):
                    traits_list = []
                    
                # EXTRAEMOS LOS NUEVOS CAMPOS PARA LA BACKSTORY
                gender = row.get('gender', 'unknown')
                occupation = row.get('occupation', 'unemployed')
                qualification = row.get('qualification', 'none')
                interests = row.get('interests', 'various')
                
                # Creamos el agente con todos sus datos
                new_agent = Agent(
                    agent_id=agent_id, 
                    name=name, 
                    social_activity=social_activity, 
                    traits_list=traits_list, 
                    age=age,
                    gender=gender,
                    occupation=occupation,
                    qualification=qualification,
                    interests=interests
                )
                agents_list.append(new_agent)
                
        # La magia de la prioridad: ordenamos la lista de mayor a menor
        agents_list.sort(key=lambda x: x.social_activity, reverse=True)
        
        print(f"[OK] Se han cargado y ordenado {len(agents_list)} agentes exitosamente.")
        
        if len(agents_list) >= 3:
            print(f"- Top 3 más activos: {agents_list[0].name}, {agents_list[1].name}, {agents_list[2].name}")
            
        return agents_list
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{filepath}'")
        return []

if __name__ == "__main__":
    mis_agentes = load_agents_from_csv("users.csv")