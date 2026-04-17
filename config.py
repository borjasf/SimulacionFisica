# --- CONSTANTES DE TIEMPO ---
SLEEP_TICK = 0.05       # Pausa del bucle principal
SLEEP_DIALOGUE = 2.0    # Pausa de lectura en consola para los diálogos

# --- CONSTANTES ESPACIALES (MODELO G-EPR) ---
# [A review of human mobility...]
BASE_EXPLORATION_RHO = 0.8 #Página 12. En la referencia [20] del documento es 0.6 de base, pero al ser ejecuciones "cortas" y las personas venir de base sin conocimiento previo, intentamos acelerar ese proceso de reconocimiento de lugares.
BASE_GAMMA = 0.5 #Página 12.
BASE_SPATIAL_BETA = 2.0 # Página 15 del estudio: "The distance exponent β is typically found to be around 2, consistent with a gravity model of mobility."

MEMORY_DECAY_FACTOR = 0.05  # Factor de decaimiento temporal (a mayor número, olvidan más rápido)
MAX_IMPORTANCE_SCORE = 10.0 # Normalizador de la nota de importancia (por defecto es del 1 al 10)
MAX_RETRIEVED_MEMORIES = 3  # Número máximo de recuerdos a inyectar en el prompt del LLM

# --- CONSTANTES DE RED SOCIAL Y PROBABILIDAD (MODELO CONTINUO) ---
# Probabilidades de interacción al cruzarse
FRIEND_INTERACTION_PROB = 0.85      # Probabilidad base de que dos amigos se paren a hablar (85%)
MIN_INTERACTION_PROB = 0.5         # Suelo probabilístico: Interacción por puro azar entre opuestos (5%)
MAX_INTERACTION_PROB = 0.95         # Techo probabilístico: Límite máximo para desconocidos afines (95%)

# Multiplicadores
HOMOPHILY_PROB_MULTIPLIER = 0.20    # Cada punto de homofilia suma un 10% de probabilidad
FRIEND_PRIORITY_BONUS = 500         # Puntuación inflada para que los amigos lideren el orden de prioridad


# --- MODO TESTER / DEBUG ---
MOCK_LLM = True         # Si es True, no llama a Gemini (ahorra tiempo y dinero en pruebas largas)
PRINT_LOGS = False        # Apaga los prints de los turnos para que la consola vaya a máxima velocidad
MAX_TURNS = 10000         # Si es > 0, la simulación se detendrá sola al llegar a este turno