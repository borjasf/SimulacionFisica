# Configuración global de la simulación

# Reproducibilidad: None para aleatoriedad real, número para determinismo auditado
RANDOM_SEED = None

# Timing de ejecución
SLEEP_TICK = 0.05       # Pausa del bucle principal (segundos)
SLEEP_DIALOGUE = 2.0    # Pausa para mostrar diálogos en consola

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

# Motor de decisión: selecciona entre estocástico o semántico
DECISION_ENGINE = "MARKOV"          # "MARKOV" (rápido, INE) o "LLM" (lento, IA)

# Validación del motor de decisión
if DECISION_ENGINE not in ["MARKOV", "LLM"]:
    raise ValueError(f"DECISION_ENGINE debe ser 'MARKOV' o 'LLM'")

# Modo de prueba y configuración de output
MOCK_LLM = True         # True: no llamar a Gemini (pruebas rápidas)
PRINT_LOGS = False        # False: sin logs por consola (velocidad máxima)
MAX_TURNS = 10000     # Límite de turnos (0 = sin límite)