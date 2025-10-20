"""
Modelo de Datos Central - Ficha Técnica del Atleta

✅ AÑADIDOS: Nuevos campos técnicos de experiencia y competición
- running_experience_years: Experiencia total en atletismo 
- current_training_period: Período actual de entrenamiento
- competitive_level: Nivel competitivo alcanzado

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
    y prevenir recurrencias.
    """
    type: str = ""
    date_approx: str = ""
    recovery_desc: str = ""

@dataclass
class Race:
    """
    Representa una carrera objetivo (principal o intermedia).
    Incluye todos los parámetros necesarios para la periodización
    y personalización del plan de entrenamiento.
    """
    name: str = ""
    date: str = ""
    distance_km: float = 0.0
    goal_time: Optional[str] = None
    terrain: str = ""

@dataclass
class TrainingZones:
    """
    Zonas de entrenamiento basadas en frecuencia cardíaca.
    Calculadas usando la fórmula de Karvonen (FC de reserva).
    Cada zona tiene un propósito específico en la planificación.
    """
    zone1_hr: str = ""  # Recuperación activa (50-60%)
    zone2_hr: str = ""  # Base aeróbica (60-70%)
    zone3_hr: str = ""  # Aeróbico medio (70-80%)
    zone4_hr: str = ""  # Umbral anaeróbico (80-90%)
    zone5_hr: str = ""  # VO2máx/Neuromuscular (90-100%)

