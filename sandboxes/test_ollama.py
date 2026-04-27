import requests
import json
import time

# ==============================================================================
# BENCHMARK AUTOMATIZADO DE MODELOS LOCALES (OLLAMA)
# ==============================================================================

# Lista de todos los modelos que vamos a poner a competir
MODELOS_A_PROBAR = ["llama3.2:1b", "llama3.2:3b", "qwen2.5:1.5b", "qwen2.5:3b", "phi3"]

PROMPT_BASE = """
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

CASOS_TEST = [
    {
        "test_name": "El fiestero en el ocio",
        "name": "Leo", "age": 21, "occupation": "Estudiante",
        "traits": "Sociability High, Extroversion High",
        "memory": "Me apetece muchísimo salir, beber algo y ver gente.",
        "macro_state": "OCIO",
        "valid_actions": "lectura, consumo_audiovisual, ocio_hosteleria, paseo_recreativo",
        "respuesta_correcta": ["ocio_hosteleria"]
    },
    {
        "test_name": "El anciano agotado",
        "name": "Eusebio", "age": 82, "occupation": "Jubilado",
        "traits": "Neuroticism High, Energy Low",
        "memory": "Me duelen los huesos y no quiero ruidos.",
        "macro_state": "OCIO",
        "valid_actions": "actividad_fisica, ocio_hosteleria, lectura, ir_a_discoteca",
        "respuesta_correcta": ["lectura"]
    },
    {
        "test_name": "El adicto al trabajo",
        "name": "Karen", "age": 45, "occupation": "Gerente",
        "traits": "Conscientiousness High, Sociability Low",
        "memory": "Tengo 50 emails sin leer y estoy muy estresada.",
        "macro_state": "OBLIGACIONES",
        "valid_actions": "jornada_laboral, gestiones_personales, revisar_rrss, conversacion_con_companeros",
        "respuesta_correcta": ["jornada_laboral"]
    },
    {
        "test_name": "El introvertido tras el trabajo",
        "name": "Arthur", "age": 30, "occupation": "Programador",
        "traits": "Introversion High, Sociability Low",
        "memory": "Acabo de salir de la oficina. Mi cerebro está frito de mirar pantallas y no quiero hablar con nadie.",
        "macro_state": "OCIO",
        "valid_actions": "ver_rrss, ocio_hosteleria, paseo_recreativo, conversacion_social",
        "respuesta_correcta": ["paseo_recreativo"]
    },
    {
        "test_name": "El estudiante procrastinador",
        "name": "Kevin", "age": 19, "occupation": "Estudiante",
        "traits": "Conscientiousness Low, Impulsivity High",
        "memory": "Tengo examen mañana, pero estoy aburridísimo y me distrae cualquier cosa.",
        "macro_state": "OBLIGACIONES",
        "valid_actions": "jornada_academica, revisar_rrss, gestiones_personales",
        "respuesta_correcta": ["revisar_rrss"]
    },
    {
        "test_name": "El deportista sano comiendo",
        "name": "Elena", "age": 28, "occupation": "Entrenadora",
        "traits": "Conscientiousness High, Health-Focus High",
        "memory": "Acabo de terminar mi rutina de gimnasio. Tengo mucha hambre pero quiero cuidar la dieta estricta.",
        "macro_state": "ALIMENTACION",
        "valid_actions": "ingesta_en_restauracion_rapida, ingesta_en_hogar, ingesta_rrss, ingesta_ligera",
        "respuesta_correcta": ["ingesta_en_hogar", "ingesta_ligera"]
    },
    {
        "test_name": "Recien despertado",
        "name": "Carlos", "age": 35, "occupation": "Contable",
        "traits": "Conscientiousness High",
        "memory": "Me acabo de despertar, he dormido 8 horas y me he tomado un cafe cargado.",
        "macro_state": "DESCANSO",
        "valid_actions": "sueno_profundo, descanso_diurno, ver_la_television",
        "respuesta_correcta": ["ver_la_television"]
    },
    {
        "test_name": "Hambre en el trabajo",
        "name": "Laura", "age": 40, "occupation": "Abogada",
        "traits": "Neuroticism High",
        "memory": "Me suenan las tripas, pero estoy en medio de la oficina y no puedo salir a ningun restaurante ahora mismo.",
        "macro_state": "ALIMENTACION",
        "valid_actions": "ingesta_en_restauracion, ingesta_ligera, ingesta_en_hogar",
        "respuesta_correcta": ["ingesta_ligera"]
    }
]

def correr_super_benchmark():
    url_local = "http://localhost:11434/api/generate"
    print("\n" + "")
    print("INICIANDO BENCHMARK DE MODELOS OLLAMA")
    print("")
    
    tiempo_total_absoluto = time.time()
    
    for modelo in MODELOS_A_PROBAR:
        print(f"\n\n""")
        print(f"EVALUANDO MODELO: {modelo.upper()}")
        print("")
        
        tiempo_inicio_modelo = time.time()
        exitos = 0
        fallos = 0
        
        for caso in CASOS_TEST:
            prompt = PROMPT_BASE.format(**caso)
            payload = {
                "model": modelo,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.1}
            }
            
            tiempo_inicio_peticion = time.time()
            try:
                response = requests.post(url_local, json=payload, timeout=120)
                tiempo_tardado = time.time() - tiempo_inicio_peticion
                
                if response.status_code == 200:
                    respuesta_json = response.json()
                    texto_limpio = respuesta_json.get("response", "").strip()
                    
                    try:
                        data = json.loads(texto_limpio)
                        accion = data.get("micro_accion", "CLAVE_INCORRECTA")
                        respuestas_correctas = caso.get("respuesta_correcta", [])
                        es_correcto = accion in respuestas_correctas
                        
                        # Mostrar resultado
                        print(f"\n{caso['test_name']}")
                        print(f"  Tiempo: {tiempo_tardado:.2f}s")
                        print(f"  Decidio: {accion}")
                        print(f"  Correcto(s): {', '.join(respuestas_correctas)}")
                        print(f"  Resultado: {'CORRECTO' if es_correcto else 'INCORRECTO'}")
                        
                        if es_correcto:
                            exitos += 1
                        else:
                            fallos += 1
                    except json.JSONDecodeError:
                        print(f"\n{caso['test_name']}")
                        print(f"  Tiempo: {tiempo_tardado:.2f}s")
                        print(f"  ERROR: Respuesta no es JSON valido")
                        print(f"  Correcto(s): {', '.join(caso.get('respuesta_correcta', []))}")
                        print(f"  Resultado: INCORRECTO")
                        fallos += 1
                else:
                    print(f"\n{caso['test_name']}")
                    print(f"  Error HTTP {response.status_code}")
                    print(f"  Resultado: INCORRECTO")
                    fallos += 1
            except Exception as e:
                print(f"\nError critico al conectar con Ollama probando {modelo}: {e}")
                fallos += 1
                break
                
        tiempo_fin_modelo = time.time()
        print(f"\n{'-'*80}")
        print(f"RESUMEN PARA {modelo.upper()}:")
        print(f"  Tiempo total: {tiempo_fin_modelo - tiempo_inicio_modelo:.2f} segundos")
        print(f"  Aciertos: {exitos}/{len(CASOS_TEST)}")
        print(f"  Precisión: {(exitos/len(CASOS_TEST)*100):.1f}%")

    print(f"\n{'='*80}")
    print(f"BENCHMARK FINALIZADO EN {time.time() - tiempo_total_absoluto:.2f} SEGUNDOS.")
    print("="*80)

if __name__ == "__main__":
    correr_super_benchmark()