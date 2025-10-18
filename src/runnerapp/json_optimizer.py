"""
JSON AI Optimization Module

This module specializes in transforming the AthleteProfile data model
into an AI-optimized JSON structure. The output is designed as a
high-quality structured prompt that maximizes AI comprehension and
generates better training plan responses.

Key optimizations:
- Descriptive keys with contextual meaning
- Metadata descriptions guiding AI interpretation  
- Logical data nesting and grouping
- Self-explanatory structure reducing ambiguity
- Optimized field ordering for AI processing
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
    prompt that provides maximum context and clarity to AI systems.
    
    Args:
        profile: Complete athlete profile data
    
    Returns:
        Dict[str, Any]: AI-optimized data structure
    """
    
    # Calculate derived metrics
    bmi = None
    if profile.weight_kg and profile.height_cm:
        bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
    
    # Build optimized structure
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
            "bmi": bmi,
            "anthropometric_notes": _generate_anthropometric_notes(profile, bmi)
        },
        
        "physiological_metrics": _build_physiological_section(profile),
        "training_context": _build_training_context_section(profile),
        "performance_data": _build_performance_section(profile),
        "race_goals": _build_race_goals_section(profile),
        "injury_history": _build_injury_history_section(profile),
        "ai_guidance": _build_ai_guidance_section(profile)
    }
    
    return ai_data


def _build_physiological_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build physiological metrics section for AI."""
    
    section = {
        "meta_description": "Métricas fisiológicas clave que definen el perfil de resistencia y el potencial aeróbico del atleta. Estos datos son fundamentales para establecer zonas de entrenamiento precisas y adaptar la intensidad del plan.",
        "max_hr": profile.max_hr,
        "resting_hr": profile.resting_hr,
        "vo2_max": profile.vo2_max,
        "lactate_threshold_bpm": profile.lactate_threshold_bpm,
        "hrv_ms": profile.hrv_ms,
        "training_zones": None,
        "physiological_profile": _analyze_physiological_profile(profile)
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


def _build_training_context_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build training context section for AI."""
    
    return {
        "meta_description": "Contexto actual de entrenamiento del atleta, incluyendo carga de trabajo, disponibilidad temporal y preferencias específicas. Esta información es crucial para adaptar el volumen, frecuencia y distribución de entrenamientos.",
        "current_training_load": {
            "avg_weekly_km": profile.avg_weekly_km,
            "training_days_per_week": profile.training_days_per_week,
            "load_assessment": _assess_current_load(profile)
        },
        "strength_training": {
            "history": profile.strength_training_history,
            "include_in_plan": profile.include_strength_training,
            "integration_notes": _generate_strength_notes(profile)
        },
        "scheduling_preferences": {
            "quality_session_preference": profile.quality_session_preference,
            "scheduling_flexibility": _assess_scheduling_flexibility(profile)
        },
        "training_readiness": _assess_training_readiness(profile)
    }


def _build_performance_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build performance data section for AI."""
    
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
        
        # Overall performance analysis
        section["performance_analysis"] = _analyze_overall_performance(profile)
    
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
    """Build injury history section for AI."""
    
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
                "recovery_desc": injury.recovery_desc,
                "risk_category": _categorize_injury_risk(injury.type),
                "prevention_focus": _suggest_prevention_focus(injury.type)
            })
        
        section["injury_analysis"] = _analyze_injury_patterns(profile.injuries)
    else:
        section["injury_analysis"] = "Sin lesiones registradas - Perfil de bajo riesgo para adaptaciones estándar de entrenamiento."
    
    return section


def _build_ai_guidance_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build AI-specific guidance and context."""
    
    return {
        "meta_description": "Guías específicas para el sistema de IA sobre cómo interpretar y utilizar esta ficha técnica para generar un plan de entrenamiento óptimo.",
        "profile_strength_areas": _identify_profile_strengths(profile),
        "profile_development_areas": _identify_development_areas(profile),
        "training_plan_priorities": _determine_training_priorities(profile),
        "special_considerations": _identify_special_considerations(profile),
        "recommended_plan_duration": _recommend_plan_duration(profile),
        "risk_mitigation_focus": _identify_risk_factors(profile)
    }


# Helper Functions for Analysis and Calculations

