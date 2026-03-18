# ==============================================================================
# ARCHIVO: trait_rules.py
# DESCRIPCIÓN: Traducción matemática de los 5 Grandes Rasgos de Personalidad 
# basados en los 100 clústeres de Goldberg (1990, Tabla 3).
# ==============================================================================

GOLDBERG_RULES = {
    "Sociability": {
        "+": {
            # GOLDBERG (+): Clúster 1 (Gregarismo), Clúster 2 (Nivel de energía)
            # Justificación: Buscan el contacto social y la actividad fuera de casa.
            "markov_weight_modifiers": {
                "OCIO_SOCIAL_SITIO": 1.4,       # Un 40% más de probabilidad de ir a sitios sociales
                "OCIO_SOCIAL_CONVERSAR": 1.5,   # Altísima propensión a iniciar conversaciones
                "INACTIVO_RELAX": 0.7,          # Evitan quedarse en casa sin hacer nada
                "OCIO_INDIVIDUAL": 1.2          # Mayor energía para salir al parque/deporte
            },
            "exploration_rho_bonus": 0.15,      # Más propensos a descubrir locales nuevos
            "homophily_base_bonus": 10          # Facilitadores sociales (conectan grupos)
        },
        "-": {
            # GOLDBERG (-): Clúster 10 (Aislamiento), Clúster 11 (Silencio), Clúster 16 (Pasividad)
            # Justificación: Prefieren entornos controlados, solitarios o digitales.
            "markov_weight_modifiers": {
                "OCIO_SOCIAL_SITIO": 0.6,       # Penalización fuerte a salir de bares/discotecas
                "OCIO_SOCIAL_CONVERSAR": 0.5,   # Hablan mucho menos aunque estén en el sitio
                "INACTIVO_RELAX": 1.3,          # Refugio principal (Aislamiento)
                "USANDO_RRSS": 1.3              # Alternativa pasiva de socialización
            },
            "exploration_rho_bonus": -0.15      # Prefieren ir a los pocos sitios que ya conocen
        }
    },
    
    "Amiability": {
        "+": {
            # GOLDBERG (+): Clúster 18 (Cooperación), Clúster 20 (Empatía), Clúster 27 (Calidez)
            # Justificación: Individuos que fomentan relaciones largas y estables.
            "markov_weight_modifiers": {
                "OCIO_SOCIAL_CONVERSAR": 1.3    # Tienden a alargar las interacciones verbales
            },
            "homophily_base_bonus": 15          # Caen bien, su umbral para entablar amistad es menor
        },
        "-": {
            # GOLDBERG (-): Clúster 30 (Beligerancia), Clúster 36 (Irritabilidad), Clúster 38 (Cinismo)
            # Justificación: Individuos competitivos o ariscos, cortan rápido las interacciones.
            "markov_weight_modifiers": {
                "OCIO_SOCIAL_CONVERSAR": 0.7    # Cortan la charla rápido para seguir a lo suyo
            },
            "homophily_base_bonus": -10         # Más exigentes a la hora de considerar a alguien amigo
        }
    },
    
    "Conscientiousness": {
        "+": {
            # GOLDBERG (+): Clúster 40 (Organización), Clúster 41 (Eficiencia), Clúster 46 (Puntualidad)
            # Justificación: Altamente rutinarios y enfocados en sus obligaciones y el orden.
            "markov_weight_modifiers": {
                "TRABAJAR_ESTUDIAR": 1.3,       # Alta adherencia a sus obligaciones
                "INACTIVO_TAREAS_CASA": 1.6,    # El rasgo definitorio para este estado (Organización)
                "USANDO_RRSS": 0.7,             # No pierden el tiempo (Eficiencia)
                "INACTIVO_RELAX": 0.8           # Menos propensos a holgazanear
            },
            "spatial_beta_modifier": 1.3        # Rutas eficientes: penalizan mucho la distancia irrazonable
        },
        "-": {
            # GOLDBERG (-): Clúster 52 (Desorganización), Clúster 58 (Pereza), Clúster 55 (Olvido)
            # Justificación: Tendencia a procrastinar y descuidar las tareas de mantenimiento.
            "markov_weight_modifiers": {
                "TRABAJAR_ESTUDIAR": 0.8,       # Mayor absentismo o escapes de su obligación
                "INACTIVO_TAREAS_CASA": 0.4,    # Rechazo a las tareas de orden/limpieza (Pereza)
                "INACTIVO_RELAX": 1.4,          # Alta tendencia a la procrastinación
                "USANDO_RRSS": 1.4              # Principal fuente de evasión
            },
            "spatial_beta_modifier": 0.8        # Rutas caóticas o ineficientes
        }
    },
    
    "Neuroticism": {
        "+": {
            # GOLDBERG (+): Clúster 65 (Ansiedad), Clúster 66 (Inestabilidad), Clúster 67 (Emocionalidad)
            # Justificación: Menor tolerancia al estrés, buscan evasión rápida constante.
            "biological_urgency_k": 2.5,        # La curva de necesidad física se dispara MUCHO antes
            "energy_decay_multiplier": 1.2,     # Se agotan emocional y físicamente más rápido
            "markov_weight_modifiers": {
                "USANDO_RRSS": 1.5,             # Consumo compulsivo como mecanismo de control de ansiedad
                "INACTIVO_RELAX": 1.2,          # Necesidad de aislamiento para recuperar estabilidad
                "TRABAJAR_ESTUDIAR": 0.8        # Dificultad para sostener la atención continua
            }
        },
        "-": {
            # GOLDBERG (-): Clúster 62 (Placidez), Clúster 63 (Independencia) [Polo opuesto: Estabilidad]
            # Justificación: Resiliencia física y mental, rutinas estoicas sin sobresaltos.
            "biological_urgency_k": 3.5,        # Aguantan el hambre y el cansancio sin alterar su rutina
            "energy_decay_multiplier": 0.8,     # Resistentes al desgaste
            "markov_weight_modifiers": {
                "USANDO_RRSS": 0.8              # Menor necesidad de evasión digital
            }
        }
    },
    
    "Openness": {
        "+": {
            # GOLDBERG (+): Clúster 75 (Creatividad), Clúster 76 (Curiosidad), Clúster 77 (Sofisticación)
            # Justificación: Rompen la rutina espacial, buscan estímulos nuevos constantemente.
            "exploration_rho_bonus": 0.35,      # Multiplicador MASIVO a explorar lugares desconocidos en el mapa
            "markov_weight_modifiers": {
                "OCIO_INDIVIDUAL": 1.3,         # Salen a caminar, leer, explorar (Curiosidad)
                "INACTIVO_RELAX": 0.8           # Se aburren rápidamente de la monotonía casera
            }
        },
        "-": {
            # GOLDBERG (-): Clúster 78 (Superficialidad), Clúster 79 (Falta de imaginación / Convencional)
            # Justificación: Conservadores espaciales, repiten la misma ruta toda su vida.
            "exploration_rho_bonus": -0.30,     # Su fórmula EPR casi siempre dictará "Retorno preferencial"
            "markov_weight_modifiers": {
                "OCIO_INDIVIDUAL": 0.7,
                "INACTIVO_RELAX": 1.2           # Preferencia por lo conocido y rutinario
            }
        }
    }
}