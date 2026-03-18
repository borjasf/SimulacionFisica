import time
from sentence_transformers import SentenceTransformer, util

print("Cargando el modelo local (tardará unos segundos la primera vez para descargarlo)...")
# Este es el modelo exacto que validó la investigación que analizamos
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Vamos a probar con un interés específico de un agente y tres recuerdos distintos
interes_agente = "Me apasiona la música clásica y el arte en general."

recuerdo_1 = "Ayer fui a un concierto de la orquesta sinfónica de la ciudad."
recuerdo_2 = "Pasé la tarde leyendo un libro de historia."
recuerdo_3 = "Tuve que fregar los platos y sacar la basura de casa."

print("\nConvirtiendo texto a vectores matemáticos...")
# El modelo convierte las frases en listas de números densos (Embeddings)
vector_interes = modelo.encode(interes_agente)
vector_r1 = modelo.encode(recuerdo_1)
vector_r2 = modelo.encode(recuerdo_2)
vector_r3 = modelo.encode(recuerdo_3)

print("\nCalculando Similitud del Coseno...")
# Comparamos el interés con cada recuerdo (1.0 es idéntico, 0.0 es nulo)
similitud_1 = util.cos_sim(vector_interes, vector_r1).item()
similitud_2 = util.cos_sim(vector_interes, vector_r2).item()
similitud_3 = util.cos_sim(vector_interes, vector_r3).item()

print(f"\nTema Central: '{interes_agente}'")
print("-" * 60)
print(f"Recuerdo 1: '{recuerdo_1}'")
print(f"Puntuación de Relevancia: {similitud_1:.4f}\n")

print(f"Recuerdo 2: '{recuerdo_2}'")
print(f"Puntuación de Relevancia: {similitud_2:.4f}\n")

print(f"Recuerdo 3: '{recuerdo_3}'")
print(f"Puntuación de Relevancia: {similitud_3:.4f}")


print("\n--- PRUEBA DE VELOCIDAD REAL (MODELO YA CARGADO) ---")
inicio = time.time()

# Calculamos un recuerdo nuevo
nuevo_recuerdo = "He comprado unas entradas para la ópera de esta noche."
vector_nuevo = modelo.encode(nuevo_recuerdo)
similitud_nueva = util.cos_sim(vector_interes, vector_nuevo).item()

fin = time.time()
milisegundos = (fin - inicio) * 1000

print(f"Recuerdo: '{nuevo_recuerdo}'")
print(f"Puntuación: {similitud_nueva:.4f}")
print(f"Tiempo de procesamiento real: {milisegundos:.2f} milisegundos")