"""
JSON AI Optimization Module - ACTUALIZADO SIN EXPERIENCE_NOTES

✅ ELIMINADO: Campo "experience_notes" que podría sesgar razonamiento de IA
✅ AÑADIDOS: Nuevos campos técnicos para mejor contexto de IA
- running_experience_years: Experiencia deportiva total
- current_training_period: Período de entrenamiento actual

✅ MANTENIDO: Campo "include_strength_training" en JSON (eliminado solo del PDF)
✅ CORREGIDO: Sin importación circular
✅ LIMPIO: Sin análisis de coherencia en JSON (se fuerza en CLI)

This module specializes in transforming the AthleteProfile data model
into an AI-optimized JSON structure without ANY conditioning of AI reasoning.
The output provides pure raw data and minimal descriptive analysis to allow
AI systems complete autonomy in generating training recommendations.

Key optimizations:
- Descriptive keys with contextual meaning
- Metadata descriptions for data interpretation only
- Logical data nesting and grouping
- Self-explanatory structure reducing ambiguity
- REMOVED ALL fields that could bias AI decision-making
- Pure data focus with maximum AI autonomy
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from .models import AthleteProfile, TrainingZones, Injury, Race
from .calculations import calculate_bmi, format_distance_for_display

def optimize_profile_for_ai(profile: AthleteProfile) -> Dict[str, Any]:
    """
    Transform athlete profile into AI-optimized JSON structure.
    
    This function implements the prompt engineering strategy defined in the
    technical specification. The resulting JSON serves as a structured
    prompt that provides maximum context and clarity to AI systems
    WITHOUT any conditioning of their reasoning process.
    
    Args:
        profile: Complete athlete profile data
        
    Returns:
        Dict[str, Any]: AI-optimized data structure (maximally unbiased)
    """
    
    # Calculate derived metrics
    bmi = None
    if profile.weight_kg and profile.height_cm:
        bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
    
    # Build optimized structure (maximally unbiased version)
    ai_data = {
        "athlete_summary": {
            "meta_description": "Resumen ejecutivo del atleta para personalización de la comunicación y contextualización general del perfil.",
            "name": profile.name,
            "age": profile.age,
            "gender": profile.gender,
            "generated_at": datetime.now().isoformat(),
            "profile_completeness": _calculate_profile_completeness(profile)
        },
        
        "personal_info": {
            "meta_description": "Datos personales básicos del atleta, incluyendo antropometría relevante para cálculos fisiológicos y biomecánicos.",
            "age": profile.age,
            "gender": profile.gender,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "bmi": bmi
        },
        
        "physiological_metrics": _build_physiological_section(profile),
        "training_context": _build_training_context_section_with_new_fields(profile),
        "performance_data": _build_performance_section(profile),
        "race_goals": _build_race_goals_section(profile),
        "injury_history": _build_injury_history_section(profile)
    }
    
    return ai_data

def _build_physiological_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build physiological metrics section for AI (unbiased version)."""
    
    section = {
        "meta_description": "Métricas fisiológicas clave que definen el perfil de resistencia y el potencial aeróbico del atleta. Estos datos son fundamentales para establecer zonas de entrenamiento precisas y adaptar la intensidad del plan.",
        "max_hr": profile.max_hr,
        "resting_hr": profile.resting_hr,
        "vo2_max": profile.vo2_max,
        "lactate_threshold_bpm": profile.lactate_threshold_bpm,
        "hrv_ms": profile.hrv_ms,
        "training_zones": None
    }
    
    # Add training zones if available
    if profile.training_zones:
        section["training_zones"] = {
            "calculation_method": "Fórmula de Karvonen basada en FC de reserva",
            "zones": {
                "zone1_recovery": {
                    "name": "Recuperación Activa",
                    "hr_range": profile.training_zones.zone1_hr,
                    "intensity": "50-60% FC Reserva",
                    "purpose": "Regeneración y volumen base sin estrés metabólico"
                },
                "zone2_aerobic": {
                    "name": "Aeróbico Ligero",
                    "hr_range": profile.training_zones.zone2_hr,
                    "intensity": "60-70% FC Reserva",
                    "purpose": "Base aeróbica y resistencia fundamental"
                },
                "zone3_tempo": {
                    "name": "Aeróbico Medio",
                    "hr_range": profile.training_zones.zone3_hr,
                    "intensity": "70-80% FC Reserva",
                    "purpose": "Desarrollo aeróbico y tempo sostenido"
                },
                "zone4_threshold": {
                    "name": "Umbral Anaeróbico",
                    "hr_range": profile.training_zones.zone4_hr,
                    "intensity": "80-90% FC Reserva",
                    "purpose": "Potencia aeróbica máxima y mejora VO2máx"
                },
                "zone5_vo2max": {
                    "name": "Potencia Máxima",
                    "hr_range": profile.training_zones.zone5_hr,
                    "intensity": "90-100% FC Reserva",
                    "purpose": "Capacidad anaeróbica y velocidad máxima"
                }
            }
        }
    
    return section

