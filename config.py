# Configuración global de la simulación

# Reproducibilidad: None para aleatoriedad real, número para determinismo auditado
RANDOM_SEED = 42

# Timing de ejecución
SLEEP_TICK = 0.05       # Pausa del bucle principal (segundos)
SLEEP_DIALOGUE = 2.0    # Pausa para mostrar diálogos en consola

# Atributos iniciales de los agentes
INITIAL_BIOLOGICAL_LEVEL = 100  # Nivel inicial de saciedad y energía
BASE_URGENCY_K = 3.0            # Coeficiente de urgencia (k)

INITIAL_SHORT_TERM_MEMORY = "Acabo de despertar."                                       # Recuerdo inmediato de primera acción base
INITIAL_LONG_TERM_MEMORY = "Últimamente mi rutina ha sido bastante normal y estable."   # Recuerdo general de vida inicial

# Parámetros del modelo G-EPR de exploración espacial
# Controla el balance entre exploración de lugares nuevos y retorno a conocidos
BASE_EXPLORATION_RHO = 0.8      # Intensidad de exploración (rho)
BASE_GAMMA = 0.7                # Exponente de saturación (gamma)
BASE_SPATIAL_BETA = 2.0         # Exponente de distancia en modelo de gravedad

# Probabilidades de interacción social entre agentes
FRIEND_INTERACTION_PROB = 0.85      # Amigos se hablan con certeza
MIN_INTERACTION_PROB = 0.05          # Mínimo: solo por azar
MAX_INTERACTION_PROB = 0.95         # Máximo: límite en desconocidos afines
HOMOPHILY_PROB_MULTIPLIER = 0.3    # Cada punto de compatibilidad suma probabilidad
FRIEND_PRIORITY_BONUS = 500         # Bonus para priorizar amigos en encuentros

# Numeros mágicos homofilia
HOMOPHILY_SCALE_MULTIPLIER = 10     # Cada punto de similitud se multiplica por este factor para escalar la puntuación de homofilia
FRIENDSHIP_THRESHOLD_GAIN = 60      # Puntos de homofilia necesarios para que dos agentes se consideren amigos (ajustado por el multiplicador)
FRIENDSHIP_THRESHOLD_LOSS = 40      # Puntos de homofilia por debajo de los cuales se pierde la amistad (ajustado por el multiplicador)

# Parámetros del LLM
LLM_MAX_RETRIES = 3
LLM_RETRY_DELAY_MEMORIZAR = 10.0  # Segundos de espera si falla la Fase 1 (Memoria)
LLM_RETRY_DELAY_DIALOGUE = 2.0    # Segundos de espera si falla la Fase 2 (Diálogo)

# Variables del motor biológico
MAX_BIOLOGICAL_LEVEL = 100  # Límite superior para Energía y Saciedad

# Ritmo de recuperación energética en el estado DESCANSO
ENERGY_RECOVERY_DEEP_SLEEP = 100
ENERGY_RECOVERY_LIGHT_REST = 50

# Tasas de desgaste energético por turno
ENERGY_DECAY_HIGH = 7       # Aplicado a micro-acciones de alto impacto físico
ENERGY_DECAY_NORMAL = 5     # Aplicado a rutinas pasivas o sedentarias

# Ritmo de recuperación de saciedad en el estado ALIMENTACION
SATIETY_RECOVERY_FULL = 100 # Ingestas completas en hogar o restaurantes
SATIETY_RECOVERY_LIGHT = 40 # Ingestas ligeras o snacks rápidos

# Tasas de desgaste de saciedad por turno
SATIETY_DECAY_HIGH = 20     # Ejercicio físico o tareas domésticas intensas
SATIETY_DECAY_NORMAL = 15   # Ritmo metabólico basal en el resto de acciones

# Motor de decisión: selecciona entre estocástico o semántico
DECISION_ENGINE = "MARKOV"          # "MARKOV" (rápido, INE) o "LLM" (lento, IA)

# Validación del motor de decisión
if DECISION_ENGINE not in ["MARKOV", "LLM"]:
    raise ValueError(f"DECISION_ENGINE debe ser 'MARKOV' o 'LLM'")

# Modo de prueba y configuración de output
MOCK_LLM = True         # True: no llamar a Gemini (pruebas rápidas)
PRINT_LOGS = False        # False: sin logs por consola (velocidad máxima)
MAX_TURNS = 50000     # Límite de turnos (0 = sin límite)

# Activar mapa para pruebas
USE_LAB_MAP = False
USE_PETRI_MAP = False

# Manda sobre cualquier rasgo psicológico para pruebas matemáticas
FORCE_URGENCY_K = None  # None = usa el k real de cada agente, número = fuerza global de urgencia (Ej: 5.0)

# Interruptor de Laboratorio Psicológico 
# None = Usa la personalidad real del CSV. 
# String = Sobrescribe la personalidad de toda la ciudad (Ej: "Neuroticism +")
OVERRIDE_TRAIT = None