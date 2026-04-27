# Modificadores de actividad por edad, basados en Encuesta de Empleo del Tiempo (INE)
# Actúan como filtros estructurales y ajustes a probabilidades de Markov

AGE_RULES = {
    "16-": {
        # Menores de 16: Alta escolaridad, baja responsabilidad adulta
        "OBLIGACIONES": 1.2,           # Principalmente jornada escolar
        "TAREAS_DOMESTICAS": 0.5,
        "OCIO": 1.3,
        "ver_rrss": 2.0,
        "ocio_digital_activo": 2.5,
        "gestiones_personales": 0.1,   # Sin responsabilidades administrativas
        "mantenimiento_del_hogar": 0.2
    },
    "16-24": {
        # Adultez emergente: Exploración social y digital elevada
        "ocio_hosteleria": 1.8,
        "ver_rrss": 1.5,
        "ocio_digital_activo": 1.5,
        "gestiones_personales": 0.5    # Comienzan autonomía administrativa
    },
    "25-44": {
        # Pico de responsabilidades: Trabajo, hogar y cuidados
        "OBLIGACIONES": 1.3,
        "gestiones_personales": 1.2,
        "mantenimiento_del_hogar": 1.2,
        "ocio_hosteleria": 1.2
    },
    "45-64": {
        # Consolidación en rutinas: Mayor peso a tareas domésticas
        "TAREAS_DOMESTICAS": 1.3,
        "mantenimiento_del_hogar": 1.5,
        "consumo_audiovisual": 1.5,
        "ver_rrss": 0.8,
        "ocio_digital_activo": 0.3     # Reducción en ocio digital interactivo
    },
    "65+": {
        # Tercera edad: Optimización de energía, mayor ocio y gestiones médicas
        "OBLIGACIONES": 0.3,           # Sin obligaciones laborales
        "TAREAS_DOMESTICAS": 1.5,
        "OCIO": 1.4,
        "gestiones_personales": 1.5,   # Citas médicas, trámites, compras
        "paseo_recreativo": 2.0,       # Actividad física de bajo impacto
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