@dataclass
class AthleteProfile:
    """
    Perfil completo del atleta - Modelo de datos central.
    
    Esta clase encapsula toda la información necesaria para:
    1. Generar un plan de entrenamiento personalizado
    2. Crear documentación técnica profesional
    3. Alimentar sistemas de IA con contexto estructurado
    
    Los campos están organizados en secciones lógicas que facilitan
    tanto el procesamiento automatizado como la revisión humana.
    """
    
    # ═══════════════════════════════════════════════════════════
    # INFORMACIÓN PERSONAL BÁSICA
    # ═══════════════════════════════════════════════════════════
    name: str = ""
    age: Optional[int] = None
    gender: str = ""
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    
    # ═══════════════════════════════════════════════════════════
    # MÉTRICAS FISIOLÓGICAS
    # ═══════════════════════════════════════════════════════════
    max_hr: Optional[int] = None
    resting_hr: Optional[int] = None
    vo2_max: Optional[float] = None
    lactate_threshold_bpm: Optional[int] = None
    hrv_ms: Optional[int] = None
    training_zones: Optional[TrainingZones] = None
    
    # ═══════════════════════════════════════════════════════════
    # CONTEXTO DE ENTRENAMIENTO
    # ═══════════════════════════════════════════════════════════
    avg_weekly_km: Optional[float] = None
    training_days_per_week: str = ""
    
    # ✅ NUEVOS CAMPOS TÉCNICOS
    running_experience_years: Optional[float] = None
    current_training_period: str = ""
    
    # Disponibilidad y restricciones temporales
    available_training_days: str = ""
    unavailable_days: str = ""
    
    # Entrenamiento de fuerza
    strength_training_history: Optional[bool] = None
    include_strength_training: Optional[bool] = None
    
    # ═══════════════════════════════════════════════════════════
    # DATOS DE RENDIMIENTO
    # ═══════════════════════════════════════════════════════════
    personal_bests: Dict[str, str] = field(default_factory=dict)
    
    # ═══════════════════════════════════════════════════════════
    # OBJETIVOS Y PLANIFICACIÓN
    # ═══════════════════════════════════════════════════════════
    main_objective: Optional[Race] = None
    intermediate_races: List[Race] = field(default_factory=list)
    
    # ═══════════════════════════════════════════════════════════
    # HISTORIAL MÉDICO
    # ═══════════════════════════════════════════════════════════
    injuries: List[Injury] = field(default_factory=list)

    def is_complete(self) -> bool:
        """
        Determina si el perfil tiene información mínima para generar un plan.
        
        Criterios de completitud:
        - Información personal básica (nombre, edad, género)
        - Al menos una métrica fisiológica (FCmáx o FCrep)
        - Contexto mínimo de entrenamiento (volumen o días)
        - Objetivo principal definido
        
        Returns:
            bool: True si el perfil cumple los criterios mínimos
        """
        # Información básica obligatoria
        basic_info = bool(self.name and self.age and self.gender)
        
        # Al menos una métrica fisiológica
        physiological = bool(self.max_hr or self.resting_hr)
        
        # Contexto de entrenamiento mínimo
        training_context = bool(self.avg_weekly_km or self.training_days_per_week)
        
        # Objetivo definido
        has_objective = bool(self.main_objective)
        
        return basic_info and physiological and training_context and has_objective

    def _validate_training_days_coherence(self) -> List[str]:
        """
        Valida coherencia entre días disponibles y días no disponibles.
        
        Returns:
            List[str]: Lista de errores de coherencia encontrados
        """
        errors = []
        
        if not self.available_training_days or not self.unavailable_days:
            return errors  # No hay suficiente información para validar
        
        try:
            # Parsear días disponibles
            if '-' in self.available_training_days:
                available_parts = self.available_training_days.split('-')
                available_min = int(available_parts[0])
                available_max = int(available_parts[1]) if len(available_parts) > 1 else available_min
            else:
                available_min = available_max = int(self.available_training_days)
            
            # Contar días no disponibles
            unavailable_count = len([day.strip() for day in self.unavailable_days.split(',') if day.strip()])
            total_available_days = 7 - unavailable_count
            
            # Validar coherencia
            if total_available_days < available_min:
                errors.append(f"Incoherencia: quieres entrenar {available_min} días pero solo tienes {total_available_days} días disponibles")
            
            if unavailable_count >= 7:
                errors.append("No puedes tener todos los días como no disponibles")
                
        except (ValueError, AttributeError):
            # Si hay errores de parsing, no reportamos errores de coherencia
            pass
        
        return errors

    def to_dict(self) -> Dict:
        """
        Convierte el perfil a diccionario para serialización JSON.
        
        Maneja correctamente objetos anidados (TrainingZones, Race, Injury)
        y mantiene la estructura jerárquica para procesamiento posterior.
        
        Returns:
            Dict: Representación completa del perfil como diccionario
        """
        # Convertir objetos anidados a diccionarios
        training_zones_dict = None
        if self.training_zones:
            training_zones_dict = {
                'zone1_hr': self.training_zones.zone1_hr,
                'zone2_hr': self.training_zones.zone2_hr,
                'zone3_hr': self.training_zones.zone3_hr,
                'zone4_hr': self.training_zones.zone4_hr,
                'zone5_hr': self.training_zones.zone5_hr
            }
        
        main_objective_dict = None
        if self.main_objective:
            main_objective_dict = {
                'name': self.main_objective.name,
                'date': self.main_objective.date,
                'distance_km': self.main_objective.distance_km,
                'goal_time': self.main_objective.goal_time,
                'terrain': self.main_objective.terrain
            }
        
        intermediate_races_list = []
        for race in self.intermediate_races:
            intermediate_races_list.append({
                'name': race.name,
                'date': race.date,
                'distance_km': race.distance_km,
                'goal_time': race.goal_time,
                'terrain': race.terrain
            })
        
        injuries_list = []
        for injury in self.injuries:
            injuries_list.append({
                'type': injury.type,
                'date_approx': injury.date_approx,
                'recovery_desc': injury.recovery_desc
            })
        
        return {
            # Información personal
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            
            # Métricas fisiológicas
            'max_hr': self.max_hr,
            'resting_hr': self.resting_hr,
            'vo2_max': self.vo2_max,
            'lactate_threshold_bpm': self.lactate_threshold_bpm,
            'hrv_ms': self.hrv_ms,
            'training_zones': training_zones_dict,
            
            # Contexto de entrenamiento
            'avg_weekly_km': self.avg_weekly_km,
            'training_days_per_week': self.training_days_per_week,
            'running_experience_years': self.running_experience_years,  # ✅ NUEVO
            'current_training_period': self.current_training_period,     # ✅ NUEVO
            'available_training_days': self.available_training_days,
            'unavailable_days': self.unavailable_days,
            'strength_training_history': self.strength_training_history,
            'include_strength_training': self.include_strength_training,
            
            # Rendimiento
            'personal_bests': self.personal_bests,
            
            # Objetivos
            'main_objective': main_objective_dict,
            'intermediate_races': intermediate_races_list,
            
            # Historial médico
            'injuries': injuries_list
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'AthleteProfile':
        """
        Crea un AthleteProfile desde un diccionario.
        
        Reconstruye correctamente todos los objetos anidados y maneja
        campos faltantes con valores por defecto apropiados.
        
        Args:
            data: Diccionario con los datos del perfil
            
        Returns:
            AthleteProfile: Instancia completamente inicializada
        """
        # Reconstruir training_zones
        training_zones = None
        if data.get('training_zones'):
            zones_data = data['training_zones']
            training_zones = TrainingZones(
                zone1_hr=zones_data.get('zone1_hr', ''),
                zone2_hr=zones_data.get('zone2_hr', ''),
                zone3_hr=zones_data.get('zone3_hr', ''),
                zone4_hr=zones_data.get('zone4_hr', ''),
                zone5_hr=zones_data.get('zone5_hr', '')
            )
        
        # Reconstruir main_objective
        main_objective = None
        if data.get('main_objective'):
            obj_data = data['main_objective']
            main_objective = Race(
                name=obj_data.get('name', ''),
                date=obj_data.get('date', ''),
                distance_km=obj_data.get('distance_km', 0.0),
                goal_time=obj_data.get('goal_time'),
                terrain=obj_data.get('terrain', '')
            )
        
        # Reconstruir intermediate_races
        intermediate_races = []
        if data.get('intermediate_races'):
            for race_data in data['intermediate_races']:
                race = Race(
                    name=race_data.get('name', ''),
                    date=race_data.get('date', ''),
                    distance_km=race_data.get('distance_km', 0.0),
                    goal_time=race_data.get('goal_time'),
                    terrain=race_data.get('terrain', '')
                )
                intermediate_races.append(race)
        
        # Reconstruir injuries
        injuries = []
        if data.get('injuries'):
            for injury_data in data['injuries']:
                injury = Injury(
                    type=injury_data.get('type', ''),
                    date_approx=injury_data.get('date_approx', ''),
                    recovery_desc=injury_data.get('recovery_desc', '')
                )
                injuries.append(injury)
        
        # Crear instancia con todos los campos
        return cls(
            # Información personal
            name=data.get('name', ''),
            age=data.get('age'),
            gender=data.get('gender', ''),
            height_cm=data.get('height_cm'),
            weight_kg=data.get('weight_kg'),
            
            # Métricas fisiológicas
            max_hr=data.get('max_hr'),
            resting_hr=data.get('resting_hr'),
            vo2_max=data.get('vo2_max'),
            lactate_threshold_bpm=data.get('lactate_threshold_bpm'),
            hrv_ms=data.get('hrv_ms'),
            training_zones=training_zones,
            
            # Contexto de entrenamiento
            avg_weekly_km=data.get('avg_weekly_km'),
            training_days_per_week=data.get('training_days_per_week', ''),
            running_experience_years=data.get('running_experience_years'),      # ✅ NUEVO
            current_training_period=data.get('current_training_period', ''),    # ✅ NUEVO  
            available_training_days=data.get('available_training_days', ''),
            unavailable_days=data.get('unavailable_days', ''),
            strength_training_history=data.get('strength_training_history'),
            include_strength_training=data.get('include_strength_training'),
            
            # Rendimiento
            personal_bests=data.get('personal_bests', {}),
            
            # Objetivos
            main_objective=main_objective,
            intermediate_races=intermediate_races,
            
            # Historial médico
            injuries=injuries
        )

def create_empty_profile() -> AthleteProfile:
    """
    Crea un perfil de atleta vacío con valores por defecto.
    
    Útil para inicialización de nuevos perfiles y como baseline
    para comparaciones y validaciones.
    
    Returns:
        AthleteProfile: Perfil inicializado con valores por defecto
    """
    return AthleteProfile(
        personal_bests={
            '5k': '',
            '10k': '',
            'half_marathon': '',
            'marathon': ''
        }
    )