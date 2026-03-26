from trait_rules import GOLDBERG_RULES

class Agent:
    def __init__(self, agent_id, name, social_activity, traits_list, age, gender, occupation, qualification, interests):
        self.id = agent_id
        self.name = name
        self.social_activity = float(social_activity)
        self.traits = traits_list
        
        self.age = int(age)
        self.age_group = self._calculate_age_group(self.age)

        self.gender = gender
        self.occupation = occupation
        self.qualification = qualification
        self.interests = interests

        self.backstory = ""

        # Frecuencias ahora registran la macro y la micro acción anidada
        self.macro_frequencies = {"DORMIR": 1}
        self.micro_frequencies = {"DORMIR": {"dormir_profundamente": 1}}
        
        # VARIABLES BIOLÓGICAS
        self.energia = 100
        self.saciedad = 100

        self.energy_decay_mult = 1.0
        self.energy_recovery_mult = 1.0
        self.urgency_k = 3.0
        self.exploration_rho_bonus = 0.0
        self.spatial_beta_modifier = 1.0
        self.homophily_base_bonus = 0
        self.markov_modifiers = {}
        
        # VARIABLES ESPACIALES 
        self.home_coords = None     
        self.current_coords = None  
        self.visited_places = {}    
        self.current_location_name = "Casa"

        # MEMORIA
        self.short_term_memory = "Acabo de despertar." 
        self.action_buffer = []     
        self.long_term_memory = "Últimamente mi rutina ha sido bastante normal y estable."

        self.amigos = []

        # Frecuencias ahora registran la macro y la micro acción
        self.macro_frequencies = {"DORMIR": 1}
        self.micro_frequencies = {"dormir_profundamente": 1}

        self._apply_traits()

    def _calculate_age_group(self, age):
        if age < 16: return "16-"
        elif 16 <= age <= 24: return "16-24"
        elif 25 <= age <= 44: return "25-44"
        elif 45 <= age <= 64: return "45-64"
        else: return "65+"

    def _apply_traits(self):
        for trait_str in self.traits:
            parts = trait_str.strip().split(" ")
            if len(parts) == 2:
                trait_name, sign = parts[0], parts[1]
                if trait_name in GOLDBERG_RULES and sign in GOLDBERG_RULES[trait_name]:
                    rules = GOLDBERG_RULES[trait_name][sign]
                    if "energy_decay_multiplier" in rules:
                        self.energy_decay_mult *= rules["energy_decay_multiplier"]
                    if "energy_recovery_multiplier" in rules:
                        self.energy_recovery_mult *= rules["energy_recovery_multiplier"]
                    if "biological_urgency_k" in rules:
                        self.urgency_k = rules["biological_urgency_k"] 
                    if "exploration_rho_bonus" in rules:
                        self.exploration_rho_bonus += rules["exploration_rho_bonus"] 
                    if "spatial_beta_modifier" in rules:
                        self.spatial_beta_modifier *= rules["spatial_beta_modifier"]
                    if "homophily_base_bonus" in rules:
                        self.homophily_base_bonus += rules["homophily_base_bonus"] 
                    if "markov_weight_modifiers" in rules:
                        for action, mult in rules["markov_weight_modifiers"].items():
                            self.markov_modifiers[action] = self.markov_modifiers.get(action, 1.0) * mult

    def update_memory(self, new_macro, new_micro, location_name, turno_global, virtual_summary=""):
        """Gestiona la memoria a corto plazo. Si hay actividad virtual, la prioriza en la narrativa."""
        if new_macro != self.current_macro_state or new_micro != self.current_micro_action or virtual_summary:
            recuerdo_pasado = self.short_term_memory
            self.action_buffer.append(recuerdo_pasado)
            
            if virtual_summary:
                # Si usó las redes, el recuerdo detalla su sesión virtual exacta
                self.short_term_memory = f"He estado en {location_name} usando el móvil: {virtual_summary}."
            else:
                # Si fue una acción puramente física
                accion_natural = new_micro.replace("_", " ")
                self.short_term_memory = f"He estado haciendo lo siguiente: '{accion_natural}' en {location_name}."
            
        return False

    def flush_short_term_memory(self):
        acciones = list(self.action_buffer)
        self.action_buffer.clear()
        return acciones

    def update_long_term_memory(self, nueva_reflexion):
        self.long_term_memory = nueva_reflexion
            
    def update_state(self, new_macro, new_micro):
        """Actualiza el estado jerárquico y los contadores estadísticos anidados."""
        self.current_macro_state = new_macro
        self.current_micro_action = new_micro
        
        self.macro_frequencies[new_macro] = self.macro_frequencies.get(new_macro, 0) + 1
        
        if new_macro not in self.micro_frequencies:
            self.micro_frequencies[new_macro] = {}
        self.micro_frequencies[new_macro][new_micro] = self.micro_frequencies[new_macro].get(new_micro, 0) + 1

    def __repr__(self):
        return f"<Agent {self.name} | {self.current_macro_state} -> {self.current_micro_action}>"