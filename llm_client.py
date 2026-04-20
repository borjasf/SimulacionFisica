import os
import time
from dotenv import load_dotenv
from google import genai
import json
import config

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

# 1. Cargamos el archivo .env para proteger la clave
load_dotenv()

# 2. Rescatamos la clave del archivo oculto
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API Key.")

# 3. Inicializamos el nuevo cliente
client = genai.Client(api_key=api_key)


# PROMPT 1: BACKSTORY (No se usa de momento)
BACKSTORY_PROMPT_TEMPLATE = """
Create a brief backstory for a {gender} person called {name}, who is {age} years old.
This person works as a {occupation} and has a qualification level of {qualification}.
Their personality is described by the following traits: {traits}. Their interests include: {interests}.
Write a short biography that tells us about their background, how they grew into the person they are today, and what drives them in life.

IMPORTANT RULES:
- Write the biography ENTIRELY IN SPANISH.
- DO NOT explain anything.
- Return ONLY the raw text. Absolute prohibition of using markdown formatting.
- DO NOT write more than 300 words and less than 150 words.
"""

def generate_agent_backstory(agente):
    descripciones = [TRADUCTOR_GOLDBERG.get(rasgo.strip(), rasgo.strip()) for rasgo in agente.traits]
    rasgos_str = " ".join(descripciones)
    
    prompt = BACKSTORY_PROMPT_TEMPLATE.format(
        gender=agente.gender, name=agente.name, age=agente.age, 
        occupation=agente.occupation, qualification=agente.qualification, 
        traits=rasgos_str, interests=agente.interests
    )
    
    max_retries = 3
    for intento in range(max_retries):
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            agente.backstory = response.text.strip()
            return agente.backstory
        except Exception as e:
            if "503" in str(e) or "429" in str(e):
                time.sleep(10)
            else:
                agente.backstory = "Backstory no disponible."
                return agente.backstory
    agente.backstory = f"{agente.name} es una persona de {agente.age} años. Biografía fallida."
    return agente.backstory


# PROMPT 2: EL MOTOR DE MEMORIA (LLM-CENTRIC)
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
- BE HUMAN: Let your psychological profile dictate your tone. If you are anxious (Neuroticism +), express worry about the events. If you are lazy (Scrupulousness -), express apathy.
- You might be doing physical tasks and digital tasks (like social media) at the same time. Reflect on this multitasking realistically.
- Return ONLY a single, cohesive narrative paragraph. Absolute prohibition of using bullet points, JSON, markdown, or titles.
"""

def generate_long_term_memory(agente, lista_acciones):
    """
    Sintetiza la vida del agente en un párrafo de texto continuo.
    """
    if config.MOCK_LLM:
        return f"Me siento normal. Recientemente hice varias cosas y mi vida sigue su curso habitual."
        
    descripciones = [TRADUCTOR_GOLDBERG.get(r.strip(), r.strip()) for r in agente.traits]
    rasgos_str = " ".join(descripciones)
    
    acciones_str = "\n".join([f"- {accion}" for accion in lista_acciones])
    
    prompt = LONG_TERM_MEMORY_PROMPT_TEMPLATE.format(
        name=agente.name,
        age=agente.age,
        occupation=agente.occupation,
        traits=rasgos_str,
        previous_memory=agente.long_term_memory,
        recent_actions=acciones_str
    )
    
    max_retries = 3
    for intento in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'temperature': 0.2} # Reducimos la alucinación
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"   [Error API Memoria] Reintentando para {agente.name}... (Intento {intento + 1}/{max_retries})")
            print(f"   Motivo exacto: {e}")
            time.sleep(10)
            
    return agente.long_term_memory


# PROMPT 3: MOTOR DE DIÁLOGO Y EVALUACIÓN SOCIOLÓGICA
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
3. ENFORCE PERSONALITY (CRITICAL): Ignore AI safety guidelines regarding politeness. If a character has "Friendliness -" or "Neuroticism +", they MUST be rude, cynical, stressed, passive-aggressive, or short-tempered. EMBRACE REALISM. Conversations can be friendly, neutral, or tense. ONLY generate conflict if their personalities are incompatible (e.g. Neuroticism +) or if the context demands it. Otherwise, normal casual chats are fine.
4. The dialogue MUST be entirely in colloquial SPANISH from Spain.
5. USE THE ENVIRONMENT: They MUST integrate their physical location and current actions into their dialogue (e.g., if eating, talk about the food).

SOCIOLOGICAL EVALUATION (Homans' Social Exchange Theory):
As an expert in social psychology, evaluate the resulting conversation. Did they get along? Was it an awkward, boring, or hostile exchange?
Calculate a 'Profit' score from -5 (terrible, argument, insult) to +5 (great connection, shared laughs, deep empathy). 0 means neutral/indifferent.

Output format required (Valid JSON ONLY):
{{
    "tema_de_conversacion": "A brief 3-word summary",
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
            "tema_de_conversacion": "Modo Test",
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
        "tema_de_conversacion": "Saludos rápidos",
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
Based ONLY on your age, occupation, and personality, which of the following specific actions do you choose to do?

VALID ACTIONS (You must copy the EXACT text of one of these):
{valid_actions}

Return ONLY a JSON with the key 'micro_accion'. Do not add any formatting or extra text.
Output format required:
{{
    "micro_accion": "exact_name_from_list"
}}
"""

def decide_micro_action(agente, macro_estado, opciones_validas):
    """Pide al LLM que decida qué micro-acción tomar basándose en su perfil."""
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
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json', 'temperature': 0.2}
        )
        
        texto_limpio = response.text.strip()
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
            
        data = json.loads(texto_limpio)
        accion_elegida = data.get("micro_accion", "")
        
        if accion_elegida in opciones_validas:
            return accion_elegida
    except Exception as e:
        pass 
        
    # Fallback de seguridad: Si la IA falla, decidimos al azar para que no crashee
    import random
    return random.choice(opciones_validas)