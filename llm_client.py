# ==============================================================================
# ARCHIVO: llm_client.py
# DESCRIPCIÓN: Cliente de conexión con la API oficial de Google Gemini.
# FASE 1: Generación de Biografías (Backstories) basadas en el perfil demográfico.
# ==============================================================================

import os
import time
from dotenv import load_dotenv
from google import genai
import json
import config

# ==============================================================================
# DICCIONARIO SEMÁNTICO
# ==============================================================================
TRADUCTOR_GOLDBERG = {
    "Sociability +": "Highly extroverted, gregarious, and constantly seeks social interaction.",
    "Sociability -": "Introverted, reserved, enjoys solitude and quiet environments.",
    "Friendliness +": "Empathetic, warm, cooperative, and easy to get along with.",
    "Friendliness -": "Competitive, cynical, irritable, or distant in interactions.",
    "Scrupulousness +": "Highly organized, responsible, punctual, and routine-oriented.",
    "Scrupulousness -": "Disorganized, lazy, forgetful, and prone to procrastination.",
    "Neuroticism +": "Emotionally unstable, anxious, and easily stressed.",
    "Neuroticism -": "Placid, stoic, highly resilient to stress, and independent.",
    "Intellectual +": "Curious, creative, sophisticated, and actively seeks new experiences.",
    "Intellectual -": "Conventional, routine-bound, unimaginative, and prefers the familiar."
}

# 1. Cargamos el archivo .env para proteger la clave
load_dotenv()

# 2. Rescatamos la clave del archivo oculto
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API Key.")

# 3. Inicializamos el nuevo cliente
client = genai.Client(api_key=api_key)

# ==============================================================================
# PROMPTS
# (Instrucciones en inglés para maximizar el razonamiento del LLM, 
# salida solicitada explícitamente en español)
# ==============================================================================

BACKSTORY_PROMPT_TEMPLATE = """
Create a brief backstory for a {gender} person called {name}, who is {age} years old.
This person works as a {occupation} and has a qualification level of {qualification}.
Their personality is described by the following traits: {traits}. Their interests include: {interests}.
Write a short biography that tells us about their background, how they grew into the person they are today, and what drives them in life.

IMPORTANT RULES:
- Write the biography ENTIRELY IN SPANISH.
- DO NOT explain anything.
- Return ONLY the raw text. Absolute prohibition of using markdown formatting, bold text (**), italics, titles, or bullet points.
- DO NOT write more than 300 words and less than 150 words.
"""

# ==============================================================================
# FUNCIONES DE GENERACIÓN
# ==============================================================================

def generate_agent_backstory(agente):
    """
    Genera la historia de vida inicial del agente llamando al LLM.
    Utiliza los atributos estáticos de la clase Agent.
    """
    # 1. Limpiamos espacios (strip) y formateamos los rasgos a un string legible
    descripciones = [TRADUCTOR_GOLDBERG.get(rasgo.strip(), rasgo.strip()) for rasgo in agente.traits]
    rasgos_str = " ".join(descripciones)
    
    # 2. Inyectamos las variables de Python en el prompt de texto
    prompt = BACKSTORY_PROMPT_TEMPLATE.format(
        gender=agente.gender,
        name=agente.name,
        age=agente.age,
        occupation=agente.occupation,
        qualification=agente.qualification,
        traits=rasgos_str,
        interests=agente.interests
    )
    
    max_retries = 3
    for intento in range(max_retries):
        try:
            # 3. Llamada a la API (Usamos 2.5-flash que es rápido e ideal para texto)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            biografia = response.text.strip()
            
            # Guardamos la biografía en la mente del agente
            agente.backstory = biografia
            return biografia
            
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "429" in error_str:
                print(f"   [ API Saturada] Reintentando backstory para {agente.name} en 10s... (Intento {intento + 1}/{max_retries})")
                time.sleep(10)
            else:
                print(f" Error al generar backstory para {agente.name}: {error_str}")
                agente.backstory = "Backstory no disponible."
                return agente.backstory
                
    # Fallback si se agotan los reintentos
    agente.backstory = f"{agente.name} es una persona de {agente.age} años. Su biografía no se pudo generar."
    return agente.backstory


