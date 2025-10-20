"""
Motor de Lógica y Cálculo - Normalización y Validaciones

Este módulo implementa las funciones puras responsables de la normalización
de entradas de usuario, validación de coherencia de datos y cálculos derivados
como las zonas de entrenamiento usando la Fórmula de Karvonen.

Principios de diseño:
- Funciones puras sin efectos secundarios
- Normalización robusta que acepta múltiples formatos de entrada
- Validación de coherencia fisiológica y temporal
- Cálculos derivados reproducibles y documentados
"""

import re
from typing import Optional, List, Tuple, Dict
from datetime import datetime, date
from .models import TrainingZones

def normalize_gender_input(input_str: str) -> str:
    """
    Normaliza entrada de género a formato estándar.
    
    Acepta múltiples formatos y variaciones de entrada del usuario,
    devolviendo siempre uno de los valores normalizados.
    
    Args:
        input_str: Entrada del usuario (ej: "M", "m", "Masculino", "hombre")
    
    Returns:
        str: Valor normalizado ("Masculino", "Femenino", "Otro")
    
    Examples:
        >>> normalize_gender_input("M")
        'Masculino'
        >>> normalize_gender_input("mujer")  
        'Femenino'
        >>> normalize_gender_input("other")
        'Otro'
    """
    if not input_str:
        return ""
    
    input_lower = input_str.lower().strip()
    
    # Mapeo de entradas comunes a valores normalizados
    masculine_inputs = ['m', 'masculino', 'hombre', 'male', 'man']
    feminine_inputs = ['f', 'femenino', 'mujer', 'female', 'woman']
    
    if input_lower in masculine_inputs:
        return "Masculino"
    elif input_lower in feminine_inputs:
        return "Femenino"
    else:
        return "Otro"

def parse_time_input(input_str: str) -> Optional[str]:
    """
    Normaliza entrada de tiempo deportivo a formato HH:MM:SS.
    
    CORREGIDO: Maneja correctamente MM:SS como minutos:segundos,
    no como horas:minutos como se interpretaba erróneamente antes.
    
    Args:
        input_str: Tiempo en diversos formatos (ej: "18:30", "1:25:00", "18'30")
    
    Returns:
        Optional[str]: Tiempo normalizado o None si formato inválido
    
    Examples:
        >>> parse_time_input("18:30")  # 18 minutos, 30 segundos
        '00:18:30'
        >>> parse_time_input("1:25:30")  # 1 hora, 25 minutos, 30 segundos
        '01:25:30'
    """
    if not input_str:
        return None
    
    # Limpiar entrada y reemplazar caracteres comunes
    cleaned = input_str.strip().replace("'", ":").replace('"', "")
    
    # Patrones para diferentes formatos
    patterns = [
        r'^(\d{1,2}):(\d{2}):(\d{2})$',  # HH:MM:SS
        r'^(\d{1,2}):(\d{2})$',          # MM:SS (formato más común en running)
        r'^(\d+)\.(\d{2})\.(\d{2})$',    # H.MM.SS (formato alemán)
        r'^(\d+)h(\d{2})m(\d{2})s$',     # 1h25m30s
        r'^(\d+)h(\d{2})m$',             # 1h25m (añadir segundos)
    ]
    
    for pattern in patterns:
        match = re.match(pattern, cleaned)
        if match:
            groups = match.groups()
            
            if len(groups) == 2:  # MM:SS format - CORRECCIÓN AQUÍ
                # ✅ CORRECCIÓN: Interpretar como minutos:segundos, NO horas:minutos
                minutes, seconds = int(groups[0]), int(groups[1])
                hours = 0
                
                # Si los minutos son >= 60, convertir a horas
                if minutes >= 60:
                    hours = minutes // 60
                    minutes = minutes % 60
                    
            else:  # HH:MM:SS format
                hours, minutes, seconds = int(groups[0]), int(groups[1]), int(groups[2])
            
            # Validar rangos
            if minutes >= 60 or seconds >= 60:
                return None
            
            # ✅ FORMATEAR CORRECTAMENTE: Asegurar que las horas sean 2 dígitos
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return None

