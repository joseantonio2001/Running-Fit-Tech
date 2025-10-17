"""
Modelo de Datos Central - Ficha Técnica del Atleta

Este módulo define la estructura completa del modelo de datos que actúa como
la "Single Source of Truth" de la aplicación. El diseño no solo está pensado
para almacenamiento interno, sino optimizado para actuar como un prompt 
estructurado y auto-explicativo para la IA externa.

Utiliza dataclasses de Python con tipado estático para garantizar:
- Validación automática de tipos
- Métodos de utilidad generados (__init__, __repr__)
- Documentación clara de cada campo y su propósito para la IA

La estructura del JSON de salida es el resultado de cuidadosa ingeniería
de prompts, transformando datos simples en un dossier de inteligencia
para el entrenador virtual.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
import json


@dataclass
class Injury:
    """
    Representa una lesión individual en el historial del atleta.
    
    Cada lesión contiene información crítica para adaptar el entrenamiento
    futuro, identificar patrones de riesgo y ajustar progresiones de carga.
    """
    type: str                    # Tipo de lesión (ej: "Fascitis Plantar")
    date_approx: str            # Fecha aproximada (ej: "2022-10")
    recovery_desc: str          # Descripción de la recuperación y tratamiento


@dataclass
class Race:
    """
    Representa una carrera objetivo (principal o intermedia).
    
    Define los objetivos competitivos del atleta y proporciona contexto
    temporal y de rendimiento para el diseño del plan de entrenamiento.
    """
    name: str                   # Nombre de la carrera
    date: str                   # Fecha en formato ISO (YYYY-MM-DD)
    distance_km: float          # Distancia en kilómetros
    goal_time: Optional[str]    # Tiempo objetivo en formato HH:MM:SS
    terrain: str               # Tipo de terreno ("Llano", "Montañoso", etc.)


@dataclass
class TrainingZones:
    """
    Zonas de entrenamiento calculadas basadas en FCmáx y FCreposo.
    
    Utiliza la Fórmula de Karvonen para definir 5 zonas de intensidad
    que guiarán la prescripción de entrenamientos específicos.
    """
    zone1_hr: Optional[str] = None     # Z1: 50-60% FCR (Recuperación)
    zone2_hr: Optional[str] = None     # Z2: 60-70% FCR (Aeróbico base)
    zone3_hr: Optional[str] = None     # Z3: 70-80% FCR (Aeróbico)
    zone4_hr: Optional[str] = None     # Z4: 80-90% FCR (Umbral)
    zone5_hr: Optional[str] = None     # Z5: 90-100% FCR (VO2máx)


@dataclass
class AthleteProfile:
    """
    Perfil completo del atleta - Modelo de datos central de la aplicación.
    
    Esta clase representa la "Ficha Técnica" completa que actúa como:
    1. Fuente única de verdad para todos los módulos del sistema
    2. Prompt estructurado y auto-explicativo para la IA externa
    3. Contrato inmutable entre componentes de la arquitectura
    
    Cada campo está diseñado con claves descriptivas y metadatos que
    maximizan la comprensión y contexto para generar planes de entrenamiento
    de calidad profesional.
    """
    
    # === RESUMEN DEL ATLETA ===
    name: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # === INFORMACIÓN PERSONAL ===
    age: Optional[int] = None
    gender: str = ""                    # Normalizado: "Masculino", "Femenino", "Otro"  
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    
    # === MÉTRICAS FISIOLÓGICAS ===
    # Meta-descripción para guiar a la IA
    physiological_metrics_meta: str = field(
        default="Métricas fisiológicas clave que definen el perfil de resistencia y el potencial del atleta."
    )
    max_hr: Optional[int] = None        # Frecuencia Cardíaca Máxima (FCmáx)
    resting_hr: Optional[int] = None    # Frecuencia Cardíaca en Reposo (FCrep)
    hrv_ms: Optional[int] = None        # Variabilidad FC en milisegundos
    vo2_max: Optional[float] = None     # VO2 Máx estimado (ml/kg/min)
    lactate_threshold_bpm: Optional[int] = None  # Umbral de lactato (ppm)
    
    # === HISTORIAL DE LESIONES ===
    # Meta-descripción para guiar a la IA  
    injury_history_meta: str = field(
        default="Historial de lesiones para identificar patrones de riesgo, debilidades estructurales y adaptar el entrenamiento de fuerza y las progresiones de carga."
    )
    injuries: List[Injury] = field(default_factory=list)
    
    # === CONTEXTO DE ENTRENAMIENTO ===
    avg_weekly_km: Optional[float] = None      # Volumen semanal actual promedio
    training_days_per_week: str = ""           # Disponibilidad ("4", "4-5", etc.)
    strength_training_history: bool = False    # Experiencia previa con fuerza
    include_strength_training: bool = False    # Preferencia para nuevo plan
    quality_session_preference: str = ""       # Días preferidos para series/tempo
    
    # === DATOS DE RENDIMIENTO ===
    personal_bests: Dict[str, Optional[str]] = field(default_factory=dict)  # PBs en formato HH:MM:SS
    training_zones: Optional[TrainingZones] = field(default_factory=TrainingZones)
    
    # === OBJETIVOS DE CARRERA ===
    main_objective: Optional[Race] = None
    intermediate_races: List[Race] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """
        Convierte el perfil a diccionario para serialización JSON.
        
        Estructura el diccionario siguiendo el formato optimizado para IA
        con claves descriptivas y anidamiento lógico que actúa como prompt
        estructurado de alta calidad.
        
        Returns:
            Dict: Diccionario estructurado listo para serialización JSON
        """
        return {
            "athlete_summary": {
                "name": self.name,
                "generated_at": self.generated_at
            },
            "personal_info": {
                "age": self.age,
                "gender": self.gender,
                "height_cm": self.height_cm,
                "weight_kg": self.weight_kg
            },
            "physiological_metrics": {
                "meta_description": self.physiological_metrics_meta,
                "max_hr": self.max_hr,
                "resting_hr": self.resting_hr,
                "hrv_ms": self.hrv_ms,
                "vo2_max": self.vo2_max,
                "lactate_threshold_bpm": self.lactate_threshold_bpm
            },
            "injury_history": {
                "meta_description": self.injury_history_meta,
                "injuries": [
                    {
                        "type": injury.type,
                        "date_approx": injury.date_approx,
                        "recovery_desc": injury.recovery_desc
                    } for injury in self.injuries
                ]
            },
            "training_context": {
                "avg_weekly_km": self.avg_weekly_km,
                "training_days_per_week": self.training_days_per_week,
                "strength_training_history": self.strength_training_history,
                "include_strength_training": self.include_strength_training,
                "quality_session_preference": self.quality_session_preference
            },
            "performance_data": {
                "personal_bests": self.personal_bests,
                "training_zones": {
                    "zone1_hr": self.training_zones.zone1_hr if self.training_zones else None,
                    "zone2_hr": self.training_zones.zone2_hr if self.training_zones else None,
                    "zone3_hr": self.training_zones.zone3_hr if self.training_zones else None,
                    "zone4_hr": self.training_zones.zone4_hr if self.training_zones else None,
                    "zone5_hr": self.training_zones.zone5_hr if self.training_zones else None,
                } if self.training_zones else None
            },
            "race_goals": {
                "main_objective": {
                    "name": self.main_objective.name,
                    "date": self.main_objective.date,
                    "distance_km": self.main_objective.distance_km,
                    "goal_time": self.main_objective.goal_time,
                    "terrain": self.main_objective.terrain
                } if self.main_objective else None,
                "intermediate_races": [
                    {
                        "name": race.name,
                        "date": race.date,
                        "distance_km": race.distance_km,
                        "goal_time": race.goal_time,
                        "terrain": race.terrain
                    } for race in self.intermediate_races
                ]
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AthleteProfile':
        """
        Crea una instancia de AthleteProfile desde un diccionario.
        
        Permite deserialización desde JSON manteniendo la estructura
        y validación de tipos del dataclass.
        
        Args:
            data: Diccionario con datos del perfil
            
        Returns:
            AthleteProfile: Instancia del perfil del atleta
        """
        profile = cls()
        
        # Resumen del atleta
        if "athlete_summary" in data:
            summary = data["athlete_summary"]
            profile.name = summary.get("name", "")
            profile.generated_at = summary.get("generated_at", profile.generated_at)
        
        # Información personal
        if "personal_info" in data:
            personal = data["personal_info"]
            profile.age = personal.get("age")
            profile.gender = personal.get("gender", "")
            profile.height_cm = personal.get("height_cm")
            profile.weight_kg = personal.get("weight_kg")
        
        # Métricas fisiológicas
        if "physiological_metrics" in data:
            physio = data["physiological_metrics"]
            profile.max_hr = physio.get("max_hr")
            profile.resting_hr = physio.get("resting_hr")
            profile.hrv_ms = physio.get("hrv_ms")
            profile.vo2_max = physio.get("vo2_max")
            profile.lactate_threshold_bpm = physio.get("lactate_threshold_bpm")
        
        # Historial de lesiones
        if "injury_history" in data and "injuries" in data["injury_history"]:
            for injury_data in data["injury_history"]["injuries"]:
                injury = Injury(
                    type=injury_data.get("type", ""),
                    date_approx=injury_data.get("date_approx", ""),
                    recovery_desc=injury_data.get("recovery_desc", "")
                )
                profile.injuries.append(injury)
        
        # Contexto de entrenamiento
        if "training_context" in data:
            training = data["training_context"]
            profile.avg_weekly_km = training.get("avg_weekly_km")
            profile.training_days_per_week = training.get("training_days_per_week", "")
            profile.strength_training_history = training.get("strength_training_history", False)
            profile.include_strength_training = training.get("include_strength_training", False)
            profile.quality_session_preference = training.get("quality_session_preference", "")
        
        # Datos de rendimiento
        if "performance_data" in data:
            performance = data["performance_data"]
            profile.personal_bests = performance.get("personal_bests", {})
            
            # Zonas de entrenamiento
            if "training_zones" in performance and performance["training_zones"]:
                zones_data = performance["training_zones"]
                profile.training_zones = TrainingZones(
                    zone1_hr=zones_data.get("zone1_hr"),
                    zone2_hr=zones_data.get("zone2_hr"),
                    zone3_hr=zones_data.get("zone3_hr"),
                    zone4_hr=zones_data.get("zone4_hr"),
                    zone5_hr=zones_data.get("zone5_hr")
                )
        
        # Objetivos de carrera
        if "race_goals" in data:
            goals = data["race_goals"]
            
            # Objetivo principal
            if "main_objective" in goals and goals["main_objective"]:
                main_data = goals["main_objective"]
                profile.main_objective = Race(
                    name=main_data.get("name", ""),
                    date=main_data.get("date", ""),
                    distance_km=main_data.get("distance_km", 0.0),
                    goal_time=main_data.get("goal_time"),
                    terrain=main_data.get("terrain", "")
                )
            
            # Carreras intermedias
            if "intermediate_races" in goals:
                for race_data in goals["intermediate_races"]:
                    race = Race(
                        name=race_data.get("name", ""),
                        date=race_data.get("date", ""),
                        distance_km=race_data.get("distance_km", 0.0),
                        goal_time=race_data.get("goal_time"),
                        terrain=race_data.get("terrain", "")
                    )
                    profile.intermediate_races.append(race)
        
        return profile
    
    def validate_data(self) -> List[str]:
        """
        Valida la integridad y coherencia de los datos del perfil.
        
        Implementa validaciones de lógica de negocio que van más allá
        del tipado estático, asegurando coherencia fisiológica y temporal.
        
        Returns:
            List[str]: Lista de errores encontrados (vacía si todo es válido)
        """
        errors = []
        
        # Validaciones fisiológicas
        if self.max_hr and self.resting_hr:
            if self.max_hr <= self.resting_hr:
                errors.append("FCmáx debe ser mayor que FCrep")
        
        if self.age:
            if self.age < 10 or self.age > 100:
                errors.append("Edad debe estar entre 10 y 100 años")
        
        if self.weight_kg:
            if self.weight_kg < 30 or self.weight_kg > 200:
                errors.append("Peso debe estar entre 30 y 200 kg")
                
        if self.height_cm:
            if self.height_cm < 100 or self.height_cm > 250:
                errors.append("Altura debe estar entre 100 y 250 cm")
        
        # Validaciones de entrenamiento
        if self.avg_weekly_km:
            if self.avg_weekly_km < 0 or self.avg_weekly_km > 300:
                errors.append("Volumen semanal debe estar entre 0 y 300 km")
        
        # Validaciones de género normalizado
        valid_genders = ["Masculino", "Femenino", "Otro"]
        if self.gender and self.gender not in valid_genders:
            errors.append(f"Género debe ser uno de: {', '.join(valid_genders)}")
        
        return errors
    
    def is_complete(self) -> bool:
        """
        Verifica si el perfil tiene datos mínimos para generar un plan.
        
        Define los campos críticos que deben estar presentes para que
        la IA pueda generar un plan de entrenamiento efectivo.
        
        Returns:
            bool: True si el perfil está completo para generar plan
        """
        required_fields = [
            self.name,
            self.age,
            self.gender,
            self.main_objective
        ]
        
        return all(field is not None and field != "" for field in required_fields)


def create_empty_profile() -> AthleteProfile:
    """
    Crea un perfil vacío con valores por defecto.
    
    Útil para inicializar nuevos perfiles o como plantilla
    para entrada manual de datos.
    
    Returns:
        AthleteProfile: Perfil vacío inicializado
    """
    profile = AthleteProfile()
    
    # Inicializar diccionario de marcas personales vacío
    profile.personal_bests = {
        "5k": None,
        "10k": None,
        "half_marathon": None,
        "marathon": None
    }
    
    return profile


def create_sample_profile() -> AthleteProfile:
    """
    Crea un perfil de muestra basado en el ejemplo del documento.
    
    Implementa los datos de "Tomás Solórzano" como referencia
    y para pruebas del sistema.
    
    Returns:
        AthleteProfile: Perfil de muestra completo
    """
    profile = AthleteProfile(
        name="Tomás Solórzano",
        age=19,
        gender="Masculino",
        height_cm=180,
        weight_kg=67.0,
        max_hr=184,
        resting_hr=41,
        vo2_max=60.0,
        lactate_threshold_bpm=179,
        avg_weekly_km=50.0,
        training_days_per_week="5",
        strength_training_history=False,
        include_strength_training=True,
        quality_session_preference="Martes, Jueves"
    )
    
    # Marcas personales
    profile.personal_bests = {
        "5k": "00:18:00",
        "10k": "00:39:50", 
        "half_marathon": "01:36:00",
        "marathon": None
    }
    
    # Objetivo principal
    profile.main_objective = Race(
        name="Media Maratón de Valencia",
        date="2024-11-30",
        distance_km=21.097,
        goal_time="01:28:00",
        terrain="Llano"
    )
    
    # Carrera intermedia
    intermediate_race = Race(
        name="10k de la Ciudad",
        date="2024-10-15",
        distance_km=10.0,
        goal_time="00:38:00",
        terrain="Llano"
    )
    profile.intermediate_races.append(intermediate_race)
    
    return profile