def _calculate_profile_completeness(profile: AthleteProfile) -> Dict[str, Any]:
    """Calculate profile completeness metrics."""
    total_fields = 0
    completed_fields = 0
    
    # Core fields (weighted more heavily)
    core_fields = [
        profile.name, profile.age, profile.gender,
        profile.max_hr, profile.resting_hr,
        profile.avg_weekly_km, profile.training_days_per_week,
        profile.main_objective
    ]
    
    for field in core_fields:
        total_fields += 2  # Core fields count double
        if field:
            completed_fields += 2
    
    # Optional fields
    optional_fields = [
        profile.height_cm, profile.weight_kg, profile.vo2_max,
        profile.lactate_threshold_bpm, profile.hrv_ms,
        profile.strength_training_history, profile.include_strength_training,
        profile.quality_session_preference
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


def _generate_anthropometric_notes(profile: AthleteProfile, bmi: Optional[float]) -> str:
    """Generate anthropometric analysis notes."""
    notes = []
    
    if bmi:
        if bmi < 18.5:
            notes.append("BMI bajo - considerar análisis nutricional")
        elif 18.5 <= bmi < 25:
            notes.append("BMI óptimo para corredor de resistencia")
        elif 25 <= bmi < 30:
            notes.append("BMI elevado - posible enfoque en composición corporal")
        else:
            notes.append("BMI alto - evaluación médica recomendada")
    
    if profile.height_cm and profile.age:
        if profile.height_cm > 185:
            notes.append("Altura elevada - ventajas en zancada, atención a eficiencia")
        elif profile.height_cm < 165:
            notes.append("Estatura menor - ventajas en agilidad y recuperación")
    
    return " | ".join(notes) if notes else "Datos antropométricos dentro de rangos normales"


def _analyze_physiological_profile(profile: AthleteProfile) -> str:
    """Analyze physiological profile and provide insights."""
    insights = []
    
    if profile.max_hr and profile.resting_hr:
        hr_reserve = profile.max_hr - profile.resting_hr
        if hr_reserve > 160:
            insights.append("Excelente reserva cardíaca para entrenamiento de alta intensidad")
        elif hr_reserve < 120:
            insights.append("Reserva cardíaca limitada - enfocar en desarrollo aeróbico gradual")
        
        if profile.resting_hr < 50:
            insights.append("FC reposo muy baja - indicador de excelente adaptación aeróbica")
        elif profile.resting_hr > 70:
            insights.append("FC reposo elevada - oportunidad de mejora en base aeróbica")
    
    if profile.vo2_max:
        if profile.gender == "Masculino":
            if profile.vo2_max > 60:
                insights.append("VO2máx excepcional - potencial para alto rendimiento")
            elif profile.vo2_max < 40:
                insights.append("VO2máx bajo - gran margen de mejora con entrenamiento estructurado")
        else:  # Femenino
            if profile.vo2_max > 50:
                insights.append("VO2máx excepcional - potencial para alto rendimiento")
            elif profile.vo2_max < 35:
                insights.append("VO2máx bajo - gran margen de mejora con entrenamiento estructurado")
    
    return " | ".join(insights) if insights else "Perfil fisiológico dentro de parámetros esperados"


def _assess_current_load(profile: AthleteProfile) -> str:
    """Assess current training load."""
    if not profile.avg_weekly_km:
        return "Carga actual no especificada - iniciar con volumen conservador"
    
    weekly_km = profile.avg_weekly_km
    
    if weekly_km < 20:
        return "Volumen bajo - corredor principiante o en retorno al entrenamiento"
    elif weekly_km < 40:
        return "Volumen moderado - base sólida para desarrollo progresivo"
    elif weekly_km < 60:
        return "Volumen alto - atleta experimentado con buena base aeróbica"
    elif weekly_km < 80:
        return "Volumen muy alto - corredor avanzado, atención a recuperación"
    else:
        return "Volumen elite - atleta de alto rendimiento, periodización crítica"


def _generate_strength_notes(profile: AthleteProfile) -> str:
    """Generate strength training integration notes."""
    if profile.strength_training_history is None:
        return "Historial de fuerza no especificado"
    
    if profile.include_strength_training is None:
        return "Preferencia de inclusión no especificada"
    
    if profile.strength_training_history and profile.include_strength_training:
        return "Atleta experimentado - integrar 2-3 sesiones/semana con periodización específica"
    elif not profile.strength_training_history and profile.include_strength_training:
        return "Principiante en fuerza - comenzar con 1-2 sesiones/semana, énfasis en técnica"
    elif profile.strength_training_history and not profile.include_strength_training:
        return "Experiencia previa pero no desea incluir - considerar trabajo correctivo mínimo"
    else:
        return "Sin fuerza - enfoque 100% en desarrollo aeróbico y técnica de carrera"


def _assess_scheduling_flexibility(profile: AthleteProfile) -> str:
    """Assess scheduling flexibility."""
    if not profile.training_days_per_week:
        return "Disponibilidad no especificada"
    
    days = profile.training_days_per_week
    
    if isinstance(days, str) and '-' in days:
        return f"Flexibilidad alta - rango de {days} permite adaptación semanal"
    else:
        try:
            day_count = int(days)
            if day_count <= 3:
                return "Disponibilidad limitada - maximizar calidad sobre cantidad"
            elif day_count <= 5:
                return "Disponibilidad estándar - equilibrio óptimo intensidad/volumen"
            else:
                return "Alta disponibilidad - oportunidad para volumen elevado"
        except:
            return "Formato de disponibilidad no estándar"


def _assess_training_readiness(profile: AthleteProfile) -> Dict[str, str]:
    """Assess overall training readiness."""
    readiness = {
        "physiological": "No evaluado",
        "experience": "No evaluado", 
        "injury_risk": "No evaluado",
        "goal_alignment": "No evaluado"
    }
    
    # Physiological readiness
    if profile.max_hr and profile.resting_hr:
        hr_quality = "Excelente" if profile.resting_hr < 60 else "Buena"
        readiness["physiological"] = f"{hr_quality} base para entrenamiento estructurado"
    
    # Experience level
    if profile.avg_weekly_km:
        if profile.avg_weekly_km > 40:
            readiness["experience"] = "Experiencia sólida - apto para entrenamiento avanzado"
        elif profile.avg_weekly_km > 20:
            readiness["experience"] = "Experiencia moderada - progresión gradual recomendada"
        else:
            readiness["experience"] = "Principiante - enfoque en construcción de base"
    
    # Injury risk assessment
    if profile.injuries:
        high_risk_injuries = [inj for inj in profile.injuries 
                            if any(risk in inj.type.lower() 
                                 for risk in ['fascitis', 'tendinitis', 'fractura', 'ligamento'])]
        if high_risk_injuries:
            readiness["injury_risk"] = "Riesgo elevado - adaptaciones preventivas necesarias"
        else:
            readiness["injury_risk"] = "Riesgo moderado - precauciones estándar"
    else:
        readiness["injury_risk"] = "Riesgo bajo - sin restricciones aparentes"
    
    # Goal alignment
    if profile.main_objective:
        weeks_available = _calculate_weeks_until_race(profile.main_objective.date)
        if weeks_available and weeks_available > 12:
            readiness["goal_alignment"] = "Tiempo suficiente para preparación óptima"
        elif weeks_available and weeks_available > 6:
            readiness["goal_alignment"] = "Tiempo limitado - planificación intensiva necesaria"
        else:
            readiness["goal_alignment"] = "Tiempo muy limitado - objetivos de mantenimiento"
    
    return readiness


def _analyze_overall_performance(profile: AthleteProfile) -> Dict[str, Any]:
    """Analyze overall performance level and potential."""
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
        "improvement_potential": _assess_improvement_potential(profile),
        "training_focus_recommendation": _recommend_training_focus(profile)
    }
    
    return analysis


