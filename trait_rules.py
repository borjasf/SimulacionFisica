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
                # IMPACTO CAPA 1 (Dónde van - Condicionalidad Andresen)
                "OCIO": 1.2,
                "TAREAS_DOMESTICAS": 0.8,
                # IMPACTO CAPA 2 (Qué hacen - Frecuencia de actos sociales Mehl)
                "ocio_hosteleria": 2.5,        
                "conversacion_social": 1.8,
                "conversacion_con_companeros": 1.8,
                "conversacion_con_convivientes": 1.8,
                "interaccion_ingesta": 1.5,
                "ingesta_en_restauracion": 1.3,
                "consumo_audiovisual": 0.5,
                "ocio_digital_activo": 0.5,
                "lectura": 0.4
            },
            "exploration_rho_bonus": 0.15,      
            "homophily_base_bonus": 10          
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 
                "OCIO": 0.8,
                "TAREAS_DOMESTICAS": 1.2,
                # IMPACTO CAPA 2 
                "ver_rrss": 1.8,
                "revisar_rrss": 1.8,
                "ingesta_rrss": 1.8,
                "consumo_audiovisual": 1.5,
                "ocio_digital_activo": 1.5,
                "lectura": 1.5,
                "conversacion_social": 0.3,
                "conversacion_con_companeros": 0.3,
                "conversacion_con_convivientes": 0.3,
                "interaccion_ingesta": 0.3,
                "ocio_hosteleria": 0.1
            },
            "exploration_rho_bonus": -0.15      
        }
    },
    
    "Amiability": {
        "+": {
            "markov_weight_modifiers": {
                # Frecuencia de actos sociales solidarios/empáticos (Mehl, 2017)
                "conversacion_social": 1.4,
                "conversacion_con_companeros": 1.4,
                "conversacion_con_convivientes": 1.4,
                "interaccion_ingesta": 1.4
            },
            "homophily_base_bonus": 15          
        },
        "-": {
            "markov_weight_modifiers": {
                "conversacion_social": 0.5,
                "conversacion_con_companeros": 0.5,
                "conversacion_con_convivientes": 0.5,
                "interaccion_ingesta": 0.5
            },
            "homophily_base_bonus": -10         
        }
    },
    
    "Conscientiousness": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OBLIGACIONES": 1.3,
                "TAREAS_DOMESTICAS": 1.2,
                # IMPACTO CAPA 2 (Enfoque en orden y tareas - Goldberg, 1990)
                "jornada_laboral": 1.5,       
                "jornada_academica": 1.5,
                "mantenimiento_del_hogar": 1.8,
                "gestiones_personales": 1.6,
                "ver_rrss": 0.4,
                "revisar_rrss": 0.4,
                "ingesta_rrss": 0.4,
                "consumo_audiovisual": 0.6,
                "ocio_hosteleria": 0.5
            },
            "spatial_beta_modifier": 1.3        
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OBLIGACIONES": 0.7,
                "TAREAS_DOMESTICAS": 1.3,
                # IMPACTO CAPA 2
                "jornada_laboral": 0.6,       
                "jornada_academica": 0.6,
                "mantenimiento_del_hogar": 0.3,
                "gestiones_personales": 0.3,
                "ver_rrss": 1.6,
                "revisar_rrss": 1.6,
                "ingesta_rrss": 1.6,
                "ocio_digital_activo": 1.5
            },
            "spatial_beta_modifier": 0.8        
        }
    },
    
    "Neuroticism": {
        "+": {
            # Reactividad fisiológica al estrés en el día a día (Shui et al., 2023)
            "biological_urgency_k": 2.5,        
            "energy_decay_multiplier": 1.2,     
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OBLIGACIONES": 0.8,
                "TAREAS_DOMESTICAS": 1.2,
                # IMPACTO CAPA 2 (Refugio en actividades pasivas)
                "ver_rrss": 1.8,
                "revisar_rrss": 1.8,
                "ingesta_rrss": 1.8,             
                "consumo_audiovisual": 1.5,
                "jornada_laboral": 0.7,
                "jornada_academica": 0.7,
                "conversacion_social": 0.7,
                "conversacion_con_companeros": 0.7,
                "conversacion_con_convivientes": 0.7,
                "interaccion_ingesta": 0.7
            }
        },
        "-": {
            "biological_urgency_k": 3.5,        
            "energy_decay_multiplier": 0.8,     
            "markov_weight_modifiers": {
                "ver_rrss": 0.7,
                "revisar_rrss": 0.7,
                "ingesta_rrss": 0.7,
            }
        }
    },
    
    "Openness": {
        "+": {
            "exploration_rho_bonus": 0.35,      
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 1.3,
                "TAREAS_DOMESTICAS": 0.8,
                # IMPACTO CAPA 2 (Búsqueda de novedad y estimulación intelectual)
                "actividad_cultural": 2.5,         
                "lectura": 2.0,
                "paseo_recreativo": 1.4,
                "ingesta_en_restauracion": 1.3,
                "consumo_audiovisual": 0.6
            }
        },
        "-": {
            "exploration_rho_bonus": -0.30,     
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 0.7,
                "TAREAS_DOMESTICAS": 1.2,
                # IMPACTO CAPA 2
                "actividad_cultural": 0.3,
                "lectura": 0.5,
                "ingesta_en_restauracion": 0.7,
                "consumo_audiovisual": 1.4
            }
        }
    }
}