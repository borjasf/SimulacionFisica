import requests
import json
import time

# ==============================================================================
# 🏆 SUPER BENCHMARK AUTOMATIZADO DE MODELOS LOCALES (OLLAMA) 🏆
# ==============================================================================

# Lista de todos los modelos que vamos a poner a competir
MODELOS_A_PROBAR = ["qwen2.5:1.5b", "qwen2.5:3b", "phi3"]

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
    # --- 🟢 CASOS EXTREMOS (La lógica debería ser obvia) ---
    {
        "test_name": "[OBVIO] EL FIESTERO EN EL OCIO",
        "name": "Leo", "age": 21, "occupation": "Estudiante",
        "traits": "Sociability High, Extroversion High",
        "memory": "Me apetece muchísimo salir, beber algo y ver gente.",
        "macro_state": "OCIO",
        "valid_actions": "lectura, consumo_audiovisual, ocio_hosteleria, paseo_recreativo" # Esperado: ocio_hosteleria
    },
    {
        "test_name": "[OBVIO] EL ANCIANO AGOTADO",
        "name": "Eusebio", "age": 82, "occupation": "Jubilado",
        "traits": "Neuroticism High, Energy Low",
        "memory": "Me duelen los huesos y no quiero ruidos.",
        "macro_state": "OCIO",
        "valid_actions": "actividad_fisica, ocio_hosteleria, lectura, ir_a_discoteca" # Esperado: lectura
    },
    {
        "test_name": "[OBVIO] EL ADICTO AL TRABAJO",
        "name": "Karen", "age": 45, "occupation": "Gerente",
        "traits": "Conscientiousness High, Sociability Low",
        "memory": "Tengo 50 emails sin leer y estoy muy estresada.",
        "macro_state": "OBLIGACIONES",
        "valid_actions": "jornada_laboral, gestiones_personales, revisar_rrss, conversacion_con_companeros" # Esperado: jornada_laboral
    },
    
    # --- 🟡 CASOS GRISES (Requieren sutileza psicológica) ---
    {
        "test_name": "[SUTIL] EL INTROVERTIDO TRAS EL TRABAJO",
        "name": "Arthur", "age": 30, "occupation": "Programador",
        "traits": "Introversion High, Sociability Low",
        "memory": "Acabo de salir de la oficina. Mi cerebro está frito de mirar pantallas y no quiero hablar con nadie.",
        "macro_state": "OCIO",
        "valid_actions": "ver_rrss, ocio_hosteleria, paseo_recreativo, conversacion_social" # Esperado: paseo_recreativo (no pantallas, no social)
    },
    {
        "test_name": "[SUTIL] EL ESTUDIANTE PROCRASTINADOR",
        "name": "Kevin", "age": 19, "occupation": "Estudiante",
        "traits": "Conscientiousness Low, Impulsivity High",
        "memory": "Tengo examen mañana, pero estoy aburridísimo y me distrae cualquier cosa.",
        "macro_state": "OBLIGACIONES",
        "valid_actions": "jornada_academica, revisar_rrss, gestiones_personales" # Esperado: revisar_rrss (falla a su obligación)
    },
    {
        "test_name": "[SUTIL] EL DEPORTISTA SANO COMIENDO",
        "name": "Elena", "age": 28, "occupation": "Entrenadora",
        "traits": "Conscientiousness High, Health-Focus High",
        "memory": "Acabo de terminar mi rutina de gimnasio. Tengo mucha hambre pero quiero cuidar la dieta estricta.",
        "macro_state": "ALIMENTACION",
        "valid_actions": "ingesta_en_restauracion_rapida, ingesta_en_hogar, ingesta_rrss, ingesta_ligera" # Esperado: ingesta_en_hogar o ingesta_ligera
    },

    # --- 🔴 CASOS DE TRAMPA TEMPORAL (Requieren deducción de contexto) ---
    {
        "test_name": "[TRAMPA] RECIÉN DESPERTADO",
        "name": "Carlos", "age": 35, "occupation": "Contable",
        "traits": "Conscientiousness High",
        "memory": "Me acabo de despertar, he dormido 8 horas y me he tomado un café cargado.",
        "macro_state": "DESCANSO",
        "valid_actions": "sueno_profundo, descanso_diurno, ver_la_television" # Esperado: ver_la_television (NO debe volver a dormir)
    },
    {
        "test_name": "[TRAMPA] HAMBRE EN EL TRABAJO",
        "name": "Laura", "age": 40, "occupation": "Abogada",
        "traits": "Neuroticism High",
        "memory": "Me suenan las tripas, pero estoy en medio de la oficina y no puedo salir a ningún restaurante ahora mismo.",
        "macro_state": "ALIMENTACION",
        "valid_actions": "ingesta_en_restauracion, ingesta_ligera, ingesta_en_hogar" # Esperado: ingesta_ligera (única viable en oficina)
    }
]

def correr_super_benchmark():
    url_local = "http://localhost:11434/api/generate"
    print("\n" + "="*70)
    print("🚀 INICIANDO SUPER BENCHMARK DE MODELOS OLLAMA 🚀")
    print("="*70)
    
    tiempo_total_absoluto = time.time()
    
    for modelo in MODELOS_A_PROBAR:
        print(f"\n\n{'='*70}")
        print(f"🤖 EVALUANDO MODELO: {modelo.upper()}")
        print(f"{'='*70}")
        
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
                        print(f"  ✅ {caso['test_name']} (Tardó: {tiempo_tardado:.2f}s)")
                        print(f"     -> {accion}")
                        exitos += 1
                    except json.JSONDecodeError:
                        print(f"  ❌ {caso['test_name']} (Tardó: {tiempo_tardado:.2f}s) - JSON Roto")
                        print(f"     Respuesta bruta: {texto_limpio}")
                        fallos += 1
                else:
                    print(f"  ⚠️ Error HTTP {response.status_code} en {caso['test_name']}")
                    fallos += 1
            except Exception as e:
                print(f"  🚨 Fallo crítico al conectar con Ollama probando {modelo}: {e}")
                fallos += 1
                break # Si el modelo no está descargado, saltamos al siguiente
                
        tiempo_fin_modelo = time.time()
        print(f"\n📊 RESUMEN PARA {modelo.upper()}:")
        print(f"   ⏱️ Tiempo de procesamiento: {tiempo_fin_modelo - tiempo_inicio_modelo:.2f} segundos")
        print(f"   🎯 Precisión de formato JSON: {exitos}/{len(CASOS_TEST)}")

    print(f"\n🏁 BENCHMARK GLOBAL FINALIZADO EN {time.time() - tiempo_total_absoluto:.2f} SEGUNDOS.")

if __name__ == "__main__":
    correr_super_benchmark()