def _build_ai_guidance_section(profile: AthleteProfile) -> Dict[str, Any]:
    """Build comprehensive AI guidance."""
    
    return {
        "profile_strength_areas": _identify_profile_strengths(profile),
        "profile_development_areas": _identify_development_areas(profile), 
        "training_plan_priorities": _determine_training_priorities(profile),
        "special_considerations": _identify_special_considerations(profile),
        "recommended_plan_duration": _recommend_plan_duration(profile),
        "risk_mitigation_focus": _identify_risk_factors(profile)
    }


# Analysis Helper Functions

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
    # This would contain performance benchmarking logic
    # For now, return a placeholder
    return "Nivel competitivo a evaluar con estándares por edad y género"


def _assess_goal_feasibility(profile: AthleteProfile) -> str:
    """Assess feasibility of main goal."""
    if not profile.main_objective:
        return "Sin objetivo principal definido"
    
    # This would contain goal feasibility analysis
    return "Factibilidad a evaluar basada en datos actuales y tiempo disponible"


def _identify_profile_strengths(profile: AthleteProfile) -> List[str]:
    """Identify athlete's key strengths."""
    strengths = []
    
    if profile.resting_hr and profile.resting_hr < 55:
        strengths.append("Excelente base aeróbica (FC reposo baja)")
    
    if profile.avg_weekly_km and profile.avg_weekly_km > 50:
        strengths.append("Volumen de entrenamiento elevado y consistente")
    
    if profile.personal_bests and len([pb for pb in profile.personal_bests.values() if pb]) >= 3:
        strengths.append("Experiencia competitiva amplia en múltiples distancias")
    
    if not profile.injuries:
        strengths.append("Historial libre de lesiones - bajo riesgo de recurrencia")
    
    return strengths


