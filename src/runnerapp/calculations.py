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
    """
    if not input_str:
        return ""
    
    # Convertir a minúsculas para comparación
    normalized_input = input_str.strip().lower()
    
    # Mapeo de variaciones a valores estándar
    male_variations = {
        'm', 'male', 'masculino', 'hombre', 'man', 'varón', 'varon'
    }
    
    female_variations = {
        'f', 'female', 'femenino', 'mujer', 'woman', 'fem'
    }
    
    if normalized_input in male_variations:
        return "Masculino"
    elif normalized_input in female_variations:
        return "Femenino"
    else:
        return "Otro"


def normalize_day_of_week_input(input_str: str) -> str:
    """
    Normaliza entrada de día de semana a formato completo.
    
    Args:
        input_str: Entrada del usuario (ej: "L", "lun", "Lunes")
    
    Returns:
        str: Día completo en español ("Lunes", "Martes", etc.)
    
    Examples:
        >>> normalize_day_of_week_input("L")
        'Lunes'
        >>> normalize_day_of_week_input("mier")
        'Miércoles'
    """
    if not input_str:
        return ""
    
    normalized_input = input_str.strip().lower()
    
    # Mapeo de abreviaciones y variaciones
    day_mapping = {
        'l': 'Lunes', 'lun': 'Lunes', 'lunes': 'Lunes',
        'm': 'Martes', 'mar': 'Martes', 'martes': 'Martes',
        'x': 'Miércoles', 'mie': 'Miércoles', 'mier': 'Miércoles', 
        'miércoles': 'Miércoles', 'miercoles': 'Miércoles',
        'j': 'Jueves', 'jue': 'Jueves', 'jueves': 'Jueves',
        'v': 'Viernes', 'vie': 'Viernes', 'viernes': 'Viernes',
        's': 'Sábado', 'sab': 'Sábado', 'sábado': 'Sábado', 'sabado': 'Sábado',
        'd': 'Domingo', 'dom': 'Domingo', 'domingo': 'Domingo'
    }
    
    return day_mapping.get(normalized_input, input_str.strip())


def parse_training_days_input(input_str: str) -> str:
    """
    Normaliza y valida entrada de días de entrenamiento.
    
    Acepta formatos como "4", "4-5", "3 a 4", validando coherencia.
    
    Args:
        input_str: Entrada del usuario
    
    Returns:
        str: Formato normalizado o entrada original si no se reconoce
    
    Examples:
        >>> parse_training_days_input("4-5")
        '4-5'
        >>> parse_training_days_input("3 a 4")
        '3-4'
    """
    if not input_str:
        return ""
    
    # Limpiar entrada
    cleaned = input_str.strip().lower()
    
    # Patrón para rangos: "3-4", "3 a 4", "3 - 4"
    range_pattern = r'^(\d+)\s*[-a]\s*(\d+)$'
    range_match = re.match(range_pattern, cleaned)
    
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        
        # Validar coherencia del rango
        if start > end:
            start, end = end, start  # Intercambiar si están al revés
        
        if start < 1 or end > 7:
            return input_str.strip()  # Devolver original si fuera de rango
        
        return f"{start}-{end}"
    
    # Patrón para número simple
    single_pattern = r'^(\d+)$'
    single_match = re.match(single_pattern, cleaned)
    
    if single_match:
        days = int(single_match.group(1))
        if 1 <= days <= 7:
            return str(days)
    
    return input_str.strip()  # Devolver entrada original si no se reconoce


def parse_time_input(input_str: str) -> Optional[str]:
    """
    Normaliza entrada de tiempo deportivo a formato HH:MM:SS.
    
    CORREGIDO: Maneja correctamente MM:SS como minutos:segundos,
    no como horas:minutos.
    
    Args:
        input_str: Tiempo en diversos formatos (ej: "18:30", "1:25:00", "18'30")
    
    Returns:
        Optional[str]: Tiempo normalizado o None si formato inválido
    
    Examples:
        >>> parse_time_input("18:30")  # 18 minutos, 30 segundos
        '00:18:30'
        >>> parse_time_input("1:25:30")  # 1 hora, 25 minutos, 30 segundos
        '01:25:30'
        >>> parse_time_input("10:00")  # 10 minutos, 0 segundos
        '00:10:00'
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