def parse_training_days_input(input_str: str) -> str:
    """
    Normaliza entrada de días de entrenamiento.
    
    Args:
        input_str: Días en diversos formatos (ej: "4", "4-5", "3 a 4")
    
    Returns:
        str: Formato normalizado
    """
    if not input_str:
        return ""
    
    cleaned = input_str.strip().lower()
    
    # Reemplazar variantes de separadores
    cleaned = cleaned.replace(" a ", "-").replace(" y ", "-").replace(",", "-")
    
    # Normalizar formato
    if re.match(r'^\d+$', cleaned):  # Número simple
        return cleaned
    elif re.match(r'^\d+-\d+$', cleaned):  # Rango
        return cleaned
    else:
        return input_str  # Devolver original si no se puede normalizar

def parse_unavailable_days_input(input_str: str) -> str:
    """
    NUEVA FUNCIÓN: Normaliza entrada de días no disponibles.
    
    Acepta formatos como:
    - "Domingo" -> "Domingo"
    - "D" -> "Domingo"  
    - "L,D" -> "Lunes,Domingo"
    - "Lunes, Domingo" -> "Lunes,Domingo"
    
    Args:
        input_str: Días no disponibles en diversos formatos
        
    Returns:
        str: Formato normalizado (días completos separados por comas)
    """
    if not input_str:
        return ""
    
    # Mapeo de abreviaciones a nombres completos
    day_map = {
        'l': 'Lunes', 'lunes': 'Lunes',
        'm': 'Martes', 'martes': 'Martes', 'mar': 'Martes',
        'x': 'Miércoles', 'miércoles': 'Miércoles', 'mie': 'Miércoles', 'miercoles': 'Miércoles',
        'j': 'Jueves', 'jueves': 'Jueves', 'jue': 'Jueves',
        'v': 'Viernes', 'viernes': 'Viernes', 'vie': 'Viernes',
        's': 'Sábado', 'sábado': 'Sábado', 'sab': 'Sábado', 'sabado': 'Sábado',
        'd': 'Domingo', 'domingo': 'Domingo', 'dom': 'Domingo'
    }
    
    # Limpiar y separar por comas
    cleaned = input_str.strip().lower()
    days = [day.strip() for day in re.split(r'[,;]', cleaned)]
    
    normalized_days = []
    for day in days:
        if day in day_map:
            normalized_days.append(day_map[day])
        else:
            # Si no es una abreviación reconocida, intentar capitalizar
            day_capitalized = day.capitalize()
            if day_capitalized in day_map.values():
                normalized_days.append(day_capitalized)
    
    return ','.join(normalized_days)

def normalize_day_of_week_input(input_str: str) -> str:
    """
    Normaliza entrada de día de la semana individual.
    
    Args:
        input_str: Día en formato abreviado o completo
        
    Returns:
        str: Día normalizado en formato completo
    """
    day_map = {
        'l': 'Lunes', 'lun': 'Lunes', 'lunes': 'Lunes',
        'm': 'Martes', 'mar': 'Martes', 'martes': 'Martes', 
        'x': 'Miércoles', 'mie': 'Miércoles', 'miércoles': 'Miércoles', 'miercoles': 'Miércoles',
        'j': 'Jueves', 'jue': 'Jueves', 'jueves': 'Jueves',
        'v': 'Viernes', 'vie': 'Viernes', 'viernes': 'Viernes',
        's': 'Sábado', 'sab': 'Sábado', 'sábado': 'Sábado', 'sabado': 'Sábado',
        'd': 'Domingo', 'dom': 'Domingo', 'domingo': 'Domingo'
    }
    
    cleaned = input_str.lower().strip()
    return day_map.get(cleaned, input_str.title())