def _identify_development_areas(profile: AthleteProfile) -> List[str]:
    """Identify areas for development."""
    development_areas = []
    
    if not profile.strength_training_history:
        development_areas.append("Incorporación de entrenamiento de fuerza para prevención de lesiones")
    
    if not profile.personal_bests or len([pb for pb in profile.personal_bests.values() if pb]) < 2:
        development_areas.append("Establecimiento de referencias de rendimiento en múltiples distancias")
    
    if profile.avg_weekly_km and profile.avg_weekly_km < 30:
        development_areas.append("Desarrollo progresivo de volumen de entrenamiento")
    
    return development_areas


def _determine_training_priorities(profile: AthleteProfile) -> List[str]:
    """Determine training priorities based on profile."""
    priorities = []
    
    if profile.main_objective:
        distance = profile.main_objective.distance_km
        if distance >= 42:
            priorities.append("Resistencia aeróbica de larga duración")
            priorities.append("Economía de carrera y gestión energética")
        elif distance >= 21:
            priorities.append("Potencia aeróbica y umbral de lactato")
            priorities.append("Resistencia específica de la distancia")
        elif distance >= 10:
            priorities.append("VO2máx y capacidad aeróbica")
            priorities.append("Tolerancia al lactato")
        else:
            priorities.append("Potencia aeróbica máxima")
            priorities.append("Velocidad y neuromuscular")
    
    return priorities


def _identify_special_considerations(profile: AthleteProfile) -> List[str]:
    """Identify special considerations for training plan."""
    considerations = []
    
    if profile.injuries:
        injury_types = [injury.type.lower() for injury in profile.injuries]
        if any('rodilla' in itype or 'knee' in itype for itype in injury_types):
            considerations.append("Historial de lesión de rodilla - enfoque en fortalecimiento de glúteo y core")
        if any('fascitis' in itype or 'plantar' in itype for itype in injury_types):
            considerations.append("Historial de fascitis plantar - atención a progresión de volumen y calzado")
        if any('aquiles' in itype or 'achilles' in itype for itype in injury_types):
            considerations.append("Historial Aquiles - progresión muy gradual en velocidad e intensidad")
    
    if profile.age and profile.age > 45:
        considerations.append("Atleta máster - mayor énfasis en recuperación y prevención")
    
    if profile.training_days_per_week and int(profile.training_days_per_week.split('-')[0]) <= 3:
        considerations.append("Disponibilidad limitada - maximizar eficiencia de cada sesión")
    
    return considerations


def _recommend_plan_duration(profile: AthleteProfile) -> str:
    """Recommend optimal plan duration."""
    if not profile.main_objective:
        return "Sin objetivo principal - plan de base general recomendado"
    
    weeks_available = _calculate_weeks_until_race(profile.main_objective.date)
    
    if not weeks_available:
        return "Fecha de objetivo no válida - plan de preparación general"
    
    if weeks_available < 6:
        return f"{weeks_available} semanas - Plan de mantenimiento y puesta a punto"
    elif weeks_available < 12:
        return f"{weeks_available} semanas - Plan de desarrollo específico"
    elif weeks_available < 20:
        return f"{weeks_available} semanas - Plan de preparación completa"
    else:
        return f"{weeks_available} semanas - Plan de desarrollo a largo plazo con múltiples fases"


