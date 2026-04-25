# ==============================================================================
# ARCHIVO: trait_rules.py
# DESCRIPCIÓN: Traducción matemática de los 5 Grandes Rasgos de Personalidad 
# (Goldberg, 1990) aplicados a la CAPA 1 (MACRO-ESTADOS) y CAPA 2 (MICRO-ACCIONES).
# 
# Documentación Adicional Pesos:
# 1. Andresen et al. (2024) 2. Shui et al. (2023) 3. Mehl (2017) [Método EAR]
# ==============================================================================

GOLDBERG_RULES = {
    "Sociability": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Macro-estados)
                "OCIO": 1.2,
                "TAREAS_DOMESTICAS": 0.8,
                
                # IMPACTO CAPA 2 (Micro-acciones)
                # Justificación: Goldberg (1990) Tabla 3, Factor I. Altas cargas en 
                # adjetivos "Talkative", "Sociable" y "Active".
                "ocio_hosteleria": 2.5,        # Máxima expresión de "Active/Sociable"
                "conversacion_social": 1.8,    # Reflejo directo del clúster "Talkative"
                "conversacion_con_companeros": 1.8,
                "conversacion_con_convivientes": 1.8,
                "interaccion_ingesta": 1.5,
                "ingesta_en_restauracion": 1.3,
                
                # Penalizaciones lógicas (Evitación de la inactividad asocial)
                "consumo_audiovisual": 0.5,
                "ocio_digital_activo": 0.5,
                "lectura": 0.4                 # Penalizado por oponerse al clúster "Talkative"
            },
            "exploration_rho_bonus": 0.15,      # Mayor tendencia a explorar (Active)
            "homophily_base_bonus": 10          # Facilidad de conexión inicial
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 0.8,
                "TAREAS_DOMESTICAS": 1.2,
                
                # IMPACTO CAPA 2
                # Justificación: Goldberg (1990) Tabla 3, Factor I (Polo Negativo). 
                # Altas cargas en adjetivos "Quiet", "Reserved", "Introverted", "Silent".
                "ver_rrss": 1.8,               # Interacción asíncrona ("Reserved")
                "revisar_rrss": 1.8,
                "ingesta_rrss": 1.8,
                "consumo_audiovisual": 1.5,
                "ocio_digital_activo": 1.5,
                "lectura": 1.5,                # Reflejo directo del clúster "Quiet/Silent"
                
                # Penalizaciones de interacción (Inhibición social)
                "conversacion_social": 0.3,
                "conversacion_con_companeros": 0.3,
                "conversacion_con_convivientes": 0.3,
                "interaccion_ingesta": 0.3,
                "ocio_hosteleria": 0.1         # Fuerte penalización a entornos "Noisy/Active"
            },
            "exploration_rho_bonus": -0.15      # Menor tendencia a cambiar de rutina
        }
    },
    
    "Friendliness": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 2 (Micro-acciones)
                # Justificación: Goldberg (1990) Tabla 3, Factor II. Altas cargas en
                # adjetivos "Sympathetic", "Kind", "Warm", "Cooperative", "Friendly".
                # Refleja un aumento moderado en la receptividad social, no en la búsqueda 
                # activa (que pertenece a Sociability).
                "conversacion_social": 1.4,
                "conversacion_con_companeros": 1.4,
                "conversacion_con_convivientes": 1.4,
                "interaccion_ingesta": 1.4
            },
            # Mapeo directo de adjetivos "Trusting" y "Forgiving" reduciendo la fricción relacional
            "homophily_base_bonus": 15          
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 2
                # Justificación: Goldberg (1990) Tabla 3, Factor II (Polo Negativo).
                # Altas cargas en "Cold", "Unfriendly", "Uncooperative", "Selfish".
                # Evitación de la interacción social empática o cooperativa.
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
                "OBLIGACIONES": 1.3,
                "TAREAS_DOMESTICAS": 1.2,
                
                # IMPACTO CAPA 2 (Micro-acciones)
                # Justificación: Goldberg (1990) Tabla 3, Factor III. Altas cargas en 
                # adjetivos "Organized", "Systematic", "Efficient", "Neat", "Thorough".
                "jornada_laboral": 1.5,         # Reflejo de "Efficient" y "Systematic"
                "jornada_academica": 1.5,
                "mantenimiento_del_hogar": 1.8, # Mapeo directo del clúster "Neat/Organized"
                "gestiones_personales": 1.6,    # Reflejo de "Thorough" (Meticuloso)
                
                # Penalizaciones (Evitación de la procrastinación/desperdicio de tiempo)
                "ver_rrss": 0.4,                # Oposición al clúster de eficiencia
                "revisar_rrss": 0.4,
                "ingesta_rrss": 0.4,
                "consumo_audiovisual": 0.6,
                "ocio_hosteleria": 0.5
            },
            "spatial_beta_modifier": 1.3        # Rutinas espaciales más estrictas (Systematic)
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OBLIGACIONES": 0.7,
                "TAREAS_DOMESTICAS": 0.7,       # Corregido: La desorganización reduce las tareas
                
                # IMPACTO CAPA 2
                # Justificación: Goldberg (1990) Tabla 3, Factor III (Polo Negativo). 
                # Altas cargas en "Disorganized", "Careless", "Inconsistent", "Sloppy".
                "jornada_laboral": 0.6,         # Reflejo de "Inconsistent" (Inconstante)
                "jornada_academica": 0.6,
                "mantenimiento_del_hogar": 0.3, # Mapeo directo de "Sloppy/Disorganized"
                "gestiones_personales": 0.3,
                
                # Refugio en la distracción pasiva (Comportamiento "Careless")
                "ver_rrss": 1.6,              
                "revisar_rrss": 1.6,
                "ingesta_rrss": 1.6,
                "ocio_digital_activo": 1.5
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