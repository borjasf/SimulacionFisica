import sys
import os
import json

# --- MAGIA PARA IMPORTAR DESDE LA CARPETA PADRE ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import llm_client
import config

# ==============================================================================
# ENTORNO DE PRUEBAS DE ESTRÉS PARA PROMPTS (QA TESTING)
# ==============================================================================

# FORZAMOS EL USO DE LA API REAL (Apagamos el Mock temporalmente)
config.MOCK_LLM = False

class MockAgent:
    """Clase falsa ligera para inyectar datos en llm_client sin arrancar la simulación."""
    def __init__(self, name, age, occupation, traits, interests="", qualification="None", last_reflection="Mi vida es normal."):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.traits = traits
        self.interests = interests
        self.qualification = qualification
        self.long_term_memory = last_reflection  # Ajustado al nuevo nombre
        self.gender = "unknown"

def imprimir_resultado_json(titulo, json_data):
    """Formatea la salida en la consola para leerla fácil."""
    print(f"\n{'='*60}\n{titulo}\n{'-'*60}")
    # Si es un string (como la memoria), lo imprimimos tal cual. Si es diccionario, como JSON.
    if isinstance(json_data, dict):
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    else:
        print(json_data)
    print("="*60)

def run_test_1_espejo():
    print("\n\n>>> INICIANDO PRUEBA 1: EL TEST DEL ESPEJO (Reflexión vs Personalidad)")
    acciones_comunes = ["Fui a Discoteca_Sur", "Hablé con 3 desconocidos", "Bailé mucho", "Llegué tarde a casa con mucho ruido"]
    
    agente_fiestero = MockAgent("Leo", 22, "Estudiante", ['Sociability +', 'Friendliness +'])
    agente_agobiado = MockAgent("Arthur", 25, "Programador", ['Sociability -', 'Neuroticism +'])
    
    res_fiestero = llm_client.generate_long_term_memory(agente_fiestero, acciones_comunes)
    imprimir_resultado_json("Reflexión de LEO (Extrovertido)", res_fiestero)
    
    res_agobiado = llm_client.generate_long_term_memory(agente_agobiado, acciones_comunes)
    imprimir_resultado_json("Reflexión de ARTHUR (Introvertido/Ansioso)", res_agobiado)

def run_test_2_choque():
    print("\n\n>>> INICIANDO PRUEBA 2: CHOQUE DE PERSONALIDADES (Diálogo Tenso)")
    agente_borde = MockAgent("Karen", 45, "Gerente", ['Friendliness -', 'Neuroticism +'])
    agente_pesado = MockAgent("Steve", 30, "Comercial", ['Sociability +', 'Friendliness +'])
    
    contexto = "Se acaban de conocer por primera vez en la cola del supermercado porque Karen le ha pisado a Steve sin querer."
    
    # Llamada ajustada a los 5 parámetros actuales
    resultado = llm_client.generate_social_dialogue(
        agente_borde, agente_pesado, 
        "Estresada y con prisa", "Feliz y relajado", 
        contexto
    )
    imprimir_resultado_json("Diálogo (Karen vs Steve)", resultado)

def run_test_3_generacional():
    print("\n\n>>> INICIANDO PRUEBA 3: BRECHA GENERACIONAL (Tono y Edad)")
    agente_mayor = MockAgent("Eusebio", 78, "Jubilado", ['Scrupulousness +'], "Jardinería", "Primary School")
    agente_joven = MockAgent("Kevin", 19, "Estudiante Universitario", ['Intellectual -'], "Videojuegos", "High School")
    
    contexto = "Se acaban de conocer en el Parque_Central. Están charlando para presentarse."
    
    resultado = llm_client.generate_social_dialogue(
        agente_mayor, agente_joven, 
        "Tranquilo paseando", "Aburrido mirando el móvil", 
        contexto
    )
    imprimir_resultado_json("Diálogo (Eusebio vs Kevin)", resultado)

def run_test_4_nicho():
    print("\n\n>>> INICIANDO PRUEBA 4: EL TEST DE NICHO (Intereses Específicos)")
    agente_a = MockAgent("Sheldon", 30, "Físico", ['Intellectual +'], "Física Cuántica, Agujeros Negros")
    agente_b = MockAgent("Leonard", 32, "Físico", ['Intellectual +'], "Física Cuántica, Agujeros Negros")
    
    contexto = "Son amigos. Quieren ponerse al día y hablar sobre su interés común en la Física Cuántica."
    
    resultado = llm_client.generate_social_dialogue(
        agente_a, agente_b, 
        "Emocionado por la ciencia cuántica", "Curioso y receptivo", 
        contexto
    )
    imprimir_resultado_json("Diálogo Nerd (Sheldon vs Leonard)", resultado)

if __name__ == "__main__":
    print(" INICIANDO BATERÍA DE PRUEBAS DE LLM ")
    print("Paciencia, Gemini está escribiendo...\n")
    
    try:
        run_test_1_espejo()
        run_test_2_choque()
        run_test_3_generacional()
        run_test_4_nicho()
        print("\n¡TODAS LAS PRUEBAS FINALIZADAS!")
    except Exception as e:
        print(f"\n ERROR CRÍTICO EN LA API DE GEMINI: {e}")