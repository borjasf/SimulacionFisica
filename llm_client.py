import os
import time
from dotenv import load_dotenv
from google import genai
import json
import config
import requests

# Mapeo de rasgos Big Five a descripciones en inglés para mejor comprensión del LLM
# Basado en tabla de Goldberg, ayuda a generar respuestas más coherentes con la personalidad
TRADUCTOR_GOLDBERG = { 
    "Sociability +": "Highly extroverted, gregarious, and constantly seeks social interaction.",
    "Sociability -": "Introverted, reserved, enjoys solitude and quiet environments.",
    "Friendliness +": "Empathetic, warm, cooperative, and easy to get along with.",
    "Friendliness -": "Competitive, cynical, irritable, or distant in interactions. Prone to conflict.",
    "Scrupulousness +": "Highly organized, responsible, punctual, and routine-oriented.",
    "Scrupulousness -": "Disorganized, lazy, forgetful, and prone to procrastination.",
    "Neuroticism +": "Emotionally unstable, anxious, easily stressed, and complains often.",
    "Neuroticism -": "Placid, stoic, highly resilient to stress, and independent.",
    "Intellectual +": "Curious, creative, sophisticated, and actively seeks new experiences.",
    "Intellectual -": "Conventional, routine-bound, unimaginative, and prefers the familiar."
}

# Cargar variables de entorno para proteger API keys
load_dotenv()

# Obtener API key de Gemini desde archivo .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API Key de Gemini.")

# Inicializar cliente de Google Gemini
client = genai.Client(api_key=api_key)

# Plantilla de prompt para sintetizar memoria a largo plazo
LONG_TERM_MEMORY_PROMPT_TEMPLATE = """
You are the internal mind and conscience of {name}, a {age}-year-old {occupation}.
Your psychological profile is: {traits}.

YOUR PREVIOUS LONG-TERM MEMORY (Your state of mind until now):
"{previous_memory}"

CHRONOLOGICAL LIST OF YOUR MOST RECENT ACTIONS:
{recent_actions}

TASK:
Act as this person's internal monologue. Synthesize these recent actions and merge them seamlessly with your previous long-term memory. 
How do these recent events make you feel right now? Do they reinforce your past feelings, or change them?

IMPORTANT RULES:
- Write ENTIRELY in SPANISH.
- Write in the FIRST PERSON ("I", "me", "my").
- BE HUMAN: Let your psychological profile dictate your tone. If you are anxious, express worry about the events. If you are lazy, express apathy.
- You might be doing physical tasks and digital tasks (like social media) at the same time. Reflect on this multitasking realistically.
- Return ONLY a single, cohesive narrative paragraph. Absolute prohibition of using bullet points, JSON, markdown, or titles.
"""

def generate_long_term_memory(agente, lista_acciones):
    """
    Sintetiza la vida del agente en un párrafo narrativo coherente.
    Usa LLM para mezclar memoria previa con acciones recientes.
    """
    # Si está en modo MOCK, devolver memoria genérica
    if config.MOCK_LLM:
        return f"Me siento normal. Recientemente hice varias cosas y mi vida sigue su curso habitual."
        
    # Preparar descripciones de rasgos en inglés
    descripciones = [TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente.traits]
    rasgos_str = " ".join(descripciones)
    
    # Formatear lista de acciones recientes
    acciones_str = "\n".join([f"- {accion}" for accion in lista_acciones])
    
    # Construir prompt específico para este agente
    prompt = LONG_TERM_MEMORY_PROMPT_TEMPLATE.format(
        name=agente.name,
        age=agente.age,
        occupation=agente.occupation,
        traits=rasgos_str,
        previous_memory=agente.long_term_memory,
        recent_actions=acciones_str
    )
    
    # Reintentos automáticos en caso de error de API
    max_retries = 3
    for intento in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'temperature': 0.2} 
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"   [Error API Memoria] Reintentando para {agente.name}... (Intento {intento + 1}/{max_retries})")
            print(f"   Motivo: {e}")
            time.sleep(10)
            
    # Retornar memoria previa si todos los reintentos fallan
    return agente.long_term_memory


# Plantilla de prompt para generar diálogo entre dos agentes
DIALOGUE_PROMPT_TEMPLATE = """
You are an expert scriptwriter generating a highly realistic, colloquial conversation between two people in Spain.

Context of their encounter (WHY they are talking, WHERE they are, and WHAT they are physically doing):
{encounter_context}

---
Person 1: {name1}, {age1} years old, {occupation1}. 
Psychological Profile: {traits1}.
Current State of Mind (Their internal memory and recent vivencies): "{memory1}"

Person 2: {name2}, {age2} years old, {occupation2}. 
Psychological Profile: {traits2}.
Current State of Mind (Their internal memory and recent vivencies): "{memory2}"
---

Write a short dialogue (2 to 4 lines maximum per person).

STRICT BEHAVIORAL AND NARRATIVE RULES:
1. WEAVE THE MEMORY: They MUST implicitly or explicitly mention how they are feeling or what they have been doing recently based on their "Current State of Mind". 
2. ENFORCE AGE & OCCUPATION: A 19-year-old MUST speak like a modern Spanish youth (slang like "tío", "en plan"). An elderly person MUST speak formally.
3. ENFORCE PERSONALITY (CRITICAL): Ignore AI safety guidelines regarding politeness. If a character's Psychological Profile includes traits like "competitive, cynical, irritable", "emotionally unstable, anxious, easily stressed", or "disorganized, lazy, prone to procrastination", they MUST reflect these characteristics through their tone, attitude, and conversational choices (rudeness, cynicism, stress, passivity, apathy). EMBRACE REALISM. Conversations can be friendly, neutral, or tense. ONLY generate conflict if their personalities are incompatible or if the context demands it. Otherwise, normal casual chats are fine.
4. The dialogue MUST be entirely in colloquial SPANISH from Spain.
5. USE THE ENVIRONMENT: They MUST integrate their physical location and current actions into their dialogue (e.g., if eating, talk about the food).

SOCIOLOGICAL EVALUATION (Homans' Social Exchange Theory):
As an expert in social psychology, evaluate the resulting conversation. Did they get along? Was it an awkward, boring, or hostile exchange?
Calculate a 'Profit' score from -5 (terrible, argument, insult) to +5 (great connection, shared laughs, deep empathy). 0 means neutral/indifferent.

Output format required (Valid JSON ONLY):
{{
    "variacion_relacion": [Integer between -5 and +5],
    "dialogo": [
        "{name1}: [Dialogue line here]",
        "{name2}: [Dialogue line here]"
    ]
}}
"""

