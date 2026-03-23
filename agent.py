from trait_rules import GOLDBERG_RULES

class Agent:
    def __init__(self, agent_id, name, social_activity, traits_list, age, gender, occupation, qualification, interests):
        # Datos estáticos del CSV
        self.id = agent_id
        self.name = name
        self.social_activity = float(social_activity)
        self.traits = traits_list
        
        # EDAD Y GRUPO DEMOGRÁFICO 
        self.age = int(age)
        self.age_group = self._calculate_age_group(self.age)

        # CAMPOS PARA LA BACKSTORY
        self.gender = gender
        self.occupation = occupation
        self.qualification = qualification
        self.interests = interests

        # BACKSTORY DE PRUEBA (DESACTIVADA)
        self.backstory = ""

        # Máquina de estados
        # Todos empiezan durmiendo o inactivos por defecto
        self.current_state = "DORMIR" 
        
        # VARIABLES BIOLÓGICAS
        self.energia = 100
        self.saciedad = 100

        # MULTIPLICADORES DE PERSONALIDAD BASE
        self.energy_decay_mult = 1.0
        self.energy_recovery_mult = 1.0
        self.urgency_k = 3.0
        self.exploration_rho_bonus = 0.0
        self.spatial_beta_modifier = 1.0
        self.homophily_base_bonus = 0
        self.markov_modifiers = {}
        
        # VARIABLES ESPACIALES 
        self.home_coords = None     # Su casa fija (X, Y)
        self.current_coords = None  # Dónde está en este preciso momento
        self.visited_places = {}    # Memoria de lugares: {"Bar_Manolo": 3, "Parque": 1}

        self.current_location_name = "Casa"

        # FASE 2 y 3: MEMORIA LLM-CENTRIC (NUEVO DISEÑO MINIMALISTA)
        self.short_term_memory = "Acabo de despertar." 
        self.action_buffer = []     # Lista simple de strings cronológicos
        # El largo plazo ahora es un texto único que el LLM va actualizando
        self.long_term_memory = "Últimamente mi rutina ha sido bastante normal y estable."

        # VARIABLE: Amigos en red social
        self.amigos = []

        self.state_frequencies = {"DORMIR": 1}

        # Al nacer, el agente procesa su ADN (sus rasgos)
        self._apply_traits()

    def _calculate_age_group(self, age):
        """Asigna el rango de edad según estándares demográficos."""
        if age < 16:
            return "16-"
        elif 16 <= age <= 24:
            return "16-24"
        elif 25 <= age <= 54:
            return "25-54"
        elif 55 <= age <= 64:
            return "55-64"
        else:
            return "65+"

    def _apply_traits(self):
        """Lee la lista de rasgos y altera los multiplicadores base usando las reglas de Goldberg."""
        for trait_str in self.traits:
            parts = trait_str.strip().split(" ")
            if len(parts) == 2:
                trait_name, sign = parts[0], parts[1]
                
                if trait_name in GOLDBERG_RULES and sign in GOLDBERG_RULES[trait_name]:
                    rules = GOLDBERG_RULES[trait_name][sign]
                    
                    # 1. Modificadores Biológicos
                    if "energy_decay_multiplier" in rules:
                        self.energy_decay_mult *= rules["energy_decay_multiplier"]
                    if "energy_recovery_multiplier" in rules:
                        self.energy_recovery_mult *= rules["energy_recovery_multiplier"]
                    if "biological_urgency_k" in rules:
                        self.urgency_k = rules["biological_urgency_k"] 
                        
                    # 2. Modificadores Espaciales y Sociales
                    if "exploration_rho_bonus" in rules:
                        self.exploration_rho_bonus += rules["exploration_rho_bonus"] 
                    if "spatial_beta_modifier" in rules:
                        self.spatial_beta_modifier *= rules["spatial_beta_modifier"]
                    if "homophily_base_bonus" in rules:
                        self.homophily_base_bonus += rules["homophily_base_bonus"] 
                        
                    # 3. Modificadores de Markov
                    if "markov_weight_modifiers" in rules:
                        for state, mult in rules["markov_weight_modifiers"].items():
                            self.markov_modifiers[state] = self.markov_modifiers.get(state, 1.0) * mult

    def update_memory(self, new_state, location_name, turno_global):
        """Gestiona la memoria a corto plazo. Acumula acciones cronológicamente."""
        if new_state != self.current_state:
            # Rescatamos lo que estaba haciendo hasta ahora
            recuerdo_pasado = self.short_term_memory
            
            # Lo guardamos en el búfer cronológico como texto puro
            self.action_buffer.append(recuerdo_pasado)
            
            # --- ACTUALIZAMOS EL PRESENTE ---
            state_to_text = {
                "DORMIR": "Estoy durmiendo y descansando",
                "COMER_BEBER": "Estoy comiendo/bebiendo algo",
                "TRABAJAR_ESTUDIAR": "Estoy enfocado trabajando/estudiando",
                "INACTIVO_RELAX": "Me estoy tomando un tiempo para relajarme",
                "INACTIVO_TAREAS_CASA": "Estoy haciendo tareas de mantenimiento en la casa",
                "OCIO_INDIVIDUAL": "Estoy disfrutando de un rato de ocio por mi cuenta",
                "OCIO_SOCIAL_SITIO": "Estoy pasando el rato en un lugar público",
                "OCIO_SOCIAL_CONVERSAR": "Estoy conversando de forma activa",
                "USANDO_RRSS": "Estoy navegando por las redes sociales y el entorno digital"
            }
            accion_texto = state_to_text.get(new_state, f"Estoy en estado {new_state}")
            self.short_term_memory = f"{accion_texto} en {location_name}."
            
        return False

    def flush_short_term_memory(self):
        """Devuelve toda la lista cronológica de acciones y vacía el búfer."""
        acciones = list(self.action_buffer)
        self.action_buffer.clear()
        return acciones

    def update_long_term_memory(self, nueva_reflexion):
        """Sustituye la memoria a largo plazo por el nuevo resumen narrativo del LLM."""
        self.long_term_memory = nueva_reflexion
            
    def update_state(self, new_state):
        """Actualiza el estado matemático actual sumando al contador de frecuencias."""
        self.current_state = new_state
        self.state_frequencies[new_state] = self.state_frequencies.get(new_state, 0) + 1

    def __repr__(self):
        return f"<Agent {self.name} | Edad: {self.age} ({self.age_group}) | Estado: {self.current_state}>"