def _build_training_context_section_with_new_fields(profile: AthleteProfile) -> Dict[str, Any]:
    """
    ✅ Build training context section CON NUEVOS CAMPOS TÉCNICOS - SIN EXPERIENCE_NOTES.
    
    Incluye los nuevos campos técnicos y mantiene "include_strength_training"
    (solo se eliminó del PDF, no del JSON).
    
    ❌ ELIMINADO: "experience_notes" que podría sesgar el razonamiento de la IA.
    """
    
    return {
        "meta_description": "Contexto actual de entrenamiento del atleta, incluyendo experiencia deportiva, carga de trabajo, disponibilidad temporal y restricciones de horario. Esta información es crucial para adaptar el volumen, frecuencia y distribución de entrenamientos.",
        
        "current_training_load": {
            "avg_weekly_km": profile.avg_weekly_km,
            "training_days_per_week": profile.training_days_per_week
        },
        
        # ✅ NUEVOS CAMPOS TÉCNICOS (sin experience_notes)
        "experience_and_background": {
            "running_experience_years": profile.running_experience_years,
            "current_training_period": profile.current_training_period
            # ❌ ELIMINADO: "experience_notes": _generate_experience_notes(profile)
        },
        
        "availability_constraints": {
            "available_training_days": profile.available_training_days,
            "unavailable_days": profile.unavailable_days
        },
        
        "strength_training": {
            "history": profile.strength_training_history,
            "include_in_plan": profile.include_strength_training,  # ✅ MANTENIDO en JSON
            "integration_notes": _generate_strength_integration_notes(profile)
        }
    }

def _generate_strength_integration_notes(profile: AthleteProfile) -> str:
    """Generate strength training integration notes."""
    
    if profile.strength_training_history is None:
        return "Historial de fuerza no especificado"
    
    if profile.include_strength_training is None:
        return "Preferencia de inclusión no especificada"
    
    if profile.strength_training_history and profile.include_strength_training:
        return "Atleta experimentado - integración avanzada recomendada"
    elif not profile.strength_training_history and profile.include_strength_training:
        return "Principiante en fuerza - integración gradual recomendada"
    elif profile.strength_training_history and not profile.include_strength_training:
        return "Experiencia previa pero no desea incluir - mantener mínimo"
    else:
        return "Sin fuerza - enfoque aeróbico exclusivo"