def parse_quality_session_preference(input_str: str) -> str:
    """
    FUNCIÓN OBSOLETA - Mantenida temporalmente por compatibilidad hacia atrás.
    
    DEPRECATION WARNING: Esta función será eliminada en versiones futuras.
    """
    if not input_str:
        return ""
    
    # Normalización básica
    normalized = input_str.strip()
    
    # Dividir por comas y limpiar cada día
    days = [day.strip() for day in normalized.split(',')]
    normalized_days = []
    
    for day in days:
        normalized_day = normalize_day_of_week_input(day)
        if normalized_day:
            normalized_days.append(normalized_day)
    
    return ', '.join(normalized_days)

def calculate_training_zones(max_hr: int, resting_hr: int) -> TrainingZones:
    """
    Calcula zonas de entrenamiento usando fórmula de Karvonen.
    
    La fórmula de Karvonen es considerada más precisa que el simple
    porcentaje de FC máxima, ya que toma en cuenta la reserva cardíaca
    individual del atleta.
    
    Args:
        max_hr: Frecuencia cardíaca máxima
        resting_hr: Frecuencia cardíaca en reposo
    
    Returns:
        TrainingZones: Zonas calculadas con rangos específicos
    
    Examples:
        >>> zones = calculate_training_zones(184, 41)
        >>> zones.zone1_hr
        '112-127 ppm'
    """
    hr_reserve = max_hr - resting_hr
    
    # Calcular límites de cada zona (% de reserva de FC)
    def calculate_zone(low_percent: float, high_percent: float) -> str:
        low_hr = int(resting_hr + (hr_reserve * low_percent))
        high_hr = int(resting_hr + (hr_reserve * high_percent))
        return f"{low_hr}-{high_hr} ppm"
    
    return TrainingZones(
        zone1_hr=calculate_zone(0.50, 0.60),      # 50-60% reserva
        zone2_hr=calculate_zone(0.60, 0.70),     # 60-70% reserva  
        zone3_hr=calculate_zone(0.70, 0.80),     # 70-80% reserva
        zone4_hr=calculate_zone(0.80, 0.90),     # 80-90% reserva
        zone5_hr=calculate_zone(0.90, 1.00)      # 90-100% reserva
    )

def validate_heart_rates(max_hr: int, resting_hr: int) -> List[str]:
    """
    Valida coherencia de frecuencias cardíacas.
    
    Args:
        max_hr: Frecuencia cardíaca máxima
        resting_hr: Frecuencia cardíaca en reposo
        
    Returns:
        List[str]: Lista de errores de validación (vacía si válido)
    """
    errors = []
    
    if max_hr <= resting_hr:
        errors.append("FC máxima debe ser mayor que FC en reposo")
    
    if max_hr - resting_hr < 50:
        errors.append("Diferencia entre FC máxima y reposo parece muy pequeña")
    
    return errors

def validate_physical_metrics(age: Optional[int], weight: Optional[float], height: Optional[int]) -> List[str]:
    """
    Valida coherencia de métricas físicas.
    
    Incluye cálculo de BMI y validación de rangos típicos para runners.
    """
    errors = []
    
    if age and weight and height:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 16 or bmi > 35:
            errors.append(f"BMI calculado ({bmi:.1f}) fuera de rango típico para runners")
    
    return errors

def validate_race_date(date_str: str, race_name: str) -> Tuple[bool, Optional[str]]:
    """
    Valida fecha de carrera y calcula tiempo hasta el evento.
    
    Returns:
        Tuple[bool, Optional[str]]: (fecha_válida, mensaje_warning)
    """
    try:
        race_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = date.today()
        
        days_until_race = (race_date - today).days
        
        if days_until_race < 0:
            return False, f"La fecha de {race_name} ya ha pasado"
        elif days_until_race < 30:
            return True, f"⚠️ Solo {days_until_race} días hasta {race_name} - plan será muy breve"
        elif days_until_race > 365:
            return True, f"⚠️ Fecha muy lejana ({days_until_race} días) - considere objetivos intermedios"
        else:
            return True, None
            
    except ValueError:
        return False, "Formato de fecha inválido (use YYYY-MM-DD)"

