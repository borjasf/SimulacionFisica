# Modificadores poblacionales para las Cadenas de Markov
# basados en la Franja de Edad y la Ocupación laboral del agente.

AGE_RULES = {
    "16-": {
        # Menores de 16: Poco peso burocrático, mucho ocio pasivo/digital
        "OBLIGACIONES": 1.2,
        "TAREAS_DOMESTICAS": 0.5,
        "OCIO": 1.3,
        "ver_rrss": 2.0,
        "ocio_digital_activo": 2.5,
        "gestiones_personales": 0.1,
        "mantenimiento_del_hogar": 0.2
    },
    "16-24": {
        # Jóvenes adultos: Alta socialización y digitalización
        "ocio_hosteleria": 1.8,
        "ver_rrss": 1.5,
        "ocio_digital_activo": 1.5,
        "gestiones_personales": 0.5
    },
    "25-44": {
        # Adultos jóvenes: Pico de responsabilidades y carga doméstica
        "OBLIGACIONES": 1.3,
        "gestiones_personales": 1.2,
        "mantenimiento_del_hogar": 1.2,
        "ocio_hosteleria": 1.2
    },
    "45-64": {
        # Adultos maduros: Rutinas más caseras
        "TAREAS_DOMESTICAS": 1.3,
        "mantenimiento_del_hogar": 1.5,
        "consumo_audiovisual": 1.5,
        "ver_rrss": 0.8,
        "ocio_digital_activo": 0.3
    },
    "65+": {
        # Jubilados: Desaparición de obligaciones formales, ocio tranquilo
        "OBLIGACIONES": 0.3,
        "TAREAS_DOMESTICAS": 1.5,
        "OCIO": 1.4,
        "gestiones_personales": 1.5, # Médico, bancos, recados...
        "paseo_recreativo": 2.0,
        "actividad_cultural": 1.5,
        "consumo_audiovisual": 2.0,
        "ver_rrss": 0.3,
        "ocio_digital_activo": 0.3
    }
}

def get_occupation_modifiers(occupation, age):
    """
    Analiza la ocupación del agente (y su edad) para anular las acciones 
    incompatibles multiplicándolas por 0.0, y ajustando el peso de los macro-estados.
    """
    occ = str(occupation).strip().lower()
    mods = {}
    
    # 1. JUBILADOS (O mayores de 65 por defecto)
    if age >= 65 or occ in ["jubilado", "retired", "pensionista"]:
        mods["jornada_laboral"] = 0.0
        mods["jornada_academica"] = 0.0
        mods["OBLIGACIONES"] = 0.3  # Bajan drásticamente sus obligaciones
        mods["TAREAS_DOMESTICAS"] = 1.5
        mods["OCIO"] = 1.5
        return mods
        
    # 2. ESTUDIANTES
    if occ in ["estudiante", "student", "alumno"]:
        mods["jornada_laboral"] = 0.0
        return mods
        
    # 3. DESEMPLEADOS
    if occ in ["unemployed", "desempleado", "parado", "ninguna", "none"]:
        mods["jornada_laboral"] = 0.0
        mods["jornada_academica"] = 0.0
        mods["OBLIGACIONES"] = 0.4 # Solo les quedan las gestiones personales
        mods["TAREAS_DOMESTICAS"] = 1.5
        mods["OCIO"] = 1.5
        return mods
        
    # 4. TRABAJADORES (Comportamiento por defecto para el resto)
    mods["jornada_academica"] = 0.0
    return mods