# ==============================================================================
# FASE 3: CONSOLIDACIÓN DE MEMORIA (REFLEXIÓN A LARGO PLAZO)
# ==============================================================================

REFLECTION_PROMPT_TEMPLATE = """
You are evaluating the recent life of {name}, a {age}-year-old {occupation}.
Their personality traits are: {traits}.

YOUR MENTAL BASE STATE (Your previous reflection):
"{previous_reflection}"

YOUR TOP MOST IMPORTANT RECENT VIVENCIES:
{recent_actions}

Analyze how these recent vivencies affect your mental base state from the psychological perspective of this specific person. 
Generate a high-level memory summary and rate the importance of this period in their life (1 being trivial, 10 being life-changing).

IMPORTANT RULES:
- The reflection MUST be written in SPANISH.
- The reflection MUST be in the FIRST PERSON ("I").
- You MUST return ONLY a valid JSON object. No markdown, no explanations.

Output format required:
{{
    "tema_central": "Título corto de 3 o 4 palabras",
    "resumen_narrativo": "Reflexión en primera persona de 1 o 2 frases conectando el pasado con lo reciente",
    "importancia": <número entero del 1 al 10>
}}
"""

def generate_daily_reflection(agente, lista_acciones_top):
    """
    Envía las vivencias más importantes a Gemini conectándolas con su reflexión anterior.
    """
    if config.MOCK_LLM:
        return {
            "tema_central": "Test Rápido", 
            "resumen_narrativo": "Reflexión generada en modo simulación rápida.", 
            "importancia": 5
        }
    # 1. Preparamos los datos
    descripciones = [TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente.traits]
    rasgos_str = " ".join(descripciones)
    
    # Formateamos la lista de acciones en un texto con viñetas
    acciones_str = "\n".join([f"- {accion}" for accion in lista_acciones_top])
    
    # 2. Inyectamos TODAS las variables necesarias en el prompt, incluyendo la reflexión anterior
    prompt = REFLECTION_PROMPT_TEMPLATE.format(
        name=agente.name,
        age=agente.age,
        occupation=agente.occupation,
        traits=rasgos_str,
        previous_reflection=agente.last_reflection,
        recent_actions=acciones_str
    )
    
    max_retries = 3
    for intento in range(max_retries):
        try:
            # Forzamos a Gemini a devolver un JSON válido
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            # Parseamos el texto devuelto a un diccionario de Python
            reflexion_json = json.loads(response.text.strip())
            return reflexion_json
            
        except Exception as e:
            print(f"   [Error JSON/API] Reintentando reflexión para {agente.name}... (Intento {intento + 1}/{max_retries})")
            time.sleep(10)
            
    # Fallback si falla todo
    return {
        "tema_central": "Rutina",
        "resumen_narrativo": "Siento que los últimos días han sido una continuación de mi rutina habitual.",
        "importancia": 1
    }


# ==============================================================================
# FASE 4: MOTOR DE DIÁLOGO SOCIAL
# ==============================================================================

DIALOGUE_PROMPT_TEMPLATE = """
You are a scriptwriter generating a natural, casual conversation between two people who just met or bumped into each other.

Context of their encounter (WHY they approached each other):
{encounter_context}

Person 1: {name1}, {age1} years old, {occupation1}. Personality: {traits1}.
Current Mental State: "{current_state1}"
Relevant past memories for this conversation:
{memories1}

Person 2: {name2}, {age2} years old, {occupation2}. Personality: {traits2}.
Current Mental State: "{current_state2}"
Relevant past memories for this conversation:
{memories2}

Write a short dialogue (2 to 4 lines maximum per person). 
IMPORTANT NARRATIVE RULE: They MUST explicitly talk about what they have in common based on the 'Context of their encounter' provided above. They should weave their 'Current Mental State' and 'Relevant past memories' into the conversation naturally.

IMPORTANT FORMAT RULES:
- The dialogue MUST be entirely in SPANISH.
- You MUST return ONLY a valid JSON object. No markdown.

Output format required:
{{
    "tema_de_conversacion": "A brief 3-word summary",
    "dialogo": [
        "{name1}: [Dialogue line here]",
        "{name2}: [Dialogue line here]"
    ]
}}
"""

