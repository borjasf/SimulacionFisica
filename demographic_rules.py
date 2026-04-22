# ARCHIVO: demographic_rules.py
# DESCRIPCIÓN: Modificadores estocásticos basados en Edad y Ocupación laboral.
# Actúan como filtros estructurales y pesos para las Cadenas de Markov.
#
# BASE CIENTÍFICA Y JUSTIFICACIÓN:
# 1. INE (Encuesta de Empleo del Tiempo): Define las curvas de carga doméstica 
#    y obligaciones formales (pico máximo en la franja 25-44 años).
# 2. Arnett (2007) - Teoría de la "Adultez Emergente": Justifica la franja 16-24 
#    con alta exploración social y digitalización, con baja asunción de roles adultos.
# 3. Baltes et al. (1999) - Teoría SOC (Selección, Optimización, Compensación): 
#    Justifica el repliegue de los >65 años hacia actividades de bajo coste 
#    energético (paseos, TV) y el aumento de gestiones personales diurnas (médicos).

AGE_RULES = {
    "16-": {
        # Menores de 16: Alta dependencia, nula carga burocrática
        "OBLIGACIONES": 1.2,           # Principalmente jornada escolar
        "TAREAS_DOMESTICAS": 0.5,
        "OCIO": 1.3,
        "ver_rrss": 2.0,
        "ocio_digital_activo": 2.5,
        "gestiones_personales": 0.1,   # No hacen trámites bancarios ni médicos solos
        "mantenimiento_del_hogar": 0.2
    },
    "16-24": {
        # Adultez Emergente (Arnett, 2007): Exploración y socialización
        "ocio_hosteleria": 1.8,
        "ver_rrss": 1.5,
        "ocio_digital_activo": 1.5,
        "gestiones_personales": 0.5    # Comienzan a asumir burocracia, pero baja
    },
    "25-44": {
        # Adultez Temprana: Pico de responsabilidades (Datos INE EET)
        "OBLIGACIONES": 1.3,
        "gestiones_personales": 1.2,
        "mantenimiento_del_hogar": 1.2,
        "ocio_hosteleria": 1.2
    },
    "45-64": {
        # Adultez Media: Consolidación y rutinas caseras
        "TAREAS_DOMESTICAS": 1.3,
        "mantenimiento_del_hogar": 1.5,
        "consumo_audiovisual": 1.5,
        "ver_rrss": 0.8,
        "ocio_digital_activo": 0.3     # Caída en adopción de ocio digital interactivo
    },
    "65+": {
        # Tercera Edad (Baltes et al., 1999 - Teoría SOC): Optimización de energía
        "OBLIGACIONES": 0.3,           # Desaparición de obligaciones formales
        "TAREAS_DOMESTICAS": 1.5,
        "OCIO": 1.4,
        "gestiones_personales": 1.5,   # Aumento de recados, médicos y compras diurnas
        "paseo_recreativo": 2.0,       # Actividad física compensatoria de bajo impacto
        "actividad_cultural": 1.5,
        "consumo_audiovisual": 2.0,
        "ver_rrss": 0.3,
        "ocio_digital_activo": 0.3
    }
}

def get_occupation_modifiers(occupation: str, age: int) -> dict:
    """
    Analiza la ocupación y edad del agente para generar ceros estructurales (0.0) 
    en las jornadas incompatibles, simplificando el modelo a reglas universales.
    """
    occ = str(occupation).strip().lower()
    mods = {}
    
    # 1. TERCERA EDAD (Jubilación por edad demográfica)
    if age >= 65:
        mods["jornada_laboral"] = 0.0
        mods["jornada_academica"] = 0.0
        mods["OBLIGACIONES"] = 0.3  
        return mods
        
    # 2. ESTUDIANTES
    if occ == "student":
        mods["jornada_laboral"] = 0.0
        return mods
        
    # 3. DESEMPLEADOS
    if occ == "unemployed":
        mods["jornada_laboral"] = 0.0
        mods["jornada_academica"] = 0.0
        mods["OBLIGACIONES"] = 0.4 
        return mods

    # 4. TRABAJADORES (Comportamiento por defecto)
    # Cubre el resto de casos de trabajadores en el csv.
    mods["jornada_academica"] = 0.0
    
    return mods