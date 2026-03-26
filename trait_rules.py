# ==============================================================================
# ARCHIVO: trait_rules.py
# DESCRIPCIÓN: Traducción matemática de los 5 Grandes Rasgos de Personalidad 
# aplicados a la CAPA 1 (MACRO-ESTADOS) y CAPA 2 (MICRO-ACCIONES).
# ==============================================================================

GOLDBERG_RULES = {
    "Sociability": {
        "+": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Dónde van)
                "OCIO": 1.4,
                "CASA": 0.7,
                # IMPACTO CAPA 2 (Qué hacen)
                "salir_de_fiesta": 2.5,         
                "conversar": 1.8,               
                "charlar_mientras_comes": 1.5,
                "dar_una_vuelta": 1.3,
                "ver_la_tv": 0.5,
                "jugar_videojuegos": 0.5
            },
            "exploration_rho_bonus": 0.15,      
            "homophily_base_bonus": 10          
        },
        "-": {
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1 (Dónde van)
                "OCIO": 0.6,
                "CASA": 1.4,
                # IMPACTO CAPA 2 (Qué hacen)
                "usar_rrss": 1.8,
                "ver_las_rrss": 1.8,
                "ver_la_tv": 1.5,
                "jugar_videojuegos": 1.5,
                "conversar": 0.3,
                "salir_de_fiesta": 0.1
            },
            "exploration_rho_bonus": -0.15      
        }
    },
    
    "Amiability": {
        "+": {
            "markov_weight_modifiers": {
                "conversar": 1.4,
                "charlar_mientras_comes": 1.4
            },
            "homophily_base_bonus": 15          
        },
        "-": {
            "markov_weight_modifiers": {
                "conversar": 0.5,
                "charlar_mientras_comes": 0.5
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
                # IMPACTO CAPA 2
                "trabajar": 1.5,       
                "ir_a_clase": 1.5,
                "hacer_limpieza": 1.8,
                "usar_rrss": 0.4,
                "ver_las_rrss": 0.4,
                "ver_la_tv": 0.6,
                "salir_de_fiesta": 0.5
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
                "usar_rrss": 1.6,
                "ver_las_rrss": 1.6,
                "jugar_videojuegos": 1.5
            },
            "spatial_beta_modifier": 0.8        
        }
    },
    
    "Neuroticism": {
        "+": {
            "biological_urgency_k": 2.5,        
            "energy_decay_multiplier": 1.2,     
            "markov_weight_modifiers": {
                # IMPACTO CAPA 1
                "TRABAJAR_ESTUDIAR": 0.8,
                "CASA": 1.2,
                # IMPACTO CAPA 2
                "usar_rrss": 1.8,             
                "ver_las_rrss": 1.8,
                "trabajar": 0.7,
                "ir_a_clase": 0.7
            }
        },
        "-": {
            "biological_urgency_k": 3.5,        
            "energy_decay_multiplier": 0.8,     
            "markov_weight_modifiers": {
                "usar_rrss": 0.7,
                "ver_las_rrss": 0.7
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
                # IMPACTO CAPA 2
                "culturizarse": 2.5,         
                "dar_una_vuelta": 1.4,
                "comer_fuera": 1.3,
                "ver_la_tv": 0.6
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
                "comer_fuera": 0.7,
                "ver_la_tv": 1.4
            }
        }
    }
}