def generate_social_dialogue(agente1, agente2, estado_actual1, estado_actual2, recuerdos_ag1, recuerdos_ag2, contexto_encuentro):
    """
    Toma dos agentes, sus recuerdos y el motivo por el que se han acercado (homofilia)
    y pide a Gemini que redacte una conversación basada en sus similitudes.
    """
    if config.MOCK_LLM:
        return {
            "tema_de_conversacion": "Modo Test",
            "dialogo": [f"{agente1.name}: [Diálogo de prueba rápido]", f"{agente2.name}: [Diálogo de prueba rápido]"]
        }
    # Formateamos rasgos y memorias (agente 1)
    rasgos1_str = " ".join([TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente1.traits])
    mems1_str = "\n".join([f"- {r['texto']}" for r in recuerdos_ag1]) if recuerdos_ag1 else "- Nada relevante reciente."
    
    # Formateamos rasgos y memorias (agente 2)
    rasgos2_str = " ".join([TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente2.traits])
    mems2_str = "\n".join([f"- {r['texto']}" for r in recuerdos_ag2]) if recuerdos_ag2 else "- Nada relevante reciente."

    # Inyectamos el contexto de homofilia en el prompt
    prompt = DIALOGUE_PROMPT_TEMPLATE.format(
        encounter_context=contexto_encuentro,
        name1=agente1.name, age1=agente1.age, occupation1=agente1.occupation, traits1=rasgos1_str, memories1=mems1_str, current_state1=estado_actual1,
        name2=agente2.name, age2=agente2.age, occupation2=agente2.occupation, traits2=rasgos2_str, memories2=mems2_str, current_state2=estado_actual2
    )

    max_retries = 3
    for intento in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            dialogo_json = json.loads(response.text.strip())
            return dialogo_json
            
        except Exception as e:
            print(f"   [Error Guionista] Reintentando diálogo entre {agente1.name} y {agente2.name}... (Intento {intento + 1}/{max_retries})")
            time.sleep(2)
            
    # Fallback conversacional
    return {
        "tema_de_conversacion": "Saludos genéricos",
        "dialogo": [
            f"{agente1.name}: ¡Hola {agente2.name}! Qué casualidad verte por aquí.",
            f"{agente2.name}: ¡Hola {agente1.name}! Sí, me alegro de saludarte."
        ]
    }

# ==========================================
# PRUEBA DE CONEXIÓN A LA API (MOCK DE AGENTE)
# ==========================================
if __name__ == "__main__":
    print("\n=== INICIANDO PRUEBA DE GENERACIÓN DE BACKSTORY ===")
    
    # Creamos un objeto falso ("mock") basado en los datos reales de Aaron (del CSV)
    class DummyAgent:
        def __init__(self):
            self.name = "Aaron"
            self.gender = "male"
            self.age = 69
            self.occupation = "astronaut"
            self.qualification = "High School Diploma"
            # Nótese el espacio intencional en Scrupulousness para probar el .strip()
            self.traits = ['Sociability +', 'Friendliness -', 'Scrupulousness - ', 'Neuroticism +', 'Intellectual +']
            self.interests = "Computer programming"
            self.backstory = ""

    agente_prueba = DummyAgent()
    
    #print(f"Generando biografía para {agente_prueba.name}...")
    # Descomentar la siguiente línea solo cuando quieras probar con la API real
    # resultado = generate_agent_backstory(agente_prueba)
    
    # print("\n--- RESULTADO DE GEMINI ---")
    # print(resultado)
    # print("---------------------------\n")