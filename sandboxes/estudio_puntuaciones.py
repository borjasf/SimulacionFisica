"""
Estudio de puntuaciones medias de homofilia entre agentes reales
"""
import csv
import random
from collections import defaultdict
import statistics
import sys
sys.path.append('..')
import config


class Agent:
    def __init__(self, row):
        self.name = row['name']
        self.age = int(row['age'])
        self.occupation = row['occupation']
        self.interests = row['interests'].strip("[]'\"").replace("'", "")  # Parse interests
        self.traits = row['traits'].strip("[]'\"").replace("'", "").split(", ")  # Parse traits
        
# Cargar agentes desde CSV
agents = []
with open('../users.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            agents.append(Agent(row))
        except Exception as e:
            print(f"Error cargando agente {row.get('name', 'Unknown')}: {e}")

print(f"✓ Cargados {len(agents)} agentes\n")

# Función para calcular homophily score
def calculate_homophily_score(agent_a, agent_b):
    score = 0
    
    # 1. SIMILITUD DEMOGRÁFICA (Edad)
    diferencia_edad = abs(agent_a.age - agent_b.age)
    if diferencia_edad <= 10:
        score += 1
        if diferencia_edad <= 5:
            score += 1

    # 2. SIMILITUD PROFESIONAL
    if agent_a.occupation.lower() != "unemployed" and agent_a.occupation.lower() == agent_b.occupation.lower():
        score += 1

    # 3. SIMILITUD DE INTERESES
    intereses_a = set([i.strip().lower() for i in agent_a.interests.split(',')])
    intereses_b = set([i.strip().lower() for i in agent_b.interests.split(',')])
    shared_interests = intereses_a.intersection(intereses_b)
    if shared_interests:
        score += len(shared_interests)

    # 4. SIMILITUD PSICOLÓGICA
    # Solo suma si AMBOS tienen el rasgo +
    
    # Sociability
    if "Sociability +" in agent_a.traits and "Sociability +" in agent_b.traits:
        score += 1

    # Friendliness
    if "Friendliness +" in agent_a.traits and "Friendliness +" in agent_b.traits:
        score += 1

    # Intellectual
    if "Intellectual +" in agent_a.traits and "Intellectual +" in agent_b.traits:
        score += 1

    return score

# ============ ANÁLISIS 1: Muestreo de pares ============
print("=" * 80)
print("ANÁLISIS 1: MUESTREO ALEATORIO DE PARES DE AGENTES")
print("=" * 80)

num_samples = min(1000, len(agents) * (len(agents) - 1) // 2)  # Limitar muestras
print(f"\nTomando {num_samples} pares aleatorios de agentes...\n")

scores = []
score_reasons = defaultdict(list)

for _ in range(num_samples):
    a, b = random.sample(agents, 2)
    score = calculate_homophily_score(a, b)
    scores.append(score)
    score_reasons[score].append((a.name, b.name))

# Estadísticas básicas
print("ESTADÍSTICAS DE PUNTUACIONES:")
print("-" * 80)
print(f"Total de pares analizados: {len(scores)}")
print(f"Puntuación mínima: {min(scores)}")
print(f"Puntuación máxima: {max(scores)}")
print(f"Puntuación media: {statistics.mean(scores):.2f}")
print(f"Mediana: {statistics.median(scores):.1f}")
print(f"Desviación estándar: {statistics.stdev(scores):.2f}")

# Distribución
print("\n" + "=" * 80)
print("DISTRIBUCIÓN DE PUNTUACIONES")
print("=" * 80)
print()

score_counts = defaultdict(int)
for score in scores:
    score_counts[score] += 1

for score in sorted(score_counts.keys()):
    count = score_counts[score]
    percentage = (count / len(scores)) * 100
    print(f"Score {score}: {percentage:.1f}%")

MULTIPLIER = config.HOMOPHILY_PROB_MULTIPLIER
MIN_PROB = config.MIN_INTERACTION_PROB
MAX_PROB = config.MAX_INTERACTION_PROB

media_prob = max(MIN_PROB, min(MAX_PROB, statistics.mean(scores) * MULTIPLIER))
print(f"\nCon un multiplicador de {MULTIPLIER}, la probabilidad media de interacción sería: {media_prob:.1%}")