def parse_quality_session_preference(input_str: str) -> str:
    """
    Normaliza preferencias de días para sesiones de calidad.
    
    Args:
        input_str: Entrada con días separados por comas o espacios
    
    Returns:
        str: Días normalizados separados por comas
    
    Examples:
        >>> parse_quality_session_preference("mar, jue")
        'Martes, Jueves'
    """
    if not input_str or input_str.strip().lower() in ['ninguna', 'sin preferencia', 'no']:
        return "Sin preferencia"
    
    # Dividir por comas, espacios o "y"
    separators = [',', ' y ', ' e ', ';']
    days_list = [input_str]
    
    for sep in separators:
        new_list = []
        for item in days_list:
            new_list.extend(item.split(sep))
        days_list = new_list
    
    # Normalizar cada día
    normalized_days = []
    for day in days_list:
        normalized_day = normalize_day_of_week_input(day.strip())
        if normalized_day and normalized_day not in normalized_days:
            normalized_days.append(normalized_day)
    
    return ', '.join(normalized_days) if normalized_days else "Sin preferencia"


def validate_heart_rates(max_hr: Optional[int], resting_hr: Optional[int]) -> List[str]:
    """
    Valida coherencia de frecuencias cardíacas.
    
    Args:
        max_hr: Frecuencia cardíaca máxima
        resting_hr: Frecuencia cardíaca en reposo
    
    Returns:
        List[str]: Lista de errores encontrados
    """
    errors = []
    
    if max_hr is not None and resting_hr is not None:
        if max_hr <= resting_hr:
            errors.append("La FCmáx debe ser mayor que la FCrep")
        
        if max_hr - resting_hr < 20:
            errors.append("La diferencia entre FCmáx y FCrep parece muy pequeña")
    
    if max_hr is not None:
        if max_hr < 120 or max_hr > 220:
            errors.append("FCmáx fuera del rango típico (120-220 ppm)")
    
    if resting_hr is not None:
        if resting_hr < 30 or resting_hr > 100:
            errors.append("FCrep fuera del rango típico (30-100 ppm)")
    
    return errors


def validate_physical_metrics(age: Optional[int], weight: Optional[float], 
                            height: Optional[int]) -> List[str]:
    """
    Valida coherencia de métricas físicas.
    
    Args:
        age: Edad en años
        weight: Peso en kg
        height: Altura en cm
    
    Returns:
        List[str]: Lista de errores encontrados
    """
    errors = []
    
    if age is not None:
        if age < 10 or age > 100:
            errors.append("Edad fuera del rango válido (10-100 años)")
    
    if weight is not None:
        if weight < 30 or weight > 200:
            errors.append("Peso fuera del rango típico (30-200 kg)")
    
    if height is not None:
        if height < 100 or height > 250:
            errors.append("Altura fuera del rango típico (100-250 cm)")
    
    # Validar BMI si tenemos peso y altura
    if weight is not None and height is not None:
        height_m = height / 100.0
        bmi = weight / (height_m ** 2)
        
        if bmi < 15 or bmi > 40:
            errors.append(f"BMI calculado ({bmi:.1f}) fuera del rango típico para atletas")
    
    return errors


def calculate_training_zones(max_hr: int, resting_hr: int) -> TrainingZones:
    """
    Calcula zonas de entrenamiento usando la Fórmula de Karvonen.
    
    La Fórmula de Karvonen: FC_objetivo = FCrep + (intensidad × (FCmáx - FCrep))
    
    Zonas estándar:
    - Z1: 50-60% (Recuperación activa)
    - Z2: 60-70% (Base aeróbica)
    - Z3: 70-80% (Aeróbico)
    - Z4: 80-90% (Umbral anaeróbico)
    - Z5: 90-100% (VO2máx/Neuromuscular)
    
    Args:
        max_hr: Frecuencia cardíaca máxima
        resting_hr: Frecuencia cardíaca en reposo
    
    Returns:
        TrainingZones: Objeto con las 5 zonas calculadas
    """
    hr_reserve = max_hr - resting_hr
    
    # Calcular límites de cada zona
    zones = {
        1: (0.50, 0.60),  # Z1: 50-60%
        2: (0.60, 0.70),  # Z2: 60-70%
        3: (0.70, 0.80),  # Z3: 70-80%
        4: (0.80, 0.90),  # Z4: 80-90%
        5: (0.90, 1.00),  # Z5: 90-100%
    }
    
    calculated_zones = {}
    
    for zone_num, (min_intensity, max_intensity) in zones.items():
        min_hr = round(resting_hr + (min_intensity * hr_reserve))
        max_hr_zone = round(resting_hr + (max_intensity * hr_reserve))
        calculated_zones[f'zone{zone_num}_hr'] = f"{min_hr}-{max_hr_zone}"
    
    return TrainingZones(
        zone1_hr=calculated_zones['zone1_hr'],
        zone2_hr=calculated_zones['zone2_hr'],
        zone3_hr=calculated_zones['zone3_hr'],
        zone4_hr=calculated_zones['zone4_hr'],
        zone5_hr=calculated_zones['zone5_hr']
    )


