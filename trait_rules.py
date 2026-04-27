# Implementación matemática de los 5 Grandes Rasgos de Personalidad (Big Five)
# Mapea rasgos a modificadores de probabilidad en macro-estados y micro-acciones

GOLDBERG_RULES = {
    "Sociability": {
        "+": {
            "markov_weight_modifiers": {
                # Extrovertido: Mayor propensión a ocio social
                "OCIO": 1.2,
                "TAREAS_DOMESTICAS": 0.8,
                
                # Micro-acciones: Actividades con interacción social elevada
                "ocio_hosteleria": 2.5,
                "conversacion_social": 1.8,
                "conversacion_con_companeros": 1.8,
                "conversacion_con_convivientes": 1.8,
                "interaccion_ingesta": 1.5,
                "ingesta_en_restauracion": 1.3,
                
                # Penalización de actividades solitarias
                "consumo_audiovisual": 0.5,
                "ocio_digital_activo": 0.5,
                "lectura": 0.4
            },
            "exploration_rho_bonus": 0.15,
            "homophily_base_bonus": 10
        },
        "-": {
            "markov_weight_modifiers": {
                # Introvertido: Mayor tendencia a actividades en solitario
                "OCIO": 0.8,
                "TAREAS_DOMESTICAS": 1.2,
                
                # Micro-acciones: Interacción asincrónica o pasiva
                "ver_rrss": 1.8,
                "revisar_rrss": 1.8,
                "ingesta_rrss": 1.8,
                "consumo_audiovisual": 1.5,
                "ocio_digital_activo": 1.5,
                "lectura": 1.5,
                
                # Penalización de interacción presencial
                "conversacion_social": 0.3,
                "conversacion_con_companeros": 0.3,
                "conversacion_con_convivientes": 0.3,
                "interaccion_ingesta": 0.3,
                "ocio_hosteleria": 0.1
            },
            "exploration_rho_bonus": -0.15
        }
    },
    
    "Friendliness": {
        "+": {
            "markov_weight_modifiers": {
                # Amable: Aumenta receptividad en interacciones
                "conversacion_social": 1.4,
                "conversacion_con_companeros": 1.4,
                "conversacion_con_convivientes": 1.4,
                "interaccion_ingesta": 1.4
            },
            "homophily_base_bonus": 15
        },
        "-": {
            "markov_weight_modifiers": {
                # Hostil: Evita interacción empática
                "conversacion_social": 0.5,
                "conversacion_con_companeros": 0.5,
                "conversacion_con_convivientes": 0.5,
                "interaccion_ingesta": 0.5
            },
            # Mapeo directo de adjetivos "Cold" y "Unsympathetic" elevando la barrera relacional
            "homophily_base_bonus": -10         
        }
    },
    
    "Scrupulousness": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Macro-estados)
                "OBLIGACIONES": 1.2,
                "TAREAS_DOMESTICAS": 1.2,
                
                # IMPACTO CAPA 2 (Micro-acciones)
                # Justificación: Goldberg (1990) Tabla 3, Factor III. Altas cargas en 
                # adjetivos "Organized", "Systematic", "Efficient", "Neat", "Thorough".
                "jornada_laboral": 1.5,         # Reflejo de "Efficient" y "Systematic"
                "jornada_academica": 1.5,
                "mantenimiento_del_hogar": 1.8, # Mapeo directo del clúster "Neat/Organized"
                "gestiones_personales": 1.5,   
                
                # Penalizaciones (Evitación de la procrastinación/desperdicio de tiempo)
                "ver_rrss": 0.4,                # Oposición al clúster de eficiencia
                "revisar_rrss": 0.4,
                "ingesta_rrss": 0.4,
                "consumo_audiovisual": 0.6,
            },
            "spatial_beta_modifier": 1.2        # Rutinas espaciales más estrictas (Systematic)
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OBLIGACIONES": 0.8,
                "TAREAS_DOMESTICAS": 0.8,       
                # IMPACTO CAPA 2
                # Justificación: Goldberg (1990) Tabla 3, Factor III (Polo Negativo). 
                # Altas cargas en "Disorganized", "Careless", "Inconsistent", "Sloppy".
                "jornada_laboral": 0.6,         # Reflejo de "Inconsistent"
                "jornada_academica": 0.6,
                "mantenimiento_del_hogar": 0.4, # Mapeo directo de "Sloppy/Disorganized"
                "gestiones_personales": 0.6,
                
                # Refugio en la distracción pasiva (Comportamiento "Careless")
                "ver_rrss": 1.6,              
                "revisar_rrss": 1.6,
                "ingesta_rrss": 1.6,
                "consumo_audiovisual": 1.3
            },
            "spatial_beta_modifier": 0.8        # Movimientos y rutas más erráticas
        }
    },
    
    "Neuroticism": {
        "+": {
            # IMPACTO FÍSICO (biological_engine.py)
            # Justificación: Goldberg (1990) Tabla 3, Factor IV. 
            # Altas cargas en adjetivos "Nervous", "Tense", "Anxious".
            # La tensión fisiológica y la ansiedad aceleran el desgaste de energía (carga alostática).
            "biological_urgency_k": 2.5,        # Menor tolerancia al malestar (reacciona antes al hambre/sueño)
            "energy_decay_multiplier": 1.2,     # Mayor desgaste por hiperactivación ("Tense")
            
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Macro-estados)
                "OBLIGACIONES": 0.8,            # Evitación de estrés
                "TAREAS_DOMESTICAS": 1.2,       # Búsqueda de control en un entorno seguro
                
                # IMPACTO CAPA 2 (Micro-acciones)
                # Justificación adjetivos: "Fearful", "Moody".
                # Refugio en la estimulación pasiva como estrategia de regulación emocional.
                "ver_rrss": 1.8,
                "revisar_rrss": 1.8,
                "ingesta_rrss": 1.8,             
                "consumo_audiovisual": 1.5,
                
                # Retraimiento frente a entornos exigentes o ruidosos
                "jornada_laboral": 0.7,
                "jornada_academica": 0.7,
                "conversacion_social": 0.7,
                "conversacion_con_companeros": 0.7,
                "conversacion_con_convivientes": 0.7,
                "interaccion_ingesta": 0.7
            }
        },
        "-": {
            # IMPACTO FÍSICO
            # Justificación: Goldberg (1990) Tabla 3, Factor IV (Polo Negativo / Estabilidad).
            # Altas cargas en adjetivos "Calm", "Relaxed", "Steady".
            "biological_urgency_k": 3.5,        # Mayor resiliencia y tolerancia al malestar ("Steady")
            "energy_decay_multiplier": 0.8,     # Eficiencia energética por relajación física ("Calm")
            
            "markov_weight_modifiers": {
                # IMPACTO CAPA 2
                # Al tener una línea base emocional estable ("Relaxed"), hay una menor 
                # necesidad de usar las redes sociales como apoyo emocional.
                "ver_rrss": 0.7,
                "revisar_rrss": 0.7,
                "ingesta_rrss": 0.7
            }
        }
    },
    
    "Intellectual": {
        "+": {
            # IMPACTO ESPACIAL Y DE RUTINA
            # Justificación: Goldberg (1990) Tabla 3, Factor V.
            # Altas cargas en adjetivos "Curious", "Imaginative", "Innovative".
            # Rompe la rutina espacial buscando estímulos novedosos.
            "exploration_rho_bonus": 0.35,      
            
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Macro-estados)
                "OCIO": 1.3,
                "TAREAS_DOMESTICAS": 0.8,
                
                # IMPACTO CAPA 2 (Micro-acciones)
                # Mapeo directo del clúster "Intellectual" y "Artistic" de Goldberg.
                "actividad_cultural": 2.5,         # Fuerte impulso a museos, teatro, etc.
                "lectura": 2.0,                    # Estimulación intelectual abstracta
                "paseo_recreativo": 1.4,           # Búsqueda de estímulos visuales (flâneur)
                "ingesta_en_restauracion": 1.3,    # Curiosidad gastronómica
                
                # Penalización a la monotonía y el conformismo
                "consumo_audiovisual": 0.6
            }
        },
        "-": {
            # IMPACTO ESPACIAL
            # Justificación: Goldberg (1990) Factor V (Polo Negativo).
            # Altas cargas en "Conventional", "Unimaginative", "Uncreative".
            # Fuerte apego a la rutina conocida, evitación de lo nuevo.
            "exploration_rho_bonus": -0.30,     
            
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 0.7,
                "TAREAS_DOMESTICAS": 1.2,
                
                # IMPACTO CAPA 2
                # Evitación de entornos intelectualmente o artísticamente exigentes.
                "actividad_cultural": 0.3,
                "lectura": 0.5,
                "ingesta_en_restauracion": 0.7,
                
                # Refugio en lo predecible y convencional
                "consumo_audiovisual": 1.4
            }
        }
    }
}