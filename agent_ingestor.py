import csv
import ast
from agent import Agent

def load_agents_from_csv(filepath):
    """
    Lee archivo users.csv, instancia agentes y los ordena por actividad social.
    """
    agents_list = []
    
    try:
        # Abrir CSV y leer filas
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Extraer ID del agente
                agent_id = row.get('username', row.get('id', 'unknown')).strip()
                name = row.get('name', 'SinNombre')
                
                # Extraer edad (por defecto 30)
                try:
                    age = int(row.get('age', 30))
                except ValueError:
                    age = 30
                
                # Extraer actividad social (por defecto 0.0)
                try:
                    social_activity = float(row.get('social_activity', 0.0))
                except ValueError:
                    social_activity = 0.0

                # Extraer lista de rasgos desde string
                traits_raw = row.get('traits', "[]")
                try:
                    traits_list = ast.literal_eval(traits_raw)
                except (ValueError, SyntaxError):
                    traits_list = []
                    
                # Extraer datos demográficos para narrativa
                gender = row.get('gender', 'unknown')
                occupation = row.get('occupation', 'unemployed')
                qualification = row.get('qualification', 'none')
                interests = row.get('interests', 'various')
                
                # Instanciar nuevo agente con todos sus atributos
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
    
def load_friendships_from_csv(agents_list, filepath="friendships.csv"):
    """
    Lee el CSV y establece amistades SOLO si el seguimiento es mutuo 
    (A sigue a B, y B sigue a A).
    """
    # 1. Diccionario rápido para acceder a los objetos Agente por su ID
    diccionario_agentes = {str(a.id): a for a in agents_list}
    
    # 2. Mapa temporal de seguimientos brutos: { "id_1": {"id_2", "id_3"} }
    seguimientos = {} 
    
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                follower = str(row.get('follower', '')).strip()
                followed = str(row.get('followed', '')).strip()
                
                if follower and followed:
                    if follower not in seguimientos:
                        seguimientos[follower] = set()
                    seguimientos[follower].add(followed)
        
        # 3. Validación de Reciprocidad (El Match)
        for agent_id, agent_obj in diccionario_agentes.items():
            if agent_id in seguimientos:
                for followed_id in seguimientos[agent_id]:
                    if followed_id in seguimientos and agent_id in seguimientos[followed_id]:
                        # Es mutuo. Verificamos que el amigo exista en el mundo y lo añadimos
                        if followed_id in diccionario_agentes and followed_id not in agent_obj.amigos:
                            agent_obj.amigos.append(followed_id)
                            
        print(f"[OK] Red social validada. Amistades recíprocas establecidas.")
        
    except FileNotFoundError:
        print(f"Aviso: No se encontró {filepath}. Los agentes no tendrán amistades previas.")    

if __name__ == "__main__":
    mis_agentes = load_agents_from_csv("users.csv")