def validate_race_date(date_str: str, race_name: str = "") -> Tuple[bool, str]:
    """
    Valida fecha de carrera y verifica que esté en el futuro.
    
    Args:
        date_str: Fecha en formato YYYY-MM-DD
        race_name: Nombre de la carrera (para mensajes de error)
    
    Returns:
        Tuple[bool, str]: (es_válida, mensaje_error)
    """
    try:
        race_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = date.today()
        
        if race_date <= today:
            return False, f"La fecha de {race_name or 'la carrera'} debe ser futura"
        
        # Advertir si es muy lejana (más de 2 años)
        days_diff = (race_date - today).days
        if days_diff > 730:
            return True, f"Advertencia: {race_name or 'La carrera'} es en {days_diff} días"
        
        return True, ""
        
    except ValueError:
        return False, "Formato de fecha inválido. Use YYYY-MM-DD"


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


def estimate_vo2_max_from_time(distance_km: float, time_str: str, age: int, weight_kg: float) -> Optional[float]:
    """
    Estimate VO2 max from race performance using established formulas.
    
    Args:
        distance_km: Race distance in kilometers
        time_str: Race time in HH:MM:SS or MM:SS format
        age: Athlete age
        weight_kg: Athlete weight
    
    Returns:
        Optional[float]: Estimated VO2 max in ml/kg/min or None if calculation impossible
    """
    try:
        # Parse time to seconds
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        else:
            return None
        
        # Calculate velocity in m/s
        distance_m = distance_km * 1000
        velocity_ms = distance_m / total_seconds
        
        # Use Jack Daniels' formula for VO2max estimation
        # VO2max = velocity * (0.2 + 0.9 * velocity / pace) + 3.5
        # Simplified approximation for different distances
        if distance_km == 10.0:
            # 10K formula approximation
            pace_min_per_km = total_seconds / 60 / distance_km
            vo2_estimate = 483 / pace_min_per_km
        elif distance_km == 21.097:
            # Half marathon formula approximation
            pace_min_per_km = total_seconds / 60 / distance_km
            vo2_estimate = 460 / pace_min_per_km
        else:
            return None
        
        # Apply age correction (approximate)
        age_factor = 1.0 - (max(0, age - 25) * 0.01)
        vo2_estimate *= age_factor
        
        return round(max(25.0, min(85.0, vo2_estimate)), 1)
        
    except:
        return None

def format_distance_for_display(distance_km: float) -> str:
    """
    Formatea distancia para mostrar de forma amigable.
    
    Args:
        distance_km: Distancia en kilómetros
    
    Returns:
        str: Distancia formateada (ej: "5K", "Media Maratón", "Maratón")
    """
    distance_names = {
        5.0: "5K",
        10.0: "10K", 
        15.0: "15K",
        21.097: "Media Maratón",
        21.1: "Media Maratón",
        42.195: "Maratón",
        42.2: "Maratón"
    }
    
    # Buscar coincidencia exacta o aproximada
    for dist, name in distance_names.items():
        if abs(distance_km - dist) < 0.1:
            return name
    
    # Si no hay coincidencia, mostrar km
    if distance_km == int(distance_km):
        return f"{int(distance_km)}K"
    else:
        return f"{distance_km:.1f}K"


def suggest_training_weeks(race_date: str) -> Optional[int]:
    """
    Suggest optimal training plan duration based on race date.
    
    Args:
        race_date: Race date in YYYY-MM-DD format
    
    Returns:
        Optional[int]: Suggested number of weeks or None if invalid date
    """
    try:
        from datetime import datetime
        race_dt = datetime.strptime(race_date, "%Y-%m-%d")
        now = datetime.now()
        
        if race_dt <= now:
            return None
        
        days_until = (race_dt - now).days
        weeks_until = days_until // 7
        
        # Suggest appropriate duration
        if weeks_until < 6:
            return weeks_until
        elif weeks_until < 12:
            return 8
        elif weeks_until < 20:
            return 12
        else:
            return 16
            
    except:
        return None