def _build_performance_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build performance data section for AI (unbiased version)."""
    
    section = {
        "meta_description": "Datos de rendimiento actuales del atleta incluyendo marcas personales y análisis de nivel competitivo. Estos datos permiten establecer objetivos realistas y calibrar la intensidad del entrenamiento.",
        "personal_bests": {},
        "performance_analysis": None
    }
    
    if profile.personal_bests:
        # Enhanced personal bests with analysis
        distance_data = {
            "5k": {"distance_km": 5.0, "name": "5 Kilómetros"},
            "10k": {"distance_km": 10.0, "name": "10 Kilómetros"},
            "half_marathon": {"distance_km": 21.097, "name": "Media Maratón"},
            "marathon": {"distance_km": 42.195, "name": "Maratón"}
        }
        
        for key, info in distance_data.items():
            if profile.personal_bests.get(key):
                time = profile.personal_bests[key]
                pace = _calculate_pace_from_time(time, info["distance_km"])
                
                section["personal_bests"][key] = {
                    "distance_name": info["name"],
                    "distance_km": info["distance_km"],
                    "best_time": time,
                    "average_pace": pace,
                    "performance_level": _assess_performance_level(key, time, profile.age, profile.gender)
                }
        
        section["performance_analysis"] = _analyze_overall_performance_unbiased(profile)
    
    return section

def _build_race_goals_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build race goals section for AI."""
    
    section = {
        "meta_description": "Objetivos de carrera del atleta incluyendo objetivo principal y carreras intermedias. Esta sección define el enfoque y la periodización del plan de entrenamiento.",
        "main_objective": None,
        "intermediate_races": [],
        "goal_analysis": None
    }
    
    if profile.main_objective:
        section["main_objective"] = {
            "name": profile.main_objective.name,
            "date": profile.main_objective.date,
            "distance_km": profile.main_objective.distance_km,
            "distance_display": format_distance_for_display(profile.main_objective.distance_km),
            "goal_time": profile.main_objective.goal_time,
            "terrain": profile.main_objective.terrain,
            "weeks_until_race": _calculate_weeks_until_race(profile.main_objective.date),
            "goal_feasibility": _assess_goal_feasibility(profile)
        }
    
    if profile.intermediate_races:
        for race in profile.intermediate_races:
            section["intermediate_races"].append({
                "name": race.name,
                "date": race.date,
                "distance_km": race.distance_km,
                "distance_display": format_distance_for_display(race.distance_km),
                "goal_time": race.goal_time,
                "terrain": race.terrain,
                "strategic_purpose": _determine_race_purpose(race, profile.main_objective)
            })
    
    section["goal_analysis"] = _analyze_goal_structure(profile)
    
    return section

