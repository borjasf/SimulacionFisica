# --- CONSTANTES DE TIEMPO ---
SLEEP_TICK = 0.05       # Pausa del bucle principal
SLEEP_DIALOGUE = 2.0    # Pausa de lectura en consola para los diálogos

# --- CONSTANTES ESPACIALES (MODELO G-EPR) ---
BASE_EXPLORATION_RHO = 0.8  
BASE_SPATIAL_BETA = 2.0     

# --- CONSTANTES DE MEMORIA Y RECUPERACIÓN (STANFORD PAPER) ---
# Pesos de la fórmula de fusión de recuerdos (Deben sumar 1.0)
WEIGHT_SIMILARITY = 0.5     # Peso de la similitud semántica (Vectores)
WEIGHT_RECENCY = 0.3        # Peso de lo reciente que fue el recuerdo
WEIGHT_IMPORTANCE = 0.2     # Peso de la carga emocional/importancia

MEMORY_DECAY_FACTOR = 0.05  # Factor de decaimiento temporal (a mayor número, olvidan más rápido)
MAX_IMPORTANCE_SCORE = 10.0 # Normalizador de la nota de importancia (por defecto es del 1 al 10)
MAX_RETRIEVED_MEMORIES = 3  # Número máximo de recuerdos a inyectar en el prompt del LLM

# UMBRAL PARA LA PUNTUACIÓN DE HOMOFILIA (A partir de qué puntuación se consideran que los agentes interactúan)
THRESHOLD = 3