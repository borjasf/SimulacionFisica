# 📑 INFORME EXTENSO DE MEJORA DEL DOCUMENTO

## Tabla de Contenidos
- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Mejoras por Prioridad](#mejoras-por-prioridad)
- [Cambios Sección por Sección](#cambios-sección-por-sección)
- [Elementos Nuevos a Añadir](#elementos-nuevos-a-añadir)
- [Reorganización de Contenidos](#reorganización-de-contenidos)
- [Checklist de Implementación](#checklist-de-implementación)

---

## RESUMEN EJECUTIVO

Tu documento actual tiene **nota 6.5/10**. El problema principal no es contenido incorrecto, sino **presentación desorganizada** para audiencias mixtas (especialistas + principiantes).

**Tiempo estimado de implementación**: 8-12 horas
**Mejora esperada**: 8.5-9/10

### Los 3 cambios más impactantes:
1. Añadir una sección "Lectura Rápida" al inicio (30 min)
2. Reorganizar Capítulo 3 (flujo de ejecución primero) (2 horas)
3. Explicar cada concepto con ejemplo mundano ANTES de la formalización (4 horas)

---

## MEJORAS POR PRIORIDAD

### 🔴 PRIORIDAD 1: CRÍTICO - Haz esto primero

#### 1.1 Crear Sección "Lectura Rápida para No-Especialistas" (NUEVA)

**Ubicación**: ANTES del Capítulo 2 (después de la Introducción que aún escribirás)

**Propósito**: Proporcionar contexto sin tecnicismos para que cualquiera entienda el "por qué"

**Extensión**: 2 páginas

**Texto sugerido**:

```
═══════════════════════════════════════════════════════════════════
LECTURA RÁPIDA: SI NO ENTIENDE DE SIMULACIONES MULTI-AGENTE
═══════════════════════════════════════════════════════════════════

¿QUÉ PROBLEMA RESOLVEMOS?

Imagina que quieres simular cómo 100 personas se comportan en una ciudad.
Cada persona:
  - Tiene una casa, amigos, un trabajo
  - Se cansa, tiene hambre, necesita descansar
  - Prefiere hablar con gente similar a ellos
  - Explora nuevos lugares pero vuelven a los habituales

Problema: Si programas cada decisión manualmente, necesitarías millones
de líneas de código. Necesitas reglas SIMPLES que generen comportamiento
COMPLEJO.

¿CUÁL ES LA SOLUCIÓN? (3 "Leyes" que rigen la simulación)

LEY 1: La Ley del Espacio-Tiempo (Hägerstrand, 1970)
────────────────────────────────────────────────
"La gente no puede estar en dos lugares a la vez, ni teletransportarse."

En la simulación:
  → Moverse de A a B cuesta 1 turno
  → La distancia afecta: lugares cercanos son más probables
  → Esto crea "barrios" automáticamente (sin programarlos)

EJEMPLO REAL: Por qué conoces mejor tu ciudad que otra ciudad a 500 km.
             Los viajes lejanos cuestan tiempo, así que exploras menos lejos.

LEY 2: La Ley de la Supervivencia (Homeostasis)
────────────────────────────────────────────────
"Tu cuerpo necesita comer y dormir. Si ignoras esto, mueres."

En la simulación:
  → Los agentes tienen ENERGÍA (0-100) y SACIEDAD (0-100)
  → Trabajar cansa (energía -7), comer recupera saciedad (+100)
  → Cuando el cansancio es CRÍTICO, INTERRUMPE toda rutina
  → Esto genera patrones realistas: trabajo → almuerzo → más trabajo

EJEMPLO REAL: No te importa si tienes reunión: si tienes hambre crítica,
             IRÁS a comer primero. La simulación modela esto.

LEY 3: La Ley de la Afinidad (Homofilia, McPherson 2001)
─────────────────────────────────────────────────────────
"Te rodeas de gente similar: edad, intereses, profesión."

En la simulación:
  → Dos personas que se encuentran en un café tienen X% probabilidad
     de hablar (calculada por: edad similar? sí +1, mismo trabajo? +1, etc.)
  → Esta conversación usa IA (LLM) para generar diálogo realista
  → El diálogo cambia la "relación" entre ellos (amigos, conocidos, rivales)

EJEMPLO REAL: Tienes más amigos de tu universidad que desconocidos al azar.
             La edad y los intereses comunes actúan como "filtro social".

¿CÓMO ESTO GENERA COMPORTAMIENTO "INTELIGENTE"?

La magia: Aplicando estas 3 leyes simples, los agentes:
  ✓ Crean rutinas realistas (trabajo → comida → casa → descanso)
  ✓ Forman amistades naturales (sin programarlas)
  ✓ Exploran ciudades de forma realista (conocen el barrio, viajan lejos raro)
  ✓ Tienen conversaciones coherentes (el LLM)
  
NO programamos nada de esto. EMERGE de las reglas.

¿QUÉ TECNOLOGÍA USAMOS?

1. CADENAS DE MARKOV (Decisiones predecibles)
   → "Si estoy trabajando, después como, duermo o descanso"
   → Probabilidades basadas en datos de empleo del tiempo REALES (INE)

2. MODELOS MATEMÁTICOS (Movimiento espacial)
   → G-EPR: Fórmula de "gravedad urbana"
   → Cuanto más lejano, menos probable visitarlo

3. LLM (Google Gemini) - Inteligencia Artificial
   → Solo para diálogos entre personas
   → NO para decisiones rutinarias (demasiado lento)

4. PYTHON (Lenguaje de programación)
   → Eficiente, científico, usado en simulaciones

LECTURA: ¿QUÉ ESPERAR DE ESTE DOCUMENTO?

Capítulo 2 (Marco Teórico)
  → Explica cada "Ley" en profundidad con referencias científicas
  
Capítulo 3 (Arquitectura)
  → Muestra cómo las 3 leyes se traducen en módulos de código
  → Flujo de cómo "despierta" un agente cada turno
  
Capítulo 4 (Implementación)
  → Código específico: cómo calculamos cada valor
  → Fórmulas exactas y pseudocódigo
  
Capítulo 5 (Resultados)
  → Qué patrones emergentes aparecieron
  → ¿Las amistades fueron realistas? ¿Los movimientos?

═══════════════════════════════════════════════════════════════════
FIN DE LA LECTURA RÁPIDA - Ahora sí, comienza la aventura técnica
═══════════════════════════════════════════════════════════════════
```

**Beneficios**:
- Gente sin experiencia entiende el "para qué"
- Especialistas saltarán esto pero validan tu alcance
- Establece expectativas claras

---

#### 1.2 Añadir Tabla de Abreviaturas (NUEVA)

**Ubicación**: Después del Índice, antes del Capítulo 1

**Extensión**: 1-2 páginas

```markdown
# TABLA DE ABREVIATURAS Y TÉRMINOS CLAVE

| Acrónimo | Significado | Contexto |
|----------|------------|----------|
| ABM | Agent-Based Model / Modelo Basado en Agentes | Paradigma de simulación |
| DBO | Desires, Beliefs, Opportunities / Deseos, Creencias, Oportunidades | Marco teórico |
| G-EPR | Gravity-Exploration and Preferential Return | Motor espacial |
| LLM | Large Language Model / Modelo de Lenguaje Grande (IA) | Generación de diálogos |
| POI | Point of Interest / Punto de Interés | Ubicaciones en la ciudad |
| FSM | Finite State Machine / Máquina de Estados Finitos | Modelo de decisión |
| INE | Instituto Nacional de Estadística | Datos reales españoles |
| CSV | Comma-Separated Values / Archivo de datos | Formato de entrada/salida |
| JSON | JavaScript Object Notation / Formato de datos | Respuestas del LLM |
| API | Application Programming Interface | Interfaz de Gemini |

## CONCEPTOS RECURRENTES

### Macro-estado
Una de 5 categorías amplias de actividad:
- DESCANSO
- ALIMENTACIÓN
- OBLIGACIONES
- TAREAS_DOMÉSTICAS
- OCIO

### Micro-acción
La actividad específica dentro de un macro-estado

**Ejemplo**: OCIO contiene (paseo_recreativo, ocio_hosteleria, lectura, etc.)

### Tick/Turno
Una unidad de tiempo discreto en la simulación.

No mide segundos reales, es un "paso" de decisión.

### Homofilia
Tendencia a asociarse con gente similar (edad, ocupación, intereses)

### Fricción de la distancia
Cuanto más lejos, menos probable visitarlo (similar a gravedad: más distancia = menos atracción)

### Homeostasis
El cuerpo mantiene equilibrio (energía, temperatura, etc.)

En simulación: energía y saciedad tienden a 100 (punto de equilibrio)
```

**Beneficios**:
- Lectores pueden buscar qué significa cualquier acrónimo
- Reduce confusión cuando aparecen términos nuevos

---

#### 1.3 Revisar y Corregir Abreviaturas Incorrectas

**Problema encontrado**: 
En Capítulo 3, potencialmente usas **WSDL, JAXB, JAX-WS** que son términos de **servicios web SOAP** (COMPLETAMENTE FUERA DE TEMA). Estos provienen de tu memoria sobre un curso de Arquitectura del Software.

**Acción necesaria**:
- [ ] Buscar en el PDF dónde aparecen WSDL, JAXB, etc.
- [ ] ELIMINAR esas secciones o verificar que no están en el documento actual
- [ ] Confirmar que todo es específico a tu simulación

**Verificación**: Lee el PDF completo buscando términos web/SOAP. Si aparecen, bórralos inmediatamente.

---

### 🟡 PRIORIDAD 2: IMPORTANTE - Cambios de Estructura

#### 2.1 Reorganizar Capítulo 3: Arquitectura y Diseño del Sistema

**PROBLEMA ACTUAL**:
```
Página 9:   3. Arquitectura y Diseño del Sistema
Página 10:  3.1 Paradigma de Simulación
Página 13:  3.2 Arquitectura Híbrida y Modularidad
Página 14:  3.3 Entidades y Estructuras de Datos
Página 20:  3.4 Flujo General de Ejecución (El Bucle de Vida)  ← AQUÍ DEBE ESTAR PRIMERO
Página 24:  3.5 Selección Tecnológica
```

**PROBLEMA ESPECÍFICO**:
Hasta la página 20 no entiendes cómo se ejecuta todo. El "flujo" debería ser lo PRIMERO que entiendas, luego qué módulos lo implementan.

**SOLUCIÓN - NUEVO ORDEN**:
```
3. Arquitectura y Diseño del Sistema
  │
  ├─ 3.0 EL BUCLE DE VIDA: ¿Cómo "despierta" un agente cada turno? [NUEVO]
  │      (Pseudocódigo visual del flujo principal)
  │
  ├─ 3.1 Paradigma de Simulación 
  │      (Por qué asincronía, por qué ruleta ponderada)
  │
  ├─ 3.2 Arquitectura Híbrida y Modularidad
  │      (Los 2 pilares: Chasis Físico + Motor Cognitivo)
  │
  ├─ 3.3 Entidades y Estructuras de Datos
  │      (Qué información guarda cada agente)
  │
  ├─ 3.4 Selección Tecnológica
  │      (Por qué Python + Gemini + Markov)
  │
  └─ 3.5 Detalles de Implementación
         (Código específico, aunque esto es más para Cap. 4)
```

**Texto a crear para 3.0** (1 página):

```markdown
## 3.0 EL BUCLE DE VIDA: Cómo "Despierta" un Agente cada Turno

### VISIÓN GENERAL EN 30 SEGUNDOS

Cada turno (tick), UN agente es seleccionado mediante ruleta ponderada.
Ese agente atraviesa 6 etapas de decisión:

```
    TURNO N
       ↓
    [1] ¿Quién actúa?          → Ruleta: agentes activos primero
       ↓
    [2] ¿Qué necesito?         → Motor Biológico: ¿hambre? ¿cansancio?
       ↓
    [3] ¿Qué quiero hacer?     → Motor de Markov: rutina + personalidad
       ↓
    [4] ¿Dónde lo hago?        → Motor Espacial: elegir destino
       ↓
    [5] ¿Hablo con alguien?    → Motor Social: si está en mismo lugar
       ↓
    [6] Actualizar y guardar   → Memoria, estadísticas
       ↓
    TURNO N+1
```

ESTO NO SE PROGRAMA TODO JUNTO. Se divide en 4 MOTORES que actúan
secuencialmente. Los detalles técnicos están en el Capítulo 4.

### DIAGRAMA DE FLUJO FORMAL

[Incluir aquí el pseudocódigo de página 21, pero AHORA, no en página 20]

### ¿POR QUÉ ESTE ORDEN?

La secuencia está diseñada así porque:

1. **Primero: Biología** 
   - Si mueres de hambre, TODO lo demás es irrelevante

2. **Luego: Decisión rutinaria** 
   - ¿Qué prefieres hacer?

3. **Luego: Realidad física** 
   - ¿Dónde puedes hacerlo?

4. **Finalmente: Socialización** 
   - Solo si físicamente coincides

Esta es la "Ley de Prioridades" que hace la simulación realista.
```

**Beneficios**:
- Lector entiende PRIMERO el flujo general
- Luego le enseñas los detalles de cada motor
- Evita la sensación de "perderse en detalles sin contexto"

---

#### 2.2 Consolidar Repeticiones del Modelo DBO

**PROBLEMA**:
```
Página 4 (2.2.1):
"Para evitarlo, la arquitectura del proyecto sigue el modelo analítico 
DBO (Desires, Beliefs, Opportunities). La acción humana no es aleatoria..."

Página 9 (3.1.1):
"Para garantizar rigor sociológico a nivel microscópico, la arquitectura 
adopta el modelo analítico DBO (Desires, Beliefs, Opportunities), que 
afirma que las acciones humanas resultan de la combinación entre las 
creencias y las oportunidades del individuo."
```

Son casi idénticas. Solo se menciona una vez.

**SOLUCIÓN**:
En la **segunda aparición (p. 9)**, REEMPLAZAR por un párrafo de REFERENCIA:

```markdown
### ANTERIOR (página 9):
"Para garantizar rigor sociológico a nivel microscópico, la arquitectura 
adopta el modelo analítico DBO (Desires, Beliefs, Opportunities), que 
afirma que las acciones humanas resultan de la combinación entre las 
creencias y las oportunidades del individuo. La toma de decisiones del 
agente se divide en varios componentes que respetan ese modelo."

### NUEVO (página 9):
"Como se detalla en la Sección 2.2.1, la arquitectura adopta el modelo 
DBO (Desires, Beliefs, Opportunities). Aquí especificamos cómo se 
implementa en la práctica:

- El motor estocástico modela los DESEOS del agente
- La memoria (accion_buffer) representa sus CREENCIAS
- El motor espacial restringe según OPORTUNIDADES reales

Esta división garantiza comportamiento sociológicamente válido."
```

**Beneficios**:
- Se evita repetición textual
- Se refuerza la continuidad entre Teoría e Implementación
- Ahorra 4-5 líneas

---

## 🟠 PRIORIDAD 3: ALTO IMPACTO - Explicaciones

### 3.1 Pattern: "Mundano → Fórmula → Sistema"

**PROBLEMA GENERAL**:
Tu documento lanza fórmulas sin contexto. Un lector no entiende POR QUÉ cada fórmula.

**SOLUCIÓN**:
Restructura TODAS las explicaciones complejas así:

```
PASO 1: EJEMPLO MUNDANO (1-2 líneas)
  ↓
PASO 2: LA FÓRMULA
  ↓
PASO 3: POR QUÉ IMPORTA EN TU SISTEMA
```

#### Ejemplo 1: Fricción de la Distancia (Página 31)

```markdown
## ACTUAL (solo fórmula):

"La probabilidad de elegir un destino disminuye a medida que aumenta 
la distancia hacia el mismo, ya que en el mundo real desplazarse supone 
un coste y esfuerzo. En el código, esta distancia se mide de forma 
geométrica calculando la distancia Euclidiana entre las coordenadas 
actuales del agente y el destino mediante el teorema de Pitágoras."

## MEJORADO (mundano → fórmula → sistema):

"En la vida real, prefieres el café a 100 metros sobre el que está a 2 
km. La distancia CUESTA tiempo, dinero, energía.

En el código, medimos esto con la **distancia Euclidiana**:

    d_ij = √[(x_i - x_j)² + (y_i - y_j)²]

En la simulación, esto genera 'barrios naturales': los agentes frecuentan 
lugares cercanos y raramente viajan lejos. **SIN programar barrios.**"
```

#### Ejemplo 2: Multiplicador de Supervivencia (Página 30)

```markdown
## ACTUAL (vago):

"el sistema aplica un factor multiplicador de supervivencia 
(establecido en ×10 en el desarrollo) y suma de forma aditiva"

## MEJORADO (mundano → número → justificación):

"Imagina que estás trabajando pero tienes hambre crítica. Tu urgencia 
por comer compite con tu deber laboral. ¿Cuánto pesa la urgencia?

Si el hambre vale 0.5 en la escala, y multiplicamos por 10, se convierte 
en 5, que DOMINA la probabilidad de decisión. Así:

    Probabilidad(trabajo) = base + hambre_urgencia × 10
    
Si Markov dice 0.8 (80% trabajo), pero hambre × 10 = 5, entonces:

    0.8 + 5 = 5.8 → RENORMALIZADO → 85% de irte a comer

El ×10 fue calibrado empíricamente: 
- Con ×5, los agentes ignoraban hambre
- Con ×20, comían obsesivamente"
```

#### Ejemplo 3: k=3 (curva de estrés cúbica, Página 29)

```markdown
## ACTUAL (fórmula sin motivación):

"Se determinó un valor base de k = 3.0 (curva de estrés cúbica), una 
elección arquitectónica estratégica fundamentada en dos pilares 
fundamentales..."

## MEJORADO (gráfico conceptual + justificación):

"¿Por qué NO es lineal el cansancio?

**Con k=1 (lineal)**:
- Cansancio del 30% → Urgencia del 30%
- Resultado: Agente cansado todo el rato, interrumpe cada tarea

**Con k=3 (cúbica)**:
- Cansancio del 30% → Urgencia del 2.7%
- Cansancio del 80% → Urgencia del 51%

**Resultado**: Agentes IGNORAN cansancio leve (realista), pero COLAPSAN 
cuando es crítico. Esto genera patrones humanos: trabajas 5 horas, 
luego de repente 'poff', necesitas descansar."
```

**Dónde aplicar este pattern**:
- [ ] Página 26-30: Motor Biológico (curva de utilidad, exponentes)
- [ ] Página 31-32: Motor Espacial (G-EPR, β, ρ, γ)
- [ ] Página 38: Homofilia (tabla de puntuación)
- [ ] Página 29: Multiplicador ×10

---

### 3.2 Explicar Conceptos "Raros" Cuando Aparecen PRIMERO

**Problema**: Lanzas términos sin definir, luego los explicas tarde o nunca.

**Solución**: PRIMERA MENCIÓN = DEFINICIÓN CLARA

#### a) "Suficiencia Generativa" (Página 4)

```markdown
## ACTUAL:

"La arquitectura del proyecto sigue el modelo analítico DBO 
(Desires, Beliefs, Opportunities). La acción humana no es aleatoria: 
surge de la intersección de tres elementos:"

[Lee esto y aún no entiende QUÉ ES suficiencia generativa]

## MEJORADO:

"¿Cómo sabemos si un simulador es válido? Solo por reproducir datos 
globales NO es suficiente. Dos modelos completamente diferentes pueden 
dar los mismos resultados por casualidad (equivalencia funcional).

Por eso usamos **SUFICIENCIA GENERATIVA**: el modelo debe tener reglas 
MICROSCÓPICAS correctas que, combinadas, generen patrones MACROSCÓPICOS 
correctos. Es decir, no solo debe 'parecer realista', sino estar 
construido sobre leyes válidas.

Esto es donde entra el modelo DBO (Desires, Beliefs, Opportunities)..."
```

#### b) "Equivalencia Funcional" (Página 4)

```markdown
## ACTUAL:

"validar un simulador no puede limitarse a replicar datos a escala 
macroscópica. León-Medina (2017) advierte del riesgo de equivalencia 
funcional: modelos con reglas internas erróneas que arrojan resultados 
globales correctos por casualidad estadística."

[Brevísimo, sin ejemplos]

## MEJORADO:

"### ADVERTENCIA IMPORTANTE: Equivalencia Funcional

Dos simuladores pueden dar exactamente los MISMOS RESULTADOS pero por 
razones COMPLETAMENTE DIFERENTES.

**Ejemplo absurdo**:
- Simulador A: Cada agente decide con IA avanzada
- Simulador B: Random puro
- Ambos producen: 2.3 horas promedio de trabajo/día

¿Cuál es válido? **SOLO el A** (aunque ambos dan el mismo resultado). 
Esto es 'equivalencia funcional': resultados iguales, mecánicas diferentes.

Para evitarlo, validamos que nuestras REGLAS INTERNAS sean correctas 
(micro), no solo que los RESULTADOS sean realistas (macro)."
```

#### c) "Fricción de la Distancia" (Página 31)

```markdown
## ACTUAL:

"Para dar una solución física a este problema, el sistema se basa en 
el concepto de la Fricción de la distancia. Esta idea establece que la 
probabilidad de que un agente elija un destino disminuye a medida que 
aumenta la distancia hacia el mismo..."

[Te das cuenta a mitad del párrafo qué significa]

## MEJORADO:

"### Fricción de la Distancia

En urbanismo se habla de **FRICCIÓN DE LA DISTANCIA**: es la idea de 
que los humanos evitan viajes lejanos. No es que sea imposible, es que 
cuesta tiempo, dinero, energía.

En la simulación, esto significa:
- Café a 100 metros: 60% de probabilidad
- Café a 500 metros: 15% de probabilidad
- Café a 2 km: 1% de probabilidad

**Matemáticamente**, usamos la fórmula de gravedad urbana que trata 
la distancia como 'fricción':

    Atractivo_final = Atractivo_base / (distancia^β)

Cuanto mayor β (beta), más importa la distancia. En tu caso, β=2."
```

#### d) "JSON Mode" (Página 37)

```markdown
## ACTUAL:

"El soporte nativo para el formato estructurado (JSON Mode) obliga al 
modelo a devolver esquemas de datos estrictos. Como se detallará en el 
capítulo de implementación, esta configuración es clave para automatizar 
la extracción de las variables de diálogo e impacto relacional de manera 
determinista, garantizando la estabilidad del programa."

[¿Por qué JSON y no XML o texto libre?]

## MEJORADO:

"### ¿Por qué forzamos JSON Mode?

El LLM podría devolver un diálogo como texto libre:

```
'Me alegro de verte. ¿Cómo estuvo tu día? Yo estoy cansado.'
'Pues mira, ha sido largo. ¿Y el tuyo?'
```

**Problema**: ¿Cómo extraes programáticamente 'relación mejoró +2'? 
Tendrías que parsear lenguaje natural (imposible confiable).

**Solución**: Forzar JSON (formato de datos estructurado):

```json
{
  'dialogo': [
    'Me alegra verte...',
    'Pues mira...'
  ],
  'variacion_relacion': +2
}
```

Ahora es trivial extraer `variacion_relacion` con código Python:

```python
score = response['variacion_relacion']  # ← 1 línea
```

**BENEFICIO**: Automatización confiable sin procesamiento de lenguaje 
natural complicado. El LLM hace el trabajo difícil (diálogo), pero en 
formato que el código entiende perfectamente."
```

#### e) "Temperatura 0.0" (Página 37)

```markdown
## ACTUAL:

"La invocación técnica se realiza mediante peticiones estructuradas con 
una temperatura de 0.0 para forzar la consistencia en el comportamiento 
y las reacciones del agente"

[¿Por qué? ¿Qué pasa con otras temperaturas?]

## MEJORADO:

"### Temperatura del LLM: ¿Por qué 0.0?

Los LLMs generalmente tienen 'creatividad' (temperatura 0.7-1.0). Esto 
significa: misma pregunta → diferentes respuestas cada vez.

**Problema**: Si preguntas dos veces lo mismo al LLM, obtienes diálogos 
diferentes. Esto hace que los agentes sean INCONSISTENTES.

**Solución**: Temperatura 0.0 = modo determinista. Misma entrada → misma 
salida SIEMPRE. El agente es predecible y coherente.

**TRADE-OFF**:
- ✓ Consistencia (agente siempre responde igual a mismo contexto)
- ✗ Menos creatividad (menos variedad en diálogos)

Para una simulación, la CONSISTENCIA importa más que la sorpresa."
```

#### f) "Round Robin descartado" (Página 23)

```markdown
## ACTUAL:

"En las simulaciones multi-agente clásicas, la ejecución temporal suele 
resolverse mediante un planificador circular secuencial (Round Robin), 
donde cada individuo actúa rigurosamente uno detrás de otro."

[¿Por qué es malo? NO se explica]

## MEJORADO:

"### Por qué NO usamos Round Robin

En simulaciones simples, todos actúan en ORDEN:

    Agente 1 → Agente 2 → Agente 3 → Agente 1...

**Problema: SINCRONIZACIÓN ARTIFICIAL**

- A las 8:00 SIEMPRE actúa Agente 1 primero
- A las 8:01 SIEMPRE actúa Agente 2
- Resultado: Se forman patrones repetitivos NO realistas
- Ejemplo: Los agentes se encuentran SIEMPRE a la misma hora

**Solución: RULETA PONDERADA**

- Agentes activos socialmente → mayor probabilidad de actuar pronto
- Agentes sedentarios → actúan cuando les toca
- Resultado: Encuentros impredecibles, horarios variados (realista)

Así, aunque la simulación es determinista, PARECE aleatoria y natural."
```

#### g) "Action Buffer" (página 42)

```markdown
## ACTUAL:

"Este buffer registra secuencialmente las acciones físicas ejecutadas 
(ej. pasear, comer, trabajar) desde la última vez que el agente 
interactuó socialmente."

[¿Qué es "buffer"? ¿Dónde se almacena?]

## MEJORADO:

"### Action Buffer: Registro de lo que hiciste hoy

**ACTION_BUFFER** es una 'lista de recordatorios'.

**Ejemplo**:
```
action_buffer = [
    'trabajando (jornada_laboral)',
    'comí en oficina (ingesta_en_hogar)',
    'trabajé más (jornada_laboral)',
    'salí del trabajo (desplazamiento)'
]
```

**¿Para qué?** Cuando el agente se encuentra a otro, el LLM le pregunta 
'¿qué has hecho hoy?' y el action_buffer proporciona la respuesta:

> "Hoy llevo la mañana trabajando, comí algo rápido en la oficina 
> y luego volví a trabajar."

Esto es más realista que si el LLM debe INVENTAR qué hizo."
```

---

### 3.3 Explicar el "Por qué" antes del "Cómo"

#### a) "Estado IN_TRANSIT" (página 25)

```markdown
## ACTUAL:

"Si el agente debe moverse, el sistema aplica las restricciones de 
Hägerstrand, calcula el destino ideal mediante el modelo GEPR y la 
fórmula de gravedad, y bloquea al agente en un estado de tránsito"

[¿Qué significa "estado de tránsito"? ¿Por qué "bloquea"?]

## MEJORADO:

"### Estado IN_TRANSIT: ¿Qué pasa mientras viajas?

Si el agente debe moverse, ocurre esto:

```
TURNO N:  Agente decide 'quiero ir al café' → Estado = IN_TRANSIT
          [Gastar 1 turno caminando, NO hace nada]

TURNO N+1: Agente llega al café → Estado = OCIO (ahora en café)
```

'Bloquear' significa: **EN_TRANSIT previene que haga otras cosas mientras 
viaja**. No puede cambiar de idea a mitad del camino.

**¿POR QUÉ?** Porque no puede estar en dos lugares: si viaja de A a B, 
está entre A y B, no puede decidir 'me voy al bar' sin completar el 
viaje primero."
```

#### b) "Matriz de Transición" de Markov (página 26)

```markdown
## ACTUAL:

"La estructura de esta jerarquía se ilustra en la Tabla 4.2."

[Pero la tabla aparece INMEDIATAMENTE. ¿Qué es una "matriz de transición"?]

## MEJORADO:

"### Matriz de Transición: Las reglas de decisión

Una **MATRIZ DE TRANSICIÓN** es una tabla que dice: 'Si estoy en estado X, 
¿cuál es la probabilidad de ir a estado Y?'

**EJEMPLO SIMPLE**: Si estoy DESCANSANDO:
- 5% probabilidad → COMER (tengo hambre)
- 45% probabilidad → TRABAJAR
- 35% probabilidad → TAREAS DOMÉSTICAS
- 15% probabilidad → SEGUIR DESCANSANDO

Esto es lo que calcula la 'Cadena de Markov'.

Luego la **Tabla 4.2** muestra TODAS las probabilidades (5 estados × 5 estados)."
```

---

## 🔵 PRIORIDAD 4: PULIDO - Detalles de Redacción

### 4.1 Unificar Formato de Términos

**Problema**: Algunos términos aparecen en inglés, otros en español, inconsistencia.

```
ACTUAL:
  - "Macro-Estado" vs "macro_estado"
  - "Micro-Acciones" vs "micro_acciones"
  - "Big Five" vs "Cinco Grandes"
  - "Digital Twin" vs "Gemelo Digital"
```

**SOLUCIÓN - ESTÁNDAR PROPUESTO**:

```markdown
## INGLÉS PURO (términos científicos):
  - Big Five (término científico, no traducir)
  - Round Robin (arquitectura de sistemas)
  - Action Buffer (componente de código)
  - JSON Mode (especificación técnica)
  - LLM (sigla standard)

## ESPAÑOL PURO (en narrativa):
  - Macro-estado (coherencia con "micro-acción")
  - Punto de Interés (en lugar de POI)
  - Modelo de Gravedad (en lugar de "Gravity Model")
  - Gemelo Digital (en lugar de "Digital Twin")
  - Cadena de Markov (término científico traducido)

## CÓDIGO: Siempre en lowercase con guiones bajos
  - macro_state
  - micro_action
  - action_buffer
  - current_coords
```

**Hacer un pase BUSCAR Y REEMPLAZAR** en todo el documento:
- [ ] Reemplazar "macro_estado" → "macro-estado" (en texto narrativo)
- [ ] Reemplazar "Digital Twin" → "Gemelo Digital"
- [ ] Reemplazar "POI" → "Punto de Interés" (primera mención)

---

### 4.2 Mejorar Gráficos y Visualización

**Problema**: Muchas tablas, pero no hay visualizaciones conceptuales.

#### a) Diagrama de Flujo del "Bucle de Vida" (página 10)

```
    ┌─────────────────────────────┐
    │   INICIO TURNO N            │
    └──────────────┬──────────────┘
                   ↓
    ┌─────────────────────────────┐
    │ 1. SELECCIONAR AGENTE       │
    │    (Ruleta ponderada)       │
    └──────────────┬──────────────┘
                   ↓
    ┌─────────────────────────────┐
    │ 2. EVALUAR BIOLOGÍA         │
    │    (Hambre, cansancio)      │
    └──────────────┬──────────────┘
                   ↓
           ┌───────┴───────┐
           ↓               ↓
    ¿URGENCIA   NO: Uso Markov (qué quiero)
    CRÍTICA?           ↓
      SÍ:        ┌────────────────────┐
      ↓          │ 3. ELEGIR ACCIÓN   │
    ┌─────┐      │ (Macro + Micro)    │
    │COMER│      └────────┬───────────┘
    │o     │             ↓
    │DORMIR│     ┌──────────────────────┐
    └──────┘     │ 4. ELEGIR UBICACIÓN  │
               │ (Motor Espacial)    │
               └────────┬────────────┘
                        ↓
               ┌─────────────────────┐
               │ 5. ¿COINCIDENCIAS   │
               │ SOCIALES?           │
               │ (¿Otro agente aquí?)│
               └─┬─────────────────┬─┘
                 │ SÍ        NO   │
                 ↓               ↓
            ┌────────┐      ┌──────────┐
            │ LLM:   │      │ Terminar │
            │Diálogo │      │ turno    │
            └────────┘      └──────────┘
                 ↓
            ┌──────────────┐
            │ 6. GUARDAR  │
            │ Estado final│
            └──────┬───────┘
                   ↓
           ┌──────────────────┐
           │ FIN TURNO N      │
           │ TURNO N+1        │
           └──────────────────┘
```

#### b) Gráfico: Curva de Utilidad (k=1 vs k=3, página 29)

```
Utilidad (0-1)
     │
   1 │              ╱ k=3 (cúbica)
   0.8 │           ╱
     │          ╱
   0.6 │       ╱
     │      ╱
   0.4 │   ╱         ─────── k=1 (lineal)
     │  ╱  ╱
   0.2 │╱  ╱
     │ ╱
     └─────────────────────────
       0   20  40  60  80  100
          Déficit (%)

Observaciones:
  • k=1: Aumenta linealmente (80% déficit = 80% urgencia)
  • k=3: Baja inicialmente (80% déficit = 51% urgencia)
         Pero crece exponencialmente hacia el final
  • Implicación: Ignorar cansancio es posible al principio,
                pero inevitable cuando es crítico
```

#### c) Tabla de Homofilia: Distribución de Resultados (página 39)

```
HOMOFILIA SCORE (distribución en 1000 pares)
     │
Pares│  ┌────┐
(#)  │  │    │  ┌────┐
 100 │  │    │  │    │ ┌────┐
  80 │  │    │  │    │ │    │ ┌────┐
  60 │  │    │  │    │ │    │ │    │
  40 │  │    │  │    │ │    │ │    │
  20 │  │    │  │    │ │    │ │    │
   0 │──┴────┴──┴────┴─┴────┴─┴────┴─
     0   1    2    3    4    5    6
        PUNTUACIÓN DE HOMOFILIA

Interpretación:
  • Mayoría de pares: 1-3 puntos (compatibilidad moderada)
  • Pocos pares: 0 puntos (incompatibles)
  • Muy pocos: 5+ puntos (altamente compatibles)

Multiplicador 0.30 = 30% por punto → Media de interacción ~67%
```

---

## 📝 ELEMENTOS NUEVOS A AÑADIR

### Elemento 1: Tabla de Contenidos AMPLIADA (Índice mejorado)

**Ubicación**: Después de la portada, antes del Capítulo 1

```markdown
# ÍNDICE GENERAL

## LECTURA RÁPIDA
Para no-especialistas en 5 minutos

## TABLA DE ABREVIATURAS

## CAPÍTULO 1: INTRODUCCIÓN
[A ESCRIBIR]

## CAPÍTULO 2: MARCO TEÓRICO Y ESTADO DEL ARTE
### 2.1 Simulación de Ecosistemas Sociales
### 2.2 Fundamentos de Sociología Analítica y Movilidad
  - 2.2.1 Suficiencia Generativa y DBO
  - 2.2.2 Geografía del Tiempo de Hägerstrand
  - 2.2.3 Modelos de Gravedad y Movilidad Humana
### 2.3 Dimensiones Psicológicas y Fisiológicas
  - 2.3.1 Teoría de Utilidad y Homeostasis
  - 2.3.2 Modelo Big Five
  - 2.3.3 Ciclo Vital
### 2.4 Dinámicas Relacionales y Estructura Social
  - 2.4.1 Principio de Homofilia
  - 2.4.2 Intercambio Social
  - 2.4.3 Límites Cognitivos de la IA

## CAPÍTULO 3: ARQUITECTURA Y DISEÑO DEL SISTEMA
### 3.0 EL BUCLE DE VIDA: Cómo actúa un agente [NUEVO]
### 3.1 Paradigma de Simulación y Diseño Temporal
  - 3.1.1 Suficiencia Generativa y DBO
  - 3.1.2 Modelado Espacio-Temporal
  - 3.1.3 Asincronía y Ruleta Ponderada
### 3.2 Arquitectura Híbrida y Modularidad
  - 3.2.1 Chasis Físico y Matemático
  - 3.2.2 Motor Cognitivo
  - 3.2.3 Estructura de Módulos
### 3.3 Entidades y Estructuras de Datos
  - 3.3.1 Modelado del Agente
  - 3.3.2 Estructura del Entorno Urbano
### 3.4 Selección Tecnológica
  - 3.4.1 Lenguaje Base: Python
  - 3.4.2 IA: API de Gemini

## CAPÍTULO 4: IMPLEMENTACIÓN
### 4.1 Desarrollo del Chasis Físico
  - 4.1.1 Gestión de Estados: Markov
  - 4.1.2 Motor Biológico: Homeostasis
  - 4.1.3 Motor Espacial: Fricción y Gravedad
  - 4.1.4 Simultaneidad Física y Digital
### 4.2 Desarrollo del Motor Cognitivo
  - 4.2.1 Capa Psicológica: Big Five
  - 4.2.2 Capa Social: Homofilia
  - 4.2.3 Integración LLM: Diálogos
  - 4.2.4 Por qué NO usamos LLM para micro-acciones [NUEVO]
### 4.3 Control del Sistema y Trazabilidad
  - 4.3.1 Centralización Paramétrica
  - 4.3.2 Exportación de Resultados

## CAPÍTULO 5: EXPERIMENTACIÓN Y ANÁLISIS
[A ESCRIBIR]

## CAPÍTULO 6: CONCLUSIONES Y TRABAJO FUTURO
[A ESCRIBIR]

## REFERENCIAS BIBLIOGRÁFICAS

## APÉNDICES
### A. Estructura de archivos del proyecto
### B. Parámetros configurables (config.py)
### C. Formato de salida CSV
### D. Ejemplos de diálogos generados
```

---

### Elemento 2: Glosario Ampliado (después de las abreviaturas)

```markdown
# GLOSARIO DE TÉRMINOS

## A

### AGENTE (o ENTIDAD)
Representa una persona individual en la simulación. Tiene atributos 
demográficos, psicológicos y biológicos.

**Ejemplos**: Adam (22 años, transportista), Allie (33 años, psicóloga)

### AFINIDAD
Grado de compatibilidad o atracción entre dos agentes. Se calcula sumando 
puntos por edad similar, intereses comunes, etc. Determina probabilidad 
de que dos agentes se hablen.

### ATRACCIÓN (en contexto espacial)
Cuánto "interesante" es un lugar para un agente.

En fórmula: `Atractivo = 1 / (distancia^β)`

Lugares cercanos tienen mayor atracción.

## B

### BIG FIVE (Cinco Grandes)
Modelo psicológico con 5 dimensiones de personalidad:
- **Sociability** (Sociabilidad)
- **Friendliness** (Amabilidad)
- **Scrupulousness** (Escrupulosidad)
- **Neuroticism** (Neuroticismo)
- **Intellectual** (Intelecto)

Cada agente tiene puntuaciones en estas 5 dimensiones.

## C

### CADENA DE MARKOV
Modelo matemático donde el futuro depende SOLO del presente, no del pasado.

Fórmula: `P(estado_siguiente | estado_actual)`

Usamos: Para decidir qué hace el agente en base a lo que hace AHORA.

### CHASIS FÍSICO
Conjunto de motores "baratos" computacionalmente:
- Motor Estocástico
- Motor Biológico
- Motor Espacial

Procesan miles de decisiones sin usar IA.

## D

### DEFICIENCIA FISIOLÓGICA (o DÉFICIT)
Cuánto te alejas del equilibrio óptimo:
- `Deficit_energía = 100 - energía_actual`
- `Deficit_saciedad = 100 - saciedad_actual`

Mayor déficit = mayor urgencia de actuar.

### DESPLAZAMIENTO (o IN_TRANSIT)
Estado en el que el agente está viajando entre ubicaciones. Consume 1 turno 
completo. El agente no puede hacer nada más.

### DBO (Desires, Beliefs, Opportunities)
Marco teórico que dice: **Acción = Deseos + Creencias + Oportunidades**

Tu modelo implementa esto así:
- **Deseos**: Motor Markov (qué quiero)
- **Creencias**: Memory (qué sé del mundo)
- **Oportunidades**: Motor Espacial (qué puedo hacer aquí)

## E

### EQUIVALENCIA FUNCIONAL
Problema en simulación: dos modelos diferentes pueden dar exactamente 
los mismos resultados por casualidad estadística. Es peligroso porque 
no valida que las REGLAS INTERNAS sean correctas.

## F

### FRICCIÓN DE LA DISTANCIA
Principio: Los humanos evitan viajes lejanos.

Matemáticamente: `Probabilidad ∝ 1/distancia^β`

Resultado: Agentes naturalmente crean "barrios".

## G

### G-EPR (Gravity-Exploration and Preferential Return)
Modelo que combina dos fuerzas del movimiento humano:
- **Exploración**: Probabilidad de visitar lugar nuevo
- **Retorno Preferencial**: Probabilidad de volver a lugar conocido

En fórmula: `P_explore = ρ × S^(-γ)`

### GEMELO DIGITAL (Digital Twin)
Representación virtual de un agente real. Tu simulación es un "gemelo 
digital" de la red social original.

Hereda: nombre, edad, ocupación, personalidad, amistades.

## H

### HOMEOSTASIS
Tendencia del cuerpo a mantener equilibrio interno.

En simulación: Energía y Saciedad tienden a 100. Desviaciones generan 
"urgencia" de actuar.

### HOMOFILIA
Principio: "Los pájaros del mismo plumaje vuelan juntos"

Significado: Te rodeas de gente similar a ti.

En simulación: Calcula compatibilidad por: edad, ocupación, intereses, 
personalidad.

## J

### JSON MODE
Modo en el que forzas al LLM a devolver datos en formato JSON.

**Beneficio**: Código Python puede extraer datos automáticamente.

Sin esto: Tendrías que parsear lenguaje natural (muy complicado).

## L

### LLM (Large Language Model)
Modelo de inteligencia artificial que entiende y genera lenguaje.

Tu proyecto usa: **Google Gemini 2.5 Flash**

Lo usas para: Generar diálogos realistas entre agentes.

## M

### MACRO-ESTADO
Una de 5 categorías generales de actividad:
- DESCANSO
- ALIMENTACIÓN
- OBLIGACIONES
- TAREAS_DOMÉSTICAS
- OCIO

**Nivel 1** de decisión: "¿Qué categoría general?"

### MICRO-ACCIÓN
La actividad ESPECÍFICA dentro de un macro-estado.

**Ejemplos**:
- En OCIO: paseo_recreativo, ocio_hosteleria, lectura
- En OBLIGACIONES: jornada_laboral, jornada_academica, gestiones_personales

**Nivel 2** de decisión: "¿Qué actividad exacta?"

### MOTOR COGNITIVO
Conjunto de componentes "caros" computacionalmente:
- Motor Social
- Integración LLM
- Capa Psicológica

Genera comportamiento semántico complejo (diálogos, relaciones).

### MOTOR ESTOCÁSTICO
Motor que toma decisiones basadas en probabilidades.

Implementa: Cadena de Markov + Rasgos de Personalidad

**Resultado**: "¿Qué quiero hacer?"

### MOTOR BIOLÓGICO
Motor que gestiona necesidades fisiológicas (hambre, cansancio).

Implementa: Homeostasis + Curva de Utilidad exponencial

**Resultado**: "¿Qué NECESITO hacer ahora?"

### MOTOR SOCIAL
Motor que gestiona encuentros sociales.

Implementa: Homofilia + Cálculo de compatibilidad

**Resultado**: "¿Hablo con este agente?"

### MOTOR ESPACIAL
Motor que gestiona movimiento en la ciudad.

Implementa: G-EPR + Modelo de Gravedad + Fricción de distancia

**Resultado**: "¿Dónde voy?"

## O

### OPORTUNIDAD
Aquello que es físicamente realizable en el contexto actual. El motor 
espacial restringe qué es posible hacer AQUÍ.

## R

### RUTA PREFERENCIAL (Preferential Return)
Tendencia a volver a lugares conocidos en lugar de explorar nuevos.

Fórmula: Mayor probabilidad si el lugar ha sido visitado antes.

**Resultado**: Agentes desarrollan rutinas de lugares.

### RULETA PONDERADA (o RULETA ESTOCÁSTICA)
Mecanismo para seleccionar un elemento con probabilidades desiguales.

En tu caso: Elige qué agente actúa basado en su "actividad social"

Agentes activos → actúan más frecuentemente.

## S

### SETPOINT (Punto de Equilibrio)
El nivel óptimo de una variable fisiológica.

En simulación: 
- Setpoint de energía = 100
- Setpoint de saciedad = 100

Cuando actual < setpoint: deficit, genera urgencia.

### SUFICIENCIA GENERATIVA
Principio: Que un modelo sea válido no solo por reproducir datos, sino 
por tener REGLAS INTERNAS correctas.

**Opuesto**: Equivalencia funcional (mismo resultado, reglas diferentes).

## T

### TICK (o TURNO COMPUTACIONAL)
Unidad de tiempo discreto en la simulación.

No corresponde a segundos reales: es un "paso" de decisión.

Cada tick, UN agente es seleccionado y actúa.

### TRANSICIÓN
Cambio de un estado a otro en la Cadena de Markov.

**Ejemplo**: DESCANSO → ALIMENTACIÓN (ir de dormir a comer)

Tiene probabilidad asociada (30%, 15%, etc.)

## U

### UTILIDAD
Medida matemática de "cuánto quiero hacer esto" en este momento.

Fórmula: `Utilidad = (Déficit / 100)^k`

Mayor déficit → Mayor utilidad de actuar para resolver.
```

---

## 🔄 REORGANIZACIÓN DE CONTENIDOS

### Cambio 1: Reordenar Capítulo 3 (Arquitectura)

**ANTES (actual)**:
```
Página 9:   3.1 Paradigma de Simulación
Página 13:  3.2 Arquitectura Híbrida
Página 14:  3.3 Entidades y Estructuras de Datos
Página 20:  3.4 Flujo General de Ejecución  ← DEBERÍA SER 3.0
Página 24:  3.5 Selección Tecnológica
```

**DESPUÉS (propuesto)**:
```
Página 9:   3.0 EL BUCLE DE VIDA (NUEVO)
Página 12:  3.1 Paradigma de Simulación
Página 14:  3.2 Arquitectura Híbrida y Modularidad
Página 16:  3.3 Entidades y Estructuras de Datos
Página 19:  3.4 Selección Tecnológica
```

**Acción**: 
- [ ] Copiar sección 3.4 "Flujo General de Ejecución" 
- [ ] Convertirla en nueva sección 3.0
- [ ] Renumerar subsecciones
- [ ] Ajustar referencias cruzadas

---

### Cambio 2: Expandir Sección 2.2 (Teoría)

**ANTES**:
```
2.2.1 Suficiencia Generativa y DBO (1 página)
```

**DESPUÉS**:
```
2.2.1 Suficiencia Generativa y DBO (1.5 páginas)
  - Agregar ejemplo de "equivalencia funcional"
  - Explicar por qué DBO importa

2.2.2 Geografía del Tiempo de Hägerstrand (1.5 páginas)
  - Explicar PRIMERO sin términos técnicos
  - Luego formalizar 3 restricciones

2.2.3 Modelos de Gravedad y Movilidad (1.5 páginas)
  - Explicar PRIMERO el principio mundano
  - Luego fórmula G-EPR
  - Visualización: gráfico de atracción vs distancia
```

---

### Cambio 3: Nueva sección 4.2.4 (Inviabilidad del LLM para micro-acciones)

**Ubicación**: DESPUÉS de 4.2.3, ANTES de 4.3

**Propósito**: Explicar por qué NO usas LLM para cada turno

**Contenido**:

```markdown
## 4.2.4 Por qué NO usamos LLM para Micro-Acciones

Se consideró usar LLM para CADA decisión de turno:

> "¿Qué debería hacer el agente ahora?"

### Beneficios potenciales:
- ✓ Mayor flexibilidad
- ✓ Comportamiento más natural
- ✓ Menos dependencia de probabilidades estadísticas

### Problemas identificados:

#### 1. LATENCIA (tiempo de ejecución)

Para 1000 turnos × LLM:
- Llama 3.2 (1B): 65 segundos
- Qwen 2.5 (3B): 144 segundos
- Phi3: 233 segundos

**RESULTADO**: 1000 turnos → 2+ horas (inaceptable)

Comparación: Markov puro → 10 segundos

#### 2. PRECISIÓN

Benchmark con 8 escenarios de decisión:
- Llama 3.2: 5/8 aciertos (62%)
- Qwen 2.5 (3B): 5/8 aciertos (62%)
- Phi3: 2/8 aciertos (25%)

**RESULTADO**: Frecuentes decisiones irracionales

(Ejemplo: "Agente decide trabajar cuando está comatoso por hambre")

#### 3. COSTO ECONÓMICO

- LLM remoto (Gemini) → cuota limitada
- LLM local (Ollama) → requiere GPU potente

**RESULTADO**: No viable sin recursos significativos

### CONCLUSIÓN

Markov + Personalidad es SUFICIENTE para micro-acciones porque:
- 99% de decisiones son predecibles (trabajo → almuerzo, etc.)
- LLM es mejor para casos COMPLEJOS (diálogos sociales)

Por eso usamos **ARQUITECTURA HÍBRIDA**:
- **Markov**: Decisiones rutinarias (rápido, confiable)
- **LLM**: Solo diálogos sociales (lento, complejo)

**Nota**: Si tuvieras GPU potente, podrías investigar LLM local (Ollama)
para micro-acciones. Pero con recursos actuales, no es viable.
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### FASE 1: Preparación (1 hora)

- [ ] **Crear copia de seguridad** del PDF actual
- [ ] **Leer todo el documento** linealmente (validar que no tenga secciones SOAP/WSDL)
- [ ] **Crear tabla de todas las fórmulas** en el documento (para verificar cada una)
- [ ] **Listar todas las figuras/tablas** (verificar que la numeración es coherente)

### FASE 2: Nuevas Secciones (3 horas)

- [ ] **Crear "Lectura Rápida"** (2 páginas) ANTES del Capítulo 2
- [ ] **Crear "Tabla de Abreviaturas"** (1 página) después del índice
- [ ] **Crear "Glosario"** (2-3 páginas) después de abreviaturas
- [ ] **Crear nueva sección 3.0** "El Bucle de Vida" con diagrama visual
- [ ] **Crear nueva sección 4.2.4** "Por qué no usamos LLM para micro-acciones"

### FASE 3: Explicaciones Mundanas (4 horas)

Para CADA sección de Capítulo 4, aplicar patrón "Mundano → Fórmula → Sistema":

#### Motor Biológico (Página 26-30)
- [ ] Ejemplo mundano del cansancio
- [ ] Fórmula de utilidad
- [ ] Por qué k=3 en tu sistema
- [ ] Comparación gráfica: k=1 vs k=3

#### Motor Espacial (Página 31-32)
- [ ] Ejemplo mundano de fricción de distancia
- [ ] Fórmula de gravedad urbana
- [ ] Importancia en tu simulación
- [ ] Gráfico: Atracción vs Distancia

#### Homofilia (Página 37-40)
- [ ] Ejemplo mundano de por qué prefieres gente similar
- [ ] Tabla de puntuación
- [ ] Monte Carlo distribution
- [ ] Por qué multiplicador 0.30

#### Multiplicador ×10 (Página 29-30)
- [ ] Explicar lógica (hambre crítica × 10 → interrumpe trabajo)
- [ ] Cómo se calibró empíricamente

### FASE 4: Conceptos Raros Explicados (3 horas)

- [ ] **"Suficiencia Generativa"**: Añadir en página 4 (antes de DBO)
  - Definición de qué es
  - Contraposición con equivalencia funcional
  
- [ ] **"Fricción de la Distancia"**: Añadir ejemplo en página 31
  
- [ ] **"JSON Mode"**: Añadir por qué en página 37 (no qué)
  
- [ ] **"Temperatura 0.0"**: Añadir trade-off en página 37
  
- [ ] **"IN_TRANSIT"**: Definir claramente página 25
  
- [ ] **"Action Buffer"**: Definir con ejemplo página 42
  
- [ ] **"Matriz de Transición"**: Explicar ANTES de tabla 4.2

### FASE 5: Consolidaciones (2 horas)

- [ ] **Eliminar repetición de DBO** (página 9, referencias a página 4)
- [ ] **Eliminar Round Robin sin explicación** (página 23, reescribir con "por qué es malo")
- [ ] **Consolidar explicaciones** Round Robin vs Ponderada en una ubicación

### FASE 6: Visualizaciones (2 horas)

- [ ] **Crear diagrama visual del Bucle de Vida** (ASCII o vector)
- [ ] **Crear gráfico: Curva de utilidad k=1 vs k=3**
- [ ] **Crear gráfico: Atracción vs Distancia**
- [ ] **Crear gráfico: Distribución Monte Carlo de homofilia**

### FASE 7: Unificación de Términos (1 hora)

- [ ] **Buscar y reemplazar inconsistencias**:
  - macro_estado → macro-estado (texto)
  - Digital Twin → Gemelo Digital
  - POI → Punto de Interés (primera mención)
  
- [ ] **Verificar consistencia de código**:
  - Siempre lowercase_with_underscores
  - Nunca camelCase en JSON/Python examples

### FASE 8: Verificación Final (1 hora)

- [ ] **Leer el índice**: ¿Tiene sentido el orden?
- [ ] **Leer el resumen ejecutivo**: ¿Se entiende en 5 minutos?
- [ ] **Buscar "ver página..."**: ¿Todas las referencias cruzadas son correctas?
- [ ] **Buscar "como se mencionó"**: ¿No hay confusión de dónde se menciona?
- [ ] **Verificar numeración**: Tablas 4.1-4.7, figuras, ecuaciones
- [ ] **Check de ortografía y gramática**

---

## 📊 RESUMEN DE CAMBIOS POR IMPACTO

| Cambio | Ubicación | Esfuerzo | Impacto | Prioridad |
|--------|-----------|----------|---------|-----------|
| Lectura Rápida | Inicio | 1 hora | ⭐⭐⭐ Alto | 🔴 P1 |
| Tabla Abreviaturas | Inicio | 30 min | ⭐⭐ Medio | 🔴 P1 |
| Glosario | Inicio | 1.5 horas | ⭐⭐⭐ Alto | 🔴 P1 |
| Reorganizar 3.0 | p. 9-20 | 1.5 horas | ⭐⭐⭐ Alto | 🟡 P2 |
| Motor Biológico explicado | p. 26-30 | 1 hora | ⭐⭐ Medio | 🟡 P2 |
| Motor Espacial explicado | p. 31-32 | 1 hora | ⭐⭐ Medio | 🟡 P2 |
| Homofilia explicada | p. 38-40 | 1.5 horas | ⭐⭐ Medio | 🟡 P2 |
| Visualizaciones | Varios | 2 horas | ⭐⭐ Medio | 🟠 P3 |
| Consolidar repeticiones | p. 4 y 9 | 30 min | ⭐ Bajo | 🔵 P4 |
| Unificar términos | Todo | 1 hora | ⭐ Bajo | 🔵 P4 |

**Tiempo total estimado**: 10-12 horas

---

## 🎯 ORDEN RECOMENDADO DE TRABAJO

### Semana 1:
1. Backup del PDF
2. Crear Lectura Rápida (sesión 2 horas)
3. Crear Tabla Abreviaturas (sesión 1 hora)
4. Crear Glosario (sesión 2 horas)

### Semana 2:
5. Reorganizar Capítulo 3 (sesión 3 horas)
6. Reescribir explicaciones Motor Biológico (sesión 1.5 horas)
7. Reescribir explicaciones Motor Espacial (sesión 1 hora)

### Semana 3:
8. Reescribir explicaciones Homofilia (sesión 1.5 horas)
9. Crear visualizaciones (sesión 2 horas)
10. Consolidar repeticiones y revisar (sesión 1.5 horas)
11. Correcciones finales y ortografía (sesión 1 hora)

---

## 📌 NOTAS FINALES

Este documento recoge **todas las sugerencias, cambios y mejoras** de manera 
detallada y paso a paso. Cada sección incluye:

- ✅ Ejemplo de texto ACTUAL
- ✅ Ejemplo de texto MEJORADO
- ✅ Razonamiento CLARO de por qué el cambio
- ✅ Checklist específico de QUÉS hacer
- ✅ Priorización y cronograma de trabajo

**¿Siguiente paso?**

Elige cualquier sección y comienza. Recomendación: empieza por la FASE 1 
(Lectura Rápida) porque es la más impactante y generas valor rápido.

Si necesitas ayuda implementando cualquier cambio específico, solo dímelo.

---

**Documento generado**: 9 de junio de 2026  
**Estado**: Listo para implementación  
**Versión**: 1.0