def _build_injury_history_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build injury history section for AI (unbiased version)."""
    
    section = {
        "meta_description": "Historial de lesiones para identificar patrones de riesgo, debilidades estructurales y adaptar el entrenamiento de fuerza y las progresiones de carga.",
        "injuries": [],
        "injury_analysis": None
    }
    
    if profile.injuries:
        for injury in profile.injuries:
            section["injuries"].append({
                "type": injury.type,
                "date_approx": injury.date_approx,
                "recovery_desc": injury.recovery_desc
            })
        
        section["injury_analysis"] = _analyze_injury_patterns(profile.injuries)
    else:
        section["injury_analysis"] = "Sin lesiones registradas - Perfil libre de restricciones por lesiones previas."
    
    return section

# Helper Functions for Analysis and Calculations

def _calculate_profile_completeness(profile: AthleteProfile) -> Dict[str, Any]:
    """Calculate profile completeness metrics."""
    
    total_fields = 0
    completed_fields = 0
    
    # Core fields (weighted more heavily)
    core_fields = [
        profile.name, profile.age, profile.gender,
        profile.max_hr, profile.resting_hr,
        profile.avg_weekly_km, profile.available_training_days,
        profile.main_objective
    ]
    
    for field in core_fields:
        total_fields += 2  # Core fields count double
        if field:
            completed_fields += 2
    
    # ✅ NUEVOS CAMPOS TÉCNICOS en completitud
    new_technical_fields = [
        profile.running_experience_years,
        profile.current_training_period,
    ]
    
    for field in new_technical_fields:
        total_fields += 1
        if field:
            completed_fields += 1
    
    # Optional fields
    optional_fields = [
        profile.height_cm, profile.weight_kg, profile.vo2_max,
        profile.lactate_threshold_bpm, profile.hrv_ms,
        profile.strength_training_history, profile.include_strength_training,
        profile.unavailable_days
    ]
    
    for field in optional_fields:
        total_fields += 1
        if field is not None:
            completed_fields += 1
    
    # Data sections
    if profile.personal_bests and any(profile.personal_bests.values()):
        completed_fields += 2
        total_fields += 2
    
    if profile.intermediate_races:
        completed_fields += 1
        total_fields += 1
    
    if profile.injuries:
        completed_fields += 1
        total_fields += 1
    
    completeness_percentage = (completed_fields / total_fields) * 100
    
    return {
        "completed_fields": completed_fields,
        "total_fields": total_fields,
        "completeness_percentage": round(completeness_percentage, 1),
        "readiness_level": _determine_readiness_level(completeness_percentage)
    }

def _analyze_overall_performance_unbiased(profile: AthleteProfile) -> Dict[str, Any]:
    """Analyze overall performance level and potential (WITHOUT training focus recommendations)."""
    
    if not profile.personal_bests:
        return {"level": "No evaluado", "notes": "Sin datos de rendimiento disponibles"}
    
    # Performance indicators
    has_5k = bool(profile.personal_bests.get("5k"))
    has_10k = bool(profile.personal_bests.get("10k"))
    has_half = bool(profile.personal_bests.get("half_marathon"))
    has_marathon = bool(profile.personal_bests.get("marathon"))
    
    race_experience = sum([has_5k, has_10k, has_half, has_marathon])
    
    analysis = {
        "race_experience_breadth": f"{race_experience}/4 distancias registradas",
        "specialization_tendency": _identify_specialization(profile.personal_bests),
        "improvement_potential": _assess_improvement_potential(profile)
    }
    
    return analysis

# Analysis Helper Functions (kept minimal and descriptive only)

def _calculate_pace_from_time(time_str: str, distance_km: float) -> str:
    """Calculate pace from time string and distance."""
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        else:
            return "N/A"
        
        pace_seconds = total_seconds / distance_km
        pace_minutes = int(pace_seconds // 60)
        pace_seconds = int(pace_seconds % 60)
        
        return f"{pace_minutes:02d}:{pace_seconds:02d}/km"
    except:
        return "N/A"

def _calculate_weeks_until_race(race_date: str) -> Optional[int]:
    """Calculate weeks between now and race date."""
    try:
        from datetime import datetime
        race_dt = datetime.strptime(race_date, "%Y-%m-%d")
        now = datetime.now()
        delta = race_dt - now
        weeks = delta.days // 7
        return max(0, weeks)
    except:
        return None

def _assess_performance_level(distance_key: str, time: str, age: int, gender: str) -> str:
    """Assess performance level for a given distance."""
    return "Nivel competitivo a evaluar con estándares por edad y género"

def _assess_goal_feasibility(profile: AthleteProfile) -> str:
    """Assess feasibility of main goal."""
    if not profile.main_objective:
        return "Sin objetivo principal definido"
    
    return "Factibilidad a evaluar basada en datos actuales y tiempo disponible"

def _analyze_injury_patterns(injuries: List[Injury]) -> Dict[str, Any]:
    """Analyze injury patterns for prevention strategy."""
    if not injuries:
        return {}
    
    patterns = {
        "total_injuries": len(injuries),
        "recurring_areas": _identify_recurring_areas(injuries),
        "chronicity_risk": _assess_chronicity_risk(injuries)
    }
    
    return patterns

# Additional helper functions (simplified versions - descriptive only)

def _determine_readiness_level(completeness: float) -> str:
    """Determine readiness level for training plan generation."""
    if completeness >= 80:
        return "Óptimo - datos suficientes para plan altamente personalizado"
    elif completeness >= 60:
        return "Bueno - datos adecuados para plan personalizado estándar"
    elif completeness >= 40:
        return "Básico - plan general con adaptaciones limitadas"
    else:
        return "Insuficiente - completar más secciones para mejor personalización"

def _identify_specialization(personal_bests: Dict[str, str]) -> str:
    """Identify athlete's distance specialization tendency."""
    return "Análisis de especialización basado en ratios de rendimiento entre distancias"

def _assess_improvement_potential(profile: AthleteProfile) -> str:
    """Assess improvement potential based on current metrics."""
    return "Potencial de mejora a evaluar basado en métricas actuales y objetivos"

def _identify_recurring_areas(injuries: List[Injury]) -> List[str]:
    """Identify anatomical areas with recurring injuries."""
    return ["Análisis de patrones anatómicos en desarrollo"]

def _assess_chronicity_risk(injuries: List[Injury]) -> str:
    """Assess risk of chronic issues."""
    return "Evaluación de riesgo de cronicidad basada en historial"

def _determine_race_purpose(race: Race, main_objective: Optional[Race]) -> str:
    """Determine strategic purpose of intermediate race."""
    if not main_objective:
        return "Objetivo independiente"
    
    return "Preparación estratégica para objetivo principal"

def _analyze_goal_structure(profile: AthleteProfile) -> str:
    """Analyze overall goal structure and coherence."""
    if not profile.main_objective:
        return "Sin estructura de objetivos definida"
    
    return "Análisis de coherencia y viabilidad de estructura de objetivos"