def _identify_risk_factors(profile: AthleteProfile) -> List[str]:
    """Identify risk factors and mitigation strategies."""
    risks = []
    
    if profile.injuries:
        risks.append("Historial de lesiones previas - implementar protocolos de prevención específicos")
    
    if profile.avg_weekly_km and profile.main_objective:
        current_load = profile.avg_weekly_km
        weeks_available = _calculate_weeks_until_race(profile.main_objective.date)
        
        if weeks_available and weeks_available < 8 and current_load < 30:
            risks.append("Base insuficiente para objetivo en tiempo limitado - ajustar expectativas")
    
    if not profile.strength_training_history:
        risks.append("Sin base de fuerza - mayor riesgo de lesiones por desbalances musculares")
    
    if profile.age and profile.age > 40 and profile.avg_weekly_km and profile.avg_weekly_km > 60:
        risks.append("Atleta máster con volumen alto - monitorización estrecha de recuperación")
    
    return risks


# Additional helper functions would continue here following the same pattern...

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
    # This would analyze time ratios between distances to identify strengths
    return "Análisis de especialización basado en ratios de rendimiento entre distancias"


def _assess_improvement_potential(profile: AthleteProfile) -> str:
    """Assess improvement potential based on current metrics."""
    return "Potencial de mejora a evaluar basado en métricas actuales y objetivos"


def _recommend_training_focus(profile: AthleteProfile) -> List[str]:
    """Recommend primary training focus areas."""
    focuses = ["Desarrollo aeróbico base", "Eficiencia de movimiento"]
    
    if profile.main_objective and profile.main_objective.distance_km >= 21:
        focuses.append("Resistencia específica de distancia")
    
    return focuses


def _categorize_injury_risk(injury_type: str) -> str:
    """Categorize injury risk level."""
    high_risk = ['fascitis', 'aquiles', 'fractura', 'ligamento']
    if any(risk in injury_type.lower() for risk in high_risk):
        return "Alto riesgo de recurrencia"
    else:
        return "Riesgo moderado"


def _suggest_prevention_focus(injury_type: str) -> str:
    """Suggest prevention focus for injury type."""
    injury_lower = injury_type.lower()
    
    if 'fascitis' in injury_lower:
        return "Fortalecimiento de pie y pantorrilla, progresión gradual de volumen"
    elif 'aquiles' in injury_lower:
        return "Trabajo excéntrico de pantorrilla, calentamiento específico"
    elif 'rodilla' in injury_lower or 'knee' in injury_lower:
        return "Fortalecimiento de glúteo y core, análisis de pisada"
    elif 'espalda' in injury_lower or 'lumbar' in injury_lower:
        return "Core stability y técnica de carrera"
    else:
        return "Prevención general y fortalecimiento funcional"


def _analyze_injury_patterns(injuries: List[Injury]) -> Dict[str, Any]:
    """Analyze injury patterns for prevention strategy."""
    if not injuries:
        return {}
    
    patterns = {
        "total_injuries": len(injuries),
        "recurring_areas": _identify_recurring_areas(injuries),
        "chronicity_risk": _assess_chronicity_risk(injuries),
        "prevention_strategy": _develop_prevention_strategy(injuries)
    }
    
    return patterns


def _identify_recurring_areas(injuries: List[Injury]) -> List[str]:
    """Identify anatomical areas with recurring injuries."""
    # This would analyze injury locations for patterns
    return ["Análisis de patrones anatómicos en desarrollo"]


def _assess_chronicity_risk(injuries: List[Injury]) -> str:
    """Assess risk of chronic issues."""
    return "Evaluación de riesgo de cronicidad basada en historial"


def _develop_prevention_strategy(injuries: List[Injury]) -> List[str]:
    """Develop injury prevention strategy."""
    return ["Estrategia de prevención específica basada en patrones identificados"]


def _determine_race_purpose(race: Race, main_objective: Optional[Race]) -> str:
    """Determine strategic purpose of intermediate race."""
    if not main_objective:
        return "Objetivo independiente"
    
    # This would analyze race timing and distance relative to main goal
    return "Preparación estratégica para objetivo principal"


def _analyze_goal_structure(profile: AthleteProfile) -> str:
    """Analyze overall goal structure and coherence."""
    if not profile.main_objective:
        return "Sin estructura de objetivos definida"
    
    return "Análisis de coherencia y viabilidad de estructura de objetivos"
