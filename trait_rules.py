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
                "CASA": 0.8,
                # IMPACTO CAPA 2 (Qué hacen - Frecuencia de actos sociales Mehl)
                "tomar_algo": 2.5,         
                "conversar": 1.8,               
                "conversar_comiendo": 1.5,
                "comer_fuera_de_casa": 1.3,
                "ver_la_television": 0.5,
                "jugar_videojuegos": 0.5,
                "leer": 0.4
            },
            "exploration_rho_bonus": 0.15,      
            "homophily_base_bonus": 10          
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 
                "OCIO": 0.8,
                "CASA": 1.2,
                # IMPACTO CAPA 2 
                "usar_rrss": 1.8,
                "ver_la_television": 1.5,
                "jugar_videojuegos": 1.5,
                "leer": 1.5,
                "conversar": 0.3,
                "tomar_algo": 0.1
            },
            "exploration_rho_bonus": -0.15      
        }
    },
    
    "Amiability": {
        "+": {
            "markov_weight_modifiers": {
                # Frecuencia de actos sociales solidarios/empáticos (Mehl, 2017)
                "conversar": 1.4,
                "conversar_comiendo": 1.4
            },
            "homophily_base_bonus": 15          
        },
        "-": {
            "markov_weight_modifiers": {
                "conversar": 0.5,
                "conversar_comiendo": 0.5
            },
            "homophily_base_bonus": -10         
        }
    },
    
    "Conscientiousness": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "TRABAJAR_ESTUDIAR": 1.3,
                "CASA": 1.2,
                # IMPACTO CAPA 2 (Enfoque en orden y tareas - Goldberg, 1990)
                "trabajar": 1.5,       
                "ir_a_clase": 1.5,
                "hacer_limpieza": 1.8,
                "tareas_personales": 1.6,
                "usar_rrss": 0.4,
                "ver_la_television": 0.6,
                "tomar_algo": 0.5
            },
            "spatial_beta_modifier": 1.3        
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "TRABAJAR_ESTUDIAR": 0.7,
                "CASA": 1.3,
                # IMPACTO CAPA 2
                "trabajar": 0.6,       
                "ir_a_clase": 0.6,
                "hacer_limpieza": 0.3,
                "tareas_personales": 0.3,
                "usar_rrss": 1.6,
                "jugar_videojuegos": 1.5
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
                "TRABAJAR_ESTUDIAR": 0.8,
                "CASA": 1.2,
                # IMPACTO CAPA 2 (Refugio en actividades pasivas)
                "usar_rrss": 1.8,             
                "ver_la_television": 1.5,
                "trabajar": 0.7,
                "ir_a_clase": 0.7,
                "conversar": 0.7
            }
        },
        "-": {
            "biological_urgency_k": 3.5,        
            "energy_decay_multiplier": 0.8,     
            "markov_weight_modifiers": {
                "usar_rrss": 0.7
            }
        }
    },
    
    "Openness": {
        "+": {
            "exploration_rho_bonus": 0.35,      
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 1.3,
                "CASA": 0.8,
                # IMPACTO CAPA 2 (Búsqueda de novedad y estimulación intelectual)
                "culturizarse": 2.5,         
                "leer": 2.0,
                "dar_una_vuelta": 1.4,
                "comer_fuera_de_casa": 1.3,
                "ver_la_television": 0.6
            }
        },
        "-": {
            "exploration_rho_bonus": -0.30,     
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "OCIO": 0.7,
                "CASA": 1.2,
                # IMPACTO CAPA 2
                "culturizarse": 0.3,
                "leer": 0.5,
                "comer_fuera_de_casa": 0.7,
                "ver_la_television": 1.4
            }
        }
    }
}