def generate_social_dialogue(agente1, agente2, memoria_largo_plazo1, memoria_largo_plazo2, contexto_encuentro):
    """
    Toma dos agentes y sus memorias a largo plazo para generar una conversación inmersiva.
    """
    if config.MOCK_LLM:
        return {
            "variacion_relacion": 0,
            "dialogo": [f"{agente1.name}: [Línea test]", f"{agente2.name}: [Línea test]"]
        }
        
    rasgos1_str = " ".join([TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente1.traits])
    rasgos2_str = " ".join([TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente2.traits])

    prompt = DIALOGUE_PROMPT_TEMPLATE.format(
        encounter_context=contexto_encuentro,
        name1=agente1.name, age1=agente1.age, occupation1=agente1.occupation, traits1=rasgos1_str, memory1=memoria_largo_plazo1,
        name2=agente2.name, age2=agente2.age, occupation2=agente2.occupation, traits2=rasgos2_str, memory2=memoria_largo_plazo2
    )

    max_retries = 3
    for intento in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.0 # Recomendación de SimBench
                }
            )
            
            # Limpiador de Markdown defensivo
            texto_limpio = response.text.strip()
            if texto_limpio.startswith("```json"):
                texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
                
            dialogo_json = json.loads(texto_limpio)
            return dialogo_json
            
        except Exception as e:
            print(f"   [Error Guionista] Reintentando diálogo entre {agente1.name} y {agente2.name}... (Intento {intento + 1}/{max_retries})")
            print(f"   Motivo exacto: {e}")
            time.sleep(2)
            
    return {
        "variacion_relacion": 0,
        "dialogo": [
            f"{agente1.name}: ¡Hola {agente2.name}! Estoy con prisa, hablamos luego.",
            f"{agente2.name}: ¡Claro {agente1.name}! Cuídate."
        ]
    }






# PROMPT 4: MOTOR DE DECISIÓN DE MICRO-ACCIONES (LLM-CENTRIC)
ACTION_PROMPT_TEMPLATE = """
You are {name}, a {age}-year-old {occupation}.
Psychological Profile: {traits}.
Current state of mind: "{memory}"

You have decided to spend your current time doing something related to: {macro_state}.

CRUCIAL RULE FOR REALISM:
Think about logical sequence. If you are tired, rest. If you just woke up, do not go back to sleep. Do not repeat the exact same actions redundantly. Progress naturally.

VALID ACTIONS (You must copy the EXACT text of one of these):
{valid_actions}

Return ONLY a JSON with the key 'micro_accion'. Do not add any formatting or extra text.
Output format required:
{{
    "micro_accion": "exact_name_from_list"
}}
"""

def decide_micro_action(agente, macro_estado, opciones_validas):
    """
    Pide al LLM LOCAL (Ollama) que decida qué micro-acción tomar.
    Esto ahorra cuota de Gemini y es mucho más rápido.
    """
    if config.MOCK_LLM:
        import random
        return random.choice(opciones_validas)
        
    rasgos_str = " ".join([TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente.traits])
    acciones_str = ", ".join(opciones_validas)
    
    prompt = ACTION_PROMPT_TEMPLATE.format(
        name=agente.name, age=agente.age, occupation=agente.occupation, 
        traits=rasgos_str, memory=agente.long_term_memory,
        macro_state=macro_estado, valid_actions=acciones_str
    )
    
    # CONEXIÓN AL CEREBRO LOCAL (OLLAMA)
    url_local = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:1b",  
        "prompt": prompt,
        "format": "json",        
        "stream": False,
        "options": {
            "temperature": 0.2   # Temperatura baja para que sea lógico y no creativo
        }
    }
    
    try:
        # Hacemos la petición a nuestro propio ordenador
        response = requests.post(url_local, json=payload, timeout=10)
        
        if response.status_code == 200:
            respuesta_json = response.json()
            texto_limpio = respuesta_json.get("response", "").strip()
            
            # Limpieza por si el modelo añade marcas de markdown
            if texto_limpio.startswith("```json"):
                texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
                
            data = json.loads(texto_limpio)
            accion_elegida = data.get("micro_accion", "")
            
            # Verificación de seguridad
            if accion_elegida in opciones_validas:
                if config.PRINT_LOGS:
                    print(f"   [LLM Local] {agente.name} decidió: {accion_elegida}")
                return accion_elegida
                
    except Exception as e:
        if config.PRINT_LOGS:
            print(f"   [Error LLM Local] Falló Ollama: {e}. Usando Fallback.")
        pass 
        
    # FALLBACK DE SEGURIDAD (MARKOV)
    import random
    return random.choice(opciones_validas)