# Simulación de un entorno físico basado en redes sociales sintéticas

Trabajo Fin de Grado (Ingeniería Informática, Universidad de Murcia) — Borja Sancho Fernández.
Tutores: Alejandro Buitrago López y Jose Antonio Ruipérez Valiente.

Este repositorio contiene el **chasis físico y el motor cognitivo** que dan cuerpo material a la red social sintética generada en el proyecto previo [`Synthetic generation of online social networks through homophily`](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11441429). Toda la fundamentación teórica, las fórmulas, las pruebas de rendimiento y la auditoría de resultados están documentadas en detalle en la memoria del TFG; este README solo pretende orientar a quien quiera ejecutar o navegar el código.

## Idea central

Los agentes generativos puros (estilo *Generative Agents* de Stanford) delegan **cada** decisión cotidiana a un LLM, lo que los vuelve inviables a escala urbana. Este proyecto invierte la prioridad: un **núcleo matemático determinista** (Cadenas de Markov, teoría de la utilidad homeostática, modelo de gravedad G-EPR) gobierna la rutina, la biología y el movimiento en milisegundos, y el LLM (Gemini 2.5 Flash) solo se invoca cuando dos agentes coinciden físicamente y superan un filtro de homofilia. Resultado medido: 50.000 turnos del chasis físico en ~5 segundos frente a las +42 horas que exigiría delegarlo todo al LLM.

## Estructura del repositorio

| Archivo | Rol |
|---|---|
| `main.py` | Orquestador principal. Bucle de eventos discretos: selecciona agente, actualiza biología, decide rutina, resuelve espacio, dispara lo social, exporta resultados. |
| `config.py` | Panel de control con todas las constantes del modelo (ver más abajo). |
| `agent.py` | Clase `Agent`: estado fisiológico, memoria, modificadores de personalidad, amigos, ubicación. |
| `agent_ingestor.py` | Carga `users.csv` y `friendships.csv`, instancia agentes y reconstruye amistades reciprocas. |
| `environment.py` | Mapa urbano 100×100, catálogo de Puntos de Interés, asignación de hogares y dibujo del mapa 2D final (`matplotlib`). |
| `biological_engine.py` | Desgaste de energía/saciedad y cálculo de la utilidad de intercepción homeostática (curva `(déficit/100)^k`). |
| `markov_engine.py` | Cadena de Markov jerárquica (macro-estados → micro-acciones) calibrada con la Encuesta de Empleo del Tiempo (INE) y la subrutina de "scroll" en redes sociales. |
| `trait_rules.py` | Traduce los rasgos Big Five en multiplicadores matemáticos (Markov, desgaste, exploración, fricción). |
| `demographic_rules.py` | Ceros estructurales y sesgos según ciclo vital (Adultez Emergente, modelo SOC en mayores). |
| `spatial_engine.py` | Algoritmo G-EPR (exploración vs. retorno preferencial) + modelo de gravedad para elegir destino exacto. |
| `homophily_rules.py` | Sistema aditivo de puntuación de homofilia (edad, ocupación, intereses, Big Five) y su conversión a probabilidad de interacción. |
| `social_engine.py` | Filtro de colisión espacial + homofilia; orquesta la llamada al motor cognitivo cuando procede. |
| `llm_client.py` | Cliente de Gemini 2.5 Flash: síntesis de memoria a largo plazo, generación de diálogo + *Profit score* (Homans), y fallback local vía Ollama para el modo `DECISION_ENGINE = "LLM"`. |
| `data_exporter.py` | Exporta las métricas finales (versión absoluta V1 y versión pura V2) a `resultados_tfg/*.csv`. |
| `users.csv` / `friendships.csv` | Población y grafo social de partida, heredados del simulador virtual. |

## Requisitos

No hay `requirements.txt` en el repo; las dependencias externas usadas en el código son:

```bash
pip install python-dotenv google-genai requests matplotlib
```

(El resto se apoya en librerías estándar de Python: `csv`, `random`, `math`, `ast`, `time`.)

Además, para usar el motor cognitivo real (no simulado) necesitas un archivo `.env` en la raíz con tu clave de Gemini:

```
GEMINI_API_KEY=tu_clave_aqui
```

Si `config.MOCK_LLM = True`, el sistema nunca llama a la API y usa respuestas neutras de relleno (útil para pruebas de rendimiento del chasis físico sin gastar cuota).

## Ejecución

```bash
python main.py
```

No hay más comandos ni flags: todo el comportamiento se controla editando `config.py` antes de lanzar. La simulación corre en bucle hasta `MAX_TURNS` (o indefinidamente si es `0`, deteniéndola con `Ctrl+C`). Al finalizar (por límite de turnos, interrupción manual o excepción) se imprime en consola un informe con:

- distribución de macro-estados y micro-acciones,
- porcentaje de tiempo en tránsito vs. permanencia,
- métricas de la red social emergente (grados, hubs, histograma),
- lugares más visitados,

y a continuación se exportan los CSV a `resultados_tfg/` y se abre una ventana con el mapa 2D de la ciudad (viviendas, POIs y la ruta del agente más activo marcada en dorado).

## `config.py`: parámetros que de verdad importan

`config.py` es el único punto que hay que tocar para experimentar. Los bloques más relevantes:

- **Reproducibilidad y duración**: `RANDOM_SEED` (semilla fija para resultados auditables), `MAX_TURNS` (0 = sin límite).
- **Motor de decisión**: `DECISION_ENGINE = "MARKOV"` (rápido, recomendado) o `"LLM"` (delega también la micro-acción a un modelo local vía Ollama; solo tiene sentido para los benchmarks de viabilidad descritos en la memoria).
- **`MOCK_LLM`**: si es `True`, ninguna llamada llega a Gemini; ideal para medir la velocidad pura del chasis físico o para desarrollar sin gastar cuota.
- **`PRINT_LOGS`**: con `False` se desactiva toda impresión por turno, maximizando los turnos/segundo.
- **Biología**: `BASE_URGENCY_K` (exponente de la curva de utilidad homeostática), tasas de desgaste/recuperación de energía y saciedad (`ENERGY_DECAY_*`, `SATIETY_DECAY_*`, `*_RECOVERY_*`).
- **Espacial (G-EPR)**: `BASE_EXPLORATION_RHO`, `BASE_GAMMA` (decaimiento del impulso explorador) y `BASE_SPATIAL_BETA` (fricción de la distancia en el modelo de gravedad).
- **Social**: `HOMOPHILY_PROB_MULTIPLIER` (puntos de homofilia → probabilidad de interacción), `FRIEND_INTERACTION_PROB`, `FRIENDSHIP_THRESHOLD_GAIN/LOSS` (umbrales de creación/ruptura de amistad).
- **Mapas de laboratorio**: `USE_LAB_MAP` y `USE_PETRI_MAP` sustituyen el mapa urbano normal por escenarios controlados (POIs a distancias fijas, o todos los agentes forzados a la misma celda) usados para aislar variables en la validación experimental.
- **Laboratorio psicológico**: `OVERRIDE_TRAIT` (fuerza un único rasgo Big Five a toda la población, p. ej. `"Neuroticism +"`) y `FORCE_URGENCY_K` (fuerza un `k` global ignorando el de cada agente), ambos pensados para las pruebas de sensibilidad psicológica del Capítulo 5.

## Documentación completa

Toda la justificación teórica (estado del arte, modelos sociológicos/psicológicos/geográficos), las fórmulas exactas, los prompts del LLM y los resultados experimentales están en la memoria del TFG (`TFG-BorjaSanchoFernandez.pdf`), que es la referencia autorizada por encima de este README.