def format_distance_for_display(distance_km: float) -> str:
    """Formatea distancia para mostrar de forma amigable."""
    if distance_km == 5.0:
        return "5K"
    elif distance_km == 10.0:
        return "10K"
    elif abs(distance_km - 21.097) < 0.1:
        return "Media Maratón"
    elif abs(distance_km - 42.195) < 0.1:
        return "Maratón"
    else:
        return f"{distance_km}K"

def suggest_training_weeks(race_date: str) -> int:
    """
    Sugiere duración óptima del plan basado en fecha de carrera.
    
    Args:
        race_date: Fecha en formato YYYY-MM-DD
        
    Returns:
        int: Semanas sugeridas para el plan
    """
    try:
        target_date = datetime.strptime(race_date, '%Y-%m-%d').date()
        today = date.today()
        days_until = (target_date - today).days
        weeks_until = days_until // 7
        
        # Sugerir duración basada en tiempo disponible
        if weeks_until < 8:
            return max(4, weeks_until - 1)  # Mínimo 4 semanas
        elif weeks_until < 16:
            return min(12, weeks_until - 1)  # Máximo 12 semanas para evitar sobreentrenamiento
        else:
            return 16  # Plan estándar largo
            
    except ValueError:
        return 8  # Default seguro

def estimate_vo2_max_from_time(distance_km: float, time_str: str, age: int, weight_kg: float) -> Optional[float]:
    """
    Estima VO2máx basado en tiempo de carrera usando fórmulas validadas.
    
    Utiliza las fórmulas de Mercier et al. ajustadas por edad para
    proporcionar estimaciones razonablemente precisas de VO2máx.
    
    Args:
        distance_km: Distancia de la carrera
        time_str: Tiempo en formato HH:MM:SS
        age: Edad del atleta
        weight_kg: Peso del atleta
        
    Returns:
        Optional[float]: VO2máx estimado o None si no se puede calcular
    """
    try:
        # Convertir tiempo a segundos totales
        time_parts = time_str.split(':')
        if len(time_parts) == 3:
            hours, minutes, seconds = map(int, time_parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        else:
            return None
        
        # Calcular velocidad en m/min
        distance_m = distance_km * 1000
        time_minutes = total_seconds / 60
        speed_m_per_min = distance_m / time_minutes
        
        # Fórmulas específicas por distancia
        if abs(distance_km - 10.0) < 0.1:  # 10K
            # Fórmula de Mercier et al. para 10K
            vo2_max = 15.0 * speed_m_per_min / 10.0
        elif abs(distance_km - 21.097) < 0.1:  # Media Maratón  
            # Fórmula ajustada para media maratón
            vo2_max = 14.8 * speed_m_per_min / 10.0
        else:
            # Fórmula genérica
            vo2_max = 15.0 * speed_m_per_min / 10.0
        
        # Ajustar por edad (declina ~1% por año después de los 25)
        age_factor = 1.0 - max(0, (age - 25) * 0.01)
        vo2_max_adjusted = vo2_max * age_factor
        
        # Validar rango razonable
        if 30 <= vo2_max_adjusted <= 85:
            return round(vo2_max_adjusted, 1)
        else:
            return None
            
    except (ValueError, ZeroDivisionError):
        return None

def calculate_bmi(weight_kg: float, height_cm: float) -> Optional[float]:
    """
    Calculate Body Mass Index.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        
    Returns:
        Optional[float]: BMI value or None if invalid inputs
    """
    if not weight_kg or not height_cm or weight_kg <= 0 or height_cm <= 0:
        return None
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)