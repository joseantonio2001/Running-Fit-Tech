"""
Interfaz de Línea de Comandos (CLI) - CON NUEVOS CAMPOS TÉCNICOS

✅ AÑADIDOS: Nuevos campos en sección de contexto de entrenamiento:
- Experiencia Deportiva (running_experience_years)
- Período de Entrenamiento Actual (current_training_period)  
- Nivel Competitivo (competitive_level)

Este módulo implementa la experiencia interactiva completa para la entrada
manual de datos. Utiliza prompt-toolkit para crear un cuestionario guiado,
modular y a prueba de errores que permite al usuario completar su Ficha
Técnica de manera intuitiva.

Características principales:
- Flujo conversacional modular por secciones
- Validación en tiempo real de entradas
- Normalización automática de datos
- Manejo elegante de campos opcionales
- Control completo de guardado de cambios
- Colores y formato profesional
- CTRL+C durante entrada de datos: descarta cambios de sección y vuelve al menú
- Sistema de detección de cambios en tiempo real (sin flags desincronizados)
- Gestión completa de carreras intermedias y lesiones (añadir/editar/eliminar)
- ✅ VALIDACIÓN EN BUCLE para coherencia de días de entrenamiento
"""

import sys
from copy import deepcopy
from typing import Optional, Dict, List
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog

from .models import AthleteProfile, Injury, Race, create_empty_profile
from .persistence import save_profile, load_profile, has_existing_profile
from .calculations import (
    normalize_gender_input, parse_time_input, parse_training_days_input,
    parse_unavailable_days_input, calculate_training_zones,
    validate_heart_rates, validate_physical_metrics, validate_race_date,
    format_distance_for_display, suggest_training_weeks
)

from .validators import (
    age_validator, weight_validator, height_validator, max_hr_validator,
    resting_hr_validator, vo2_max_validator, weekly_km_validator,
    training_days_validator, time_validator, date_validator,
    distance_validator, terrain_validator, name_validator, yes_no_validator
)

from .cli_helpers import (
    APP_STYLE, print_title, print_subtitle, print_section_header,
    print_success, print_warning, print_error, print_info,
    format_current_value, format_prompt_with_hint, create_menu_options,
    display_profile_summary, display_validation_errors, confirm_action,
    display_welcome_message, clear_screen, display_completion_message
)

from .training_period_validator import TrainingPeriodValidator, parse_training_period

def start_interactive_cli(existing_profile: Optional[AthleteProfile] = None) -> AthleteProfile:
    """
    Inicia la CLI interactiva completa.
    
    Punto de entrada principal para la experiencia de usuario de la Fase 2.
    Maneja el flujo completo desde carga/creación de perfil hasta finalización
    con control completo sobre el guardado de cambios.
    
    Args:
        existing_profile: Perfil ya cargado (opcional). Si se proporciona,
                         se usa en lugar de cargar desde archivo por defecto.
    
    Returns:
        AthleteProfile: Perfil completado por el usuario
    """
    clear_screen()
    display_welcome_message()
    
    # Usar perfil existente o cargar/crear nuevo
    if existing_profile:
        profile = existing_profile
        print_success(f"Usando perfil cargado: {profile.name}")
    else:
        profile = load_existing_or_create_profile()
    
    # Mantener perfil original para comparación (baseline)
    original_profile_baseline = AthleteProfile.from_dict(profile.to_dict())
    
    # Mostrar estado actual
    if profile.name:
        print_info(f"Trabajando con perfil de: {profile.name}")
        display_profile_summary(profile)
    
    # Bucle principal de interacción
    while True:
        try:
            # ✅ CORRECCIÓN: Calcular has_changes en tiempo real
            has_changes = profiles_are_different(original_profile_baseline, profile)
            choice = show_main_menu(profile, has_changes)
            
            if choice in ['1', '2', '3', '4', '5', '6']:
                # Ejecutar función correspondiente
                section_functions = {
                    '1': prompt_personal_info,
                    '2': prompt_physiological_metrics,
                    '3': prompt_training_context,
                    '4': prompt_performance_data,
                    '5': prompt_race_goals,
                    '6': manage_injury_history
                }
                
                section_names = {
                    '1': "Información Personal",
                    '2': "Métricas Fisiológicas",
                    '3': "Contexto de Entrenamiento",
                    '4': "Datos de Rendimiento",
                    '5': "Objetivos de Carrera",
                    '6': "Historial de Lesiones"
                }
                
                # Ejecutar función de la sección
                updated_profile = section_functions[choice](profile)
                
                # Asignar resultado (puede ser perfil original si hubo CTRL+C)
                profile = updated_profile
                
                # Verificar si realmente hay cambios ahora (comparando con baseline)
                if profiles_are_different(original_profile_baseline, profile):
                    print_info("⚠️ Datos modificados - recuerde guardar los cambios")
                
                print_success(f"✅ Sección '{section_names[choice]}' completada")
                
            elif choice == '7':
                display_profile_summary(profile)
                input("\nPresione Enter para continuar...")
                
            elif choice == '8':  # Guardar cambios
                            current_has_changes = profiles_are_different(original_profile_baseline, profile)
                            if current_has_changes:
                                if save_profile(profile):
                                    print_success("✅ Cambios guardados exitosamente")
                                    # Usa deepcopy para crear una copia independiente y actualizada
                                    original_profile_baseline = deepcopy(profile)
                                else:
                                    print_error("❌ Error al guardar cambios")
                            else:
                                print_info("💾 No hay cambios pendientes por guardar")
                    
            elif choice == '9':  # Finalizar y salir
                current_has_changes = profiles_are_different(original_profile_baseline, profile)
                if current_has_changes:
                    return handle_exit_with_changes_simple(profile, current_has_changes)
                else:
                    print_success("Saliendo sin cambios pendientes")
                    return profile
            else:
                print_error("Opción no válida. Por favor, seleccione una opción del menú.")
                
        except (KeyboardInterrupt, EOFError):
            print_info("\n\nInterrupción detectada.")
            current_has_changes = profiles_are_different(original_profile_baseline, profile)
            if current_has_changes:
                return handle_exit_with_changes_simple(profile, current_has_changes)
            else:
                print_success("Saliendo sin cambios pendientes")
                return profile
    
    return profile

def profiles_are_different(original: AthleteProfile, current: AthleteProfile) -> bool:
    """
    Compara perfiles para detectar cambios reales ignorando timestamps.
    
    Args:
        original: Perfil original de referencia
        current: Perfil actual para comparar
        
    Returns:
        bool: True si los perfiles son diferentes
    """
    if original is None or current is None:
        return original != current
    
    original_dict = original.to_dict()
    current_dict = current.to_dict()
    
    # Ignorar timestamps que se generan automáticamente
    original_dict.get('athlete_summary', {}).pop('generated_at', None)
    current_dict.get('athlete_summary', {}).pop('generated_at', None)
    
    return original_dict != current_dict

def load_existing_or_create_profile() -> AthleteProfile:
    """Carga perfil existente o crea uno nuevo."""
    if has_existing_profile():
        print_success("✅ Se encontró un perfil existente")
        profile = load_profile()
        if not profile.name:
            print_info("Perfil encontrado pero incompleto")
        return profile
    else:
        print_info("No se encontró perfil existente. Creando perfil nuevo...")
        return create_empty_profile()

def has_completed_injury_section(profile: AthleteProfile) -> bool:
    """
    Determina si la sección de lesiones está completada.
    Se considera completada si hay lesiones registradas.
    """
    return bool(profile.injuries and len(profile.injuries) > 0)

def show_main_menu(profile: AthleteProfile, has_changes: bool = False) -> str:
    """Muestra el menú principal y devuelve la opción seleccionada."""
    print_subtitle("MENÚ PRINCIPAL")
    
    # Mostrar indicador de cambios pendientes
    if has_changes:
        print_warning("⚠️ Hay cambios sin guardar en esta sesión")
    else:
        print_info("💾 Todos los cambios están guardados")
    
    # Calcular progreso - ACTUALIZADO para nuevos campos
    sections = [
        ("Información Personal", bool(profile.name and profile.age and profile.gender)),
        ("Métricas Fisiológicas", bool(profile.max_hr and profile.resting_hr)),
        ("Contexto Entrenamiento", bool(profile.avg_weekly_km and (profile.training_days_per_week or profile.available_training_days))),  # ACTUALIZADO
        ("Datos Rendimiento", bool(profile.personal_bests and any(profile.personal_bests.values()))),
        ("Objetivos Carrera", bool(profile.main_objective)),
        ("Historial Lesiones", has_completed_injury_section(profile))
    ]
    
    completed = sum(1 for _, is_complete in sections if is_complete)
    total = len(sections)
    print_info(f"ℹ️  Progreso del perfil: {completed}/{total} secciones completadas")
    
    menu_options = {
        '1': '📝 Información Personal' + (' ✅' if sections[0][1] else ' ⭕'),
        '2': '💓 Métricas Fisiológicas' + (' ✅' if sections[1][1] else ' ⭕'),
        '3': '🏃 Contexto de Entrenamiento' + (' ✅' if sections[2][1] else ' ⭕'),
        '4': '🏆 Datos de Rendimiento' + (' ✅' if sections[3][1] else ' ⭕'),
        '5': '🎯 Objetivos de Carrera' + (' ✅' if sections[4][1] else ' ⭕'),
        '6': '🤕 Historial de Lesiones' + (' ✅' if sections[5][1] else ' ⭕'),
        '7': '📊 Ver Resumen del Perfil',
        '8': '💾 Guardar Cambios' + (' ⚠️' if has_changes else ' ✅'),
        '9': '🚪 Finalizar y Salir'
    }
    
    choice = prompt(
        create_menu_options(menu_options),
        validator=MenuValidator(list(menu_options.keys())),
        style=APP_STYLE
    ).strip()
    
    return choice

class MenuValidator(Validator):
    """Validador para opciones de menú que hereda correctamente de Validator."""
    
    def __init__(self, valid_options: List[str]):
        self.valid_options = valid_options
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        if text not in self.valid_options:
            valid_list = ', '.join(self.valid_options)
            raise ValidationError(
                message=f'Opción inválida. Opciones válidas: {valid_list}',
                cursor_position=len(text)
            )

def prompt_personal_info(profile: AthleteProfile) -> AthleteProfile:
    """Solicita información personal básica."""
    print_section_header("Información Personal")
    
    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())
    
    try:
        # Nombre (obligatorio)
        profile.name = prompt(
            format_prompt_with_hint(
                "Nombre completo",
                "nombre y apellidos",
                profile.name
            ),
            validator=name_validator,
            default=profile.name or "",
            style=APP_STYLE
        ).strip()
        
        # Edad (obligatorio)
        age_input = prompt(
            format_prompt_with_hint(
                "Edad",
                "años",
                profile.age
            ),
            validator=age_validator,
            default=str(profile.age) if profile.age else "",
            style=APP_STYLE
        ).strip()
        if age_input:
            profile.age = int(age_input)
        
        # Género (obligatorio con normalización)
        gender_completer = WordCompleter(['Masculino', 'Femenino', 'Otro'], ignore_case=True)
        gender_input = prompt(
            format_prompt_with_hint(
                "Género",
                "M/Masculino, F/Femenino, Otro",
                profile.gender
            ),
            completer=gender_completer,
            default=profile.gender or "",
            style=APP_STYLE
        ).strip()
        if gender_input:
            profile.gender = normalize_gender_input(gender_input)
        
        # Altura (opcional)
        height_input = prompt(
            format_prompt_with_hint(
                "Altura en cm",
                "opcional - ej: 180",
                profile.height_cm
            ),
            validator=height_validator,
            default=str(profile.height_cm) if profile.height_cm else "",
            style=APP_STYLE
        ).strip()
        if height_input:
            profile.height_cm = int(height_input)
        
        # Peso (opcional)
        weight_input = prompt(
            format_prompt_with_hint(
                "Peso en kg",
                "opcional - ej: 67.5",
                profile.weight_kg
            ),
            validator=weight_validator,
            default=str(profile.weight_kg) if profile.weight_kg else "",
            style=APP_STYLE
        ).strip()
        if weight_input:
            profile.weight_kg = float(weight_input.replace(',', '.'))
        
        # Validar datos físicos
        physical_errors = validate_physical_metrics(profile.age, profile.weight_kg, profile.height_cm)
        if physical_errors:
            display_validation_errors(physical_errors)
        
        display_completion_message("Información Personal")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        # CTRL+C durante entrada de datos: descartar cambios y volver
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def prompt_physiological_metrics(profile: AthleteProfile) -> AthleteProfile:
    """Solicita métricas fisiológicas."""
    print_section_header("Métricas Fisiológicas")
    
    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())
    
    try:
        print_info("Estas métricas son clave para calcular zonas de entrenamiento precisas")
        
        # FC Máxima
        max_hr_input = prompt(
            format_prompt_with_hint(
                "Frecuencia Cardíaca Máxima (FCmáx)",
                "pulsaciones por minuto - ej: 184",
                profile.max_hr
            ),
            validator=max_hr_validator,
            default=str(profile.max_hr) if profile.max_hr else "",
            style=APP_STYLE
        ).strip()
        if max_hr_input:
            profile.max_hr = int(max_hr_input)
        
        # FC Reposo
        resting_hr_input = prompt(
            format_prompt_with_hint(
                "Frecuencia Cardíaca en Reposo (FCrep)",
                "pulsaciones por minuto - ej: 41",
                profile.resting_hr
            ),
            validator=resting_hr_validator,
            default=str(profile.resting_hr) if profile.resting_hr else "",
            style=APP_STYLE
        ).strip()
        if resting_hr_input:
            profile.resting_hr = int(resting_hr_input)
        
        # Validar coherencia de FC
        if profile.max_hr and profile.resting_hr:
            hr_errors = validate_heart_rates(profile.max_hr, profile.resting_hr)
            if hr_errors:
                display_validation_errors(hr_errors)
            else:
                print_success("Frecuencias cardíacas coherentes")
                # Calcular zonas de entrenamiento automáticamente
                profile.training_zones = calculate_training_zones(profile.max_hr, profile.resting_hr)
                print_success("Zonas de entrenamiento calculadas automáticamente")
        
        # VO2 Máx (opcional)
        vo2_input = prompt(
            format_prompt_with_hint(
                "VO2 Máximo",
                "opcional - ml/kg/min - ej: 60.0",
                profile.vo2_max
            ),
            validator=vo2_max_validator,
            default=str(profile.vo2_max) if profile.vo2_max else "",
            style=APP_STYLE
        ).strip()
        if vo2_input:
            profile.vo2_max = float(vo2_input.replace(',', '.'))
        
        # Umbral de Lactato (opcional)
        lactate_input = prompt(
            format_prompt_with_hint(
                "Umbral de Lactato",
                "opcional - pulsaciones por minuto - ej: 179",
                profile.lactate_threshold_bpm
            ),
            validator=max_hr_validator,  # Mismo rango que FCmáx
            default=str(profile.lactate_threshold_bpm) if profile.lactate_threshold_bpm else "",
            style=APP_STYLE
        ).strip()
        if lactate_input:
            profile.lactate_threshold_bpm = int(lactate_input)
        
        # VFC (opcional)
        hrv_input = prompt(
            format_prompt_with_hint(
                "Variabilidad de Frecuencia Cardíaca (VFC)",
                "opcional - milisegundos - ej: 45",
                profile.hrv_ms
            ),
            validator=OptionalIntegerValidator(10, 200),
            default=str(profile.hrv_ms) if profile.hrv_ms else "",
            style=APP_STYLE
        ).strip()
        if hrv_input:
            profile.hrv_ms = int(hrv_input)
        
        display_completion_message("Métricas Fisiológicas")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        # CTRL+C durante entrada de datos: descartar cambios y volver
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def prompt_training_context(profile: AthleteProfile) -> AthleteProfile:
    """
    Solicita contexto de entrenamiento CON NUEVOS CAMPOS TÉCNICOS.
    """
    print_section_header("Contexto de Entrenamiento")
    
    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())
    
    try:

        # ✅ NUEVO CAMPO 2: Período de Entrenamiento Actual
        current_period_input = prompt(
            format_prompt_with_hint(
                "Período de entrenamiento actual",
                "tiempo entrenando actualmente - ej: '3 semanas', '2 meses', '0 - empezando'",
                profile.current_training_period
            ),
            validator=TrainingPeriodValidator(),
            default=profile.current_training_period or "",
            style=APP_STYLE
        ).strip()
        if current_period_input:
            normalized_period = parse_training_period(current_period_input)
            profile.current_training_period = normalized_period
            
            # Mostrar confirmación si se normalizó
            if normalized_period != current_period_input:
                print_success(f"✅ Período normalizado a: '{normalized_period}'")        

        # Volumen semanal actual
        weekly_km_input = prompt(
            format_prompt_with_hint(
                "Volumen semanal promedio actual",
                "kilómetros por semana - ej: 50.0",
                profile.avg_weekly_km
            ),
            validator=weekly_km_validator,
            default=str(profile.avg_weekly_km) if profile.avg_weekly_km else "",
            style=APP_STYLE
        ).strip()
        if weekly_km_input:
            profile.avg_weekly_km = float(weekly_km_input.replace(',', '.'))
        
        # Días de entrenamiento por semana (mantener para contexto actual)
        days_input = prompt(
            format_prompt_with_hint(
                "Días de entrenamiento por semana",
                "contexto actual - ej: 4 o 4-5 para rango",
                profile.training_days_per_week
            ),
            validator=training_days_validator,
            default=profile.training_days_per_week or "",
            style=APP_STYLE
        ).strip()
        if days_input:
            profile.training_days_per_week = parse_training_days_input(days_input)
        
        # ✅ NUEVO CAMPO 1: Experiencia Deportiva (años corriendo)
        experience_input = prompt(
            format_prompt_with_hint(
                "Experiencia deportiva en running",
                "años totales practicando running - ej: 5 o 2.5",
                profile.running_experience_years
            ),
            validator=OptionalFloatValidator(0, 50),
            default=str(profile.running_experience_years) if profile.running_experience_years else "",
            style=APP_STYLE
        ).strip()
        if experience_input:
            profile.running_experience_years = float(experience_input.replace(',', '.'))
        
        # CAMPO EXISTENTE: Días disponibles para entrenar (acepta rangos)
        available_days_input = prompt(
            format_prompt_with_hint(
                "Días disponibles para entrenar",
                "ej: 4, 3-4, 5-6 (acepta rangos coherentes)",
                profile.available_training_days
            ),
            validator=training_days_validator,
            default=profile.available_training_days or profile.training_days_per_week or "",
            style=APP_STYLE
        ).strip()
        if available_days_input:
            profile.available_training_days = parse_training_days_input(available_days_input)
        
        # ✅ CAMPO EXISTENTE CON BUCLE DE VALIDACIÓN: Días NO disponibles
        while True:
            unavailable_days_input = prompt(
                format_prompt_with_hint(
                    "Días NO disponibles para entrenar",
                    "ej: Domingo, D, L,D (acepta abreviaciones) — vacío = sin restricciones",
                    profile.unavailable_days
                ),
                default=profile.unavailable_days or "",
                style=APP_STYLE
            ).strip()

            # Vacío es válido: significa sin restricciones
            if unavailable_days_input == "":
                profile.unavailable_days = ""
                break

            # Normalizar y validar coherencia
            normalized = parse_unavailable_days_input(unavailable_days_input)
            profile.unavailable_days = normalized

            validation_errors = profile._validate_training_days_coherence()
            if validation_errors:
                print_warning("⚠️ Advertencias de coherencia:")
                for error in validation_errors:
                    print_warning(f"  - {error}")
                print_info("Por favor, introduzca un valor coherente o deje vacío si no tiene restricciones.")
                continue
            break
        
        # Historial de fuerza
        strength_history_input = prompt(
            format_prompt_with_hint(
                "¿Ha realizado entrenamiento de fuerza anteriormente?",
                "S/Sí o N/No",
                "Sí" if profile.strength_training_history else "No" if profile.strength_training_history is not None else None
            ),
            validator=yes_no_validator,
            default="Sí" if profile.strength_training_history else "No" if profile.strength_training_history is not None else "",
            style=APP_STYLE
        ).strip()
        if strength_history_input:
            profile.strength_training_history = strength_history_input.lower() in ['sí', 'si', 's', 'yes', 'y']
        
        # Incluir fuerza en nuevo plan
        include_strength_input = prompt(
            format_prompt_with_hint(
                "¿Desea incluir entrenamiento de fuerza en el nuevo plan?",
                "S/Sí o N/No",
                "Sí" if profile.include_strength_training else "No" if profile.include_strength_training is not None else None
            ),
            validator=yes_no_validator,
            default="Sí" if profile.include_strength_training else "No" if profile.include_strength_training is not None else "",
            style=APP_STYLE
        ).strip()
        if include_strength_input:
            profile.include_strength_training = include_strength_input.lower() in ['sí', 'si', 's', 'yes', 'y']
        
        display_completion_message("Contexto de Entrenamiento")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        # CTRL+C durante entrada de datos: descartar cambios y volver
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def prompt_performance_data(profile: AthleteProfile) -> AthleteProfile:
    """Solicita datos de rendimiento y marcas personales."""
    print_section_header("Datos de Rendimiento")

    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())

    try:
        print_info("Ingrese sus mejores marcas personales (puede omitir las que no tenga)")

        # Asegurar que personal_bests esté inicializado
        if not profile.personal_bests:
            profile.personal_bests = {}

        # Crear una copia temporal para trabajar
        temp_personal_bests = profile.personal_bests.copy()

        # Distancias estándar
        standard_distances = [
            ("5k", "5 Kilómetros"),
            ("10k", "10 Kilómetros"),
            ("half_marathon", "Media Maratón (21K)"),
            ("marathon", "Maratón (42K)")
        ]

        for key, description in standard_distances:
            current_time = temp_personal_bests.get(key)
            time_input = prompt(
                format_prompt_with_hint(
                    f"Mejor marca en {description}",
                    "formato HH:MM:SS o MM:SS - opcional",
                    current_time
                ),
                validator=time_validator,
                default=current_time or "",
                style=APP_STYLE
            ).strip()

            if time_input:
                parsed_time = parse_time_input(time_input)
                if parsed_time:
                    temp_personal_bests[key] = parsed_time
                    print_success(f"Marca en {description}: {parsed_time}")
                else:
                    print_warning(f"No se pudo parsear el tiempo: {time_input}")
            elif current_time:
                # Mantener tiempo existente si no se ingresa nada
                temp_personal_bests[key] = current_time

        # ✅ **CORRECCIÓN**: Asignar el diccionario temporal al perfil al final
        profile.personal_bests = temp_personal_bests

        # Estimar VO2máx si no se tiene y hay marcas
        if not profile.vo2_max and profile.age and profile.weight_kg:
            best_time_for_estimation = None
            best_distance = None
            
            # Buscar la mejor marca para estimación (preferir 10K o media maratón)
            for distance_key, distance_km, description in [("10k", 10.0, "10K"), ("half_marathon", 21.097, "Media Maratón")]:
                if profile.personal_bests.get(distance_key):
                    best_time_for_estimation = profile.personal_bests[distance_key]
                    best_distance = distance_km
                    break
            
            if best_time_for_estimation:
                from .calculations import estimate_vo2_max_from_time
                estimated_vo2 = estimate_vo2_max_from_time(
                    best_distance,
                    best_time_for_estimation,
                    profile.age,
                    profile.weight_kg
                )
                
                if estimated_vo2:
                    print_info(f"VO2máx estimado basado en marca personal: {estimated_vo2} ml/kg/min")
                    if confirm_action("¿Desea usar esta estimación?", True):
                        profile.vo2_max = estimated_vo2
                        print_success(f"VO2máx establecido en: {estimated_vo2} ml/kg/min")
        
        display_completion_message("Datos de Rendimiento")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        # CTRL+C durante entrada de datos: descartar cambios y volver
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def prompt_race_goals(profile: AthleteProfile) -> AthleteProfile:
    """Solicita objetivos de carrera con gestión completa."""
    print_section_header("Objetivos de Carrera")
    
    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())
    
    try:
        # Objetivo principal (obligatorio)
        profile = manage_main_objective(profile)
        
        # Carreras intermedias con gestión completa
        profile = manage_intermediate_races_complete(profile)
        
        display_completion_message("Objetivos de Carrera")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def manage_main_objective(profile: AthleteProfile) -> AthleteProfile:
    """Gestiona el objetivo principal."""
    print_info("Defina su objetivo principal de carrera")
    
    if profile.main_objective:
        print_success(f"Objetivo actual: {profile.main_objective.name} ({profile.main_objective.date})")
        if not confirm_action("¿Desea modificar el objetivo principal?", False):
            return profile
    
    # Nombre de la carrera
    race_name = prompt(
        format_prompt_with_hint(
            "Nombre de la carrera objetivo",
            "ej: Media Maratón de Valencia",
            profile.main_objective.name if profile.main_objective else None
        ),
        validator=name_validator,
        default=profile.main_objective.name if profile.main_objective else "",
        style=APP_STYLE
    ).strip()
    
    # Fecha de la carrera
    race_date = prompt(
        format_prompt_with_hint(
            "Fecha de la carrera",
            "formato YYYY-MM-DD - ej: 2024-11-30",
            profile.main_objective.date if profile.main_objective else None
        ),
        validator=date_validator,
        default=profile.main_objective.date if profile.main_objective else "",
        style=APP_STYLE
    ).strip()
    
    # Validar fecha
    date_valid, date_error = validate_race_date(race_date, race_name)
    if not date_valid:
        print_error(date_error)
        return profile
    elif date_error:
        print_warning(date_error)
    
    # Distancia
    distance_input = prompt(
        format_prompt_with_hint(
            "Distancia en kilómetros",
            "ej: 21.097 para media maratón",
            profile.main_objective.distance_km if profile.main_objective else None
        ),
        validator=distance_validator,
        default=str(profile.main_objective.distance_km) if profile.main_objective else "",
        style=APP_STYLE
    ).strip()
    distance_km = float(distance_input.replace(',', '.'))
    
    # Tiempo objetivo (opcional)
    goal_time = prompt(
        format_prompt_with_hint(
            "Tiempo objetivo",
            "opcional - formato HH:MM:SS - ej: 01:28:00",
            profile.main_objective.goal_time if profile.main_objective else None
        ),
        validator=time_validator,
        default=profile.main_objective.goal_time if profile.main_objective else "",
        style=APP_STYLE
    ).strip()
    
    if goal_time:
        parsed_goal_time = parse_time_input(goal_time)
        if parsed_goal_time:
            goal_time = parsed_goal_time
    
    # Terreno
    terrain_completer = WordCompleter(['Llano', 'Montañoso', 'Mixto', 'Trail', 'Pista'], ignore_case=True)
    terrain = prompt(
        format_prompt_with_hint(
            "Tipo de terreno",
            "Llano, Montañoso, Mixto, Trail, Pista",
            profile.main_objective.terrain if profile.main_objective else None
        ),
        completer=terrain_completer,
        validator=terrain_validator,
        default=profile.main_objective.terrain if profile.main_objective else "",
        style=APP_STYLE
    ).strip()
    
    # Crear objetivo principal
    profile.main_objective = Race(
        name=race_name,
        date=race_date,
        distance_km=distance_km,
        goal_time=goal_time if goal_time else None,
        terrain=terrain.title()
    )
    
    print_success(f"Objetivo principal establecido: {race_name}")
    
    # Sugerir duración de plan
    suggested_weeks = suggest_training_weeks(race_date)
    print_info(f"Sugerencia: Plan de {suggested_weeks} semanas basado en fecha objetivo")
    
    return profile

def manage_intermediate_races_complete(profile: AthleteProfile) -> AthleteProfile:
    """Gestiona carreras intermedias con funcionalidad completa."""
    
    # Inicializar lista si no existe
    if not profile.intermediate_races:
        profile.intermediate_races = []
    
    while True:
        print_info("\n🏁 GESTIÓN DE CARRERAS INTERMEDIAS")
        display_race_summary(profile.intermediate_races)
        
        # Menú de opciones
        if not profile.intermediate_races:
            print_info("No hay carreras intermedias registradas")
            if confirm_action("¿Desea añadir una carrera intermedia?", False):
                race = create_intermediate_race()
                if race:
                    profile.intermediate_races.append(race)
                    print_success(f"Carrera añadida: {race.name}")
            else:
                break
        else:
            # Opciones cuando hay carreras existentes
            print_info("\n🔧 Opciones disponibles:")
            print_info("  1. ➕ Añadir nueva carrera")
            print_info("  2. ✏️  Editar carrera existente")
            print_info("  3. 🗑️  Eliminar carrera")
            print_info("  4. ➡️  Continuar sin cambios")
            
            choice = prompt(
                "Seleccione una opción (1-4): ",
                validator=MenuValidator(['1', '2', '3', '4']),
                style=APP_STYLE
            ).strip()
            
            if choice == '1':
                # Añadir nueva carrera
                race = create_intermediate_race()
                if race:
                    profile.intermediate_races.append(race)
                    print_success(f"Carrera añadida: {race.name}")
                    
            elif choice == '2':
                # Editar carrera existente
                race_index = select_race_to_modify(profile.intermediate_races, "editar")
                if race_index is not None:
                    updated_race = edit_intermediate_race(profile.intermediate_races[race_index])
                    if updated_race:
                        profile.intermediate_races[race_index] = updated_race
                        print_success(f"Carrera actualizada: {updated_race.name}")
                        
            elif choice == '3':
                # Eliminar carrera
                race_index = select_race_to_modify(profile.intermediate_races, "eliminar")
                if race_index is not None:
                    removed_race = profile.intermediate_races.pop(race_index)
                    print_success(f"Carrera eliminada: {removed_race.name}")
                    
            elif choice == '4':
                # Salir del bucle
                break
    
    return profile

def select_race_to_modify(races: List, action: str) -> Optional[int]:
    """Permite seleccionar una carrera para modificar."""
    if not races:
        return None
    
    print_info(f"\n🏁 Seleccione carrera para {action}:")
    for i, race in enumerate(races, 1):
        distance_display = format_distance_for_display(race.distance_km)
        print_info(f"  {i}. {race.name} - {distance_display} ({race.date})")
    
    try:
        choice = prompt(
            f"Seleccione número de carrera (1-{len(races)}) o 'c' para cancelar: ",
            style=APP_STYLE
        ).strip().lower()
        
        if choice == 'c':
            return None
        
        index = int(choice) - 1
        if 0 <= index < len(races):
            return index
        else:
            print_warning("Número de carrera inválido")
            return None
    except (ValueError, KeyboardInterrupt):
        return None

def edit_intermediate_race(race: Race) -> Optional[Race]:
    """Edita una carrera intermedia existente."""
    try:
        print_info(f"\n✏️  Editando: {race.name}")
        
        # Permitir mantener valores actuales presionando Enter
        name = prompt(
            format_prompt_with_hint("Nombre de la carrera", "actual: " + race.name, race.name),
            validator=name_validator,
            default=race.name,
            style=APP_STYLE
        ).strip()
        
        date = prompt(
            format_prompt_with_hint("Fecha", "YYYY-MM-DD, actual: " + race.date, race.date),
            validator=date_validator,
            default=race.date,
            style=APP_STYLE
        ).strip()
        
        distance = prompt(
            format_prompt_with_hint("Distancia en km", f"actual: {race.distance_km}", str(race.distance_km)),
            validator=distance_validator,
            default=str(race.distance_km),
            style=APP_STYLE
        ).strip()
        
        goal_time = prompt(
            format_prompt_with_hint("Tiempo objetivo", f"actual: {race.goal_time or 'Sin objetivo'}", race.goal_time),
            validator=time_validator,
            default=race.goal_time or "",
            style=APP_STYLE
        ).strip()
        
        terrain = prompt(
            format_prompt_with_hint("Tipo de terreno", f"actual: {race.terrain}", race.terrain),
            validator=terrain_validator,
            default=race.terrain,
            style=APP_STYLE
        ).strip()
        
        return Race(
            name=name,
            date=date,
            distance_km=float(distance.replace(',', '.')),
            goal_time=parse_time_input(goal_time) if goal_time else None,
            terrain=terrain.title()
        )
        
    except (KeyboardInterrupt, EOFError):
        return None

def create_intermediate_race() -> Optional[Race]:
    """Crea una carrera intermedia."""
    try:
        name = prompt(
            format_prompt_with_hint("Nombre de la carrera", "ej: 10K de la Ciudad"),
            validator=name_validator,
            style=APP_STYLE
        ).strip()
        
        date = prompt(
            format_prompt_with_hint("Fecha", "YYYY-MM-DD"),
            validator=date_validator,
            style=APP_STYLE
        ).strip()
        
        distance = prompt(
            format_prompt_with_hint("Distancia en km", "ej: 10.0"),
            validator=distance_validator,
            style=APP_STYLE
        ).strip()
        
        goal_time = prompt(
            format_prompt_with_hint("Tiempo objetivo", "opcional - HH:MM:SS"),
            validator=time_validator,
            style=APP_STYLE
        ).strip()
        
        terrain = prompt(
            format_prompt_with_hint("Tipo de terreno", "Llano, Montañoso, etc."),
            validator=terrain_validator,
            style=APP_STYLE
        ).strip()
        
        return Race(
            name=name,
            date=date,
            distance_km=float(distance.replace(',', '.')),
            goal_time=parse_time_input(goal_time) if goal_time else None,
            terrain=terrain.title()
        )
        
    except (KeyboardInterrupt, EOFError):
        return None

def manage_injury_history(profile: AthleteProfile) -> AthleteProfile:
    """Gestiona el historial de lesiones con funcionalidad completa."""
    print_section_header("Historial de Lesiones")
    
    # Crear copia de seguridad del perfil al inicio de la sección
    original_profile = AthleteProfile.from_dict(profile.to_dict())
    
    try:
        print_info("Las lesiones pasadas ayudan a personalizar el plan de entrenamiento")
        
        # Inicializar lista si no existe
        if not profile.injuries:
            profile.injuries = []
        
        while True:
            print_info("\n🤕 GESTIÓN DE HISTORIAL DE LESIONES")
            display_injury_summary(profile.injuries)
            
            if not profile.injuries:
                print_info("No hay lesiones registradas")
                if not confirm_action("¿Ha tenido alguna lesión relacionada con el running?", False):
                    break
                else:
                    injury = create_injury()
                    if injury:
                        profile.injuries.append(injury)
                        print_success(f"Lesión añadida: {injury.type}")
            else:
                # Opciones cuando hay lesiones existentes
                print_info("\n🔧 Opciones disponibles:")
                print_info("  1. ➕ Añadir nueva lesión")
                print_info("  2. ✏️  Editar lesión existente")
                print_info("  3. 🗑️  Eliminar lesión")
                print_info("  4. ➡️  Continuar sin cambios")
                
                choice = prompt(
                    "Seleccione una opción (1-4): ",
                    validator=MenuValidator(['1', '2', '3', '4']),
                    style=APP_STYLE
                ).strip()
                
                if choice == '1':
                    # Añadir nueva lesión
                    injury = create_injury()
                    if injury:
                        profile.injuries.append(injury)
                        print_success(f"Lesión añadida: {injury.type}")
                        
                elif choice == '2':
                    # Editar lesión existente
                    injury_index = select_injury_to_modify(profile.injuries, "editar")
                    if injury_index is not None:
                        updated_injury = edit_injury(profile.injuries[injury_index])
                        if updated_injury:
                            profile.injuries[injury_index] = updated_injury
                            print_success(f"Lesión actualizada: {updated_injury.type}")
                            
                elif choice == '3':
                    # Eliminar lesión
                    injury_index = select_injury_to_modify(profile.injuries, "eliminar")
                    if injury_index is not None:
                        removed_injury = profile.injuries.pop(injury_index)
                        print_success(f"Lesión eliminada: {removed_injury.type}")
                        
                elif choice == '4':
                    # Salir del bucle
                    break
        
        display_completion_message("Historial de Lesiones")
        return profile
        
    except (KeyboardInterrupt, EOFError):
        print_info("\n⚡ Entrada interrumpida - cambios de esta sección descartados")
        print_info("↩️ Volviendo al menú principal...")
        return original_profile

def select_injury_to_modify(injuries: List, action: str) -> Optional[int]:
    """Permite seleccionar una lesión para modificar."""
    if not injuries:
        return None
    
    print_info(f"\n🤕 Seleccione lesión para {action}:")
    for i, injury in enumerate(injuries, 1):
        print_info(f"  {i}. {injury.type} ({injury.date_approx})")
    
    try:
        choice = prompt(
            f"Seleccione número de lesión (1-{len(injuries)}) o 'c' para cancelar: ",
            style=APP_STYLE
        ).strip().lower()
        
        if choice == 'c':
            return None
        
        index = int(choice) - 1
        if 0 <= index < len(injuries):
            return index
        else:
            print_warning("Número de lesión inválido")
            return None
    except (ValueError, KeyboardInterrupt):
        return None

def edit_injury(injury: Injury) -> Optional[Injury]:
    """Edita una lesión existente."""
    try:
        print_info(f"\n✏️  Editando: {injury.type}")
        
        injury_type = prompt(
            format_prompt_with_hint("Tipo de lesión", "actual: " + injury.type, injury.type),
            validator=name_validator,
            default=injury.type,
            style=APP_STYLE
        ).strip()
        
        date_approx = prompt(
            format_prompt_with_hint("Fecha aproximada", "actual: " + injury.date_approx, injury.date_approx),
            default=injury.date_approx,
            style=APP_STYLE
        ).strip()
        
        recovery_desc = prompt(
            format_prompt_with_hint("Descripción de recuperación", "actual: " + injury.recovery_desc, injury.recovery_desc),
            default=injury.recovery_desc,
            style=APP_STYLE
        ).strip()

        current_status = prompt(
            format_prompt_with_hint(
                "Estado actual", 
                "opcional - ej: 'molestias leves', 'limitación de movimiento', 'sin síntomas'",
                injury.current_status  # Valor actual de la lesión
            ),
            default=injury.current_status or "",
            style=APP_STYLE
        ).strip()
        
        return Injury(
            type=injury_type,
            date_approx=date_approx,
            recovery_desc=recovery_desc,
            current_status=current_status if current_status else None  # ✅ NUEVO
        )
        
    except (KeyboardInterrupt, EOFError):
        return None

def create_injury() -> Optional[Injury]:
    """Crea una lesión."""
    try:
        injury_type = prompt(
            format_prompt_with_hint("Tipo de lesión", "ej: Fascitis Plantar, Tendinitis Aquiles"),
            validator=name_validator,
            style=APP_STYLE
        ).strip()
        
        date_approx = prompt(
            format_prompt_with_hint("Fecha aproximada", "ej: 2022-10 o Hace 2 años"),
            style=APP_STYLE
        ).strip()
        
        recovery_desc = prompt(
            format_prompt_with_hint("Descripción de recuperación", "ej: Fisioterapia y descanso 6 semanas"),
            style=APP_STYLE
        ).strip()
        
        # ✅ NUEVA PREGUNTA
        current_status = prompt(
            format_prompt_with_hint(
                "Estado actual", # El prompt principal
                "opcional - ej: 'molestias leves', 'limitación de movimiento', 'sin síntomas' (vacío = no especificado)",
                None
            ),
            style=APP_STYLE
        ).strip()
        
        return Injury(
            type=injury_type,
            date_approx=date_approx,
            recovery_desc=recovery_desc,
            current_status=current_status if current_status else None  # ✅ NUEVO
        )
        
    except (KeyboardInterrupt, EOFError):
        return None


def handle_exit_with_changes_simple(profile: AthleteProfile, has_changes: bool) -> AthleteProfile:
    """Versión simplificada del manejo de salida."""
    if not has_changes:
        return profile
    
    print_warning("⚠️ Hay cambios sin guardar")
    if confirm_action("¿Desea guardar los cambios antes de salir?", True):
        if save_profile(profile):
            print_success("✅ Cambios guardados exitosamente")
            return profile
        else:
            print_error("❌ Error al guardar")
            return profile
    else:
        print_info("🗑️ Cambios descartados - saliendo sin guardar")
        return profile

def get_missing_required_data(profile: AthleteProfile) -> List[str]:
    """Identifica datos requeridos faltantes."""
    missing = []
    
    if not profile.name:
        missing.append("Nombre del atleta")
    if not profile.age:
        missing.append("Edad")
    if not profile.gender:
        missing.append("Género")
    if not profile.main_objective:
        missing.append("Objetivo principal de carrera")
        
    return missing

def display_race_summary(races: List) -> None:
    """Muestra resumen de carreras registradas."""
    if not races:
        print_info("No hay carreras intermedias registradas")
        return
    
    print_section_header(f"Carreras Intermedias ({len(races)})")
    for i, race in enumerate(races, 1):
        distance_display = format_distance_for_display(race.distance_km)
        print_info(f"  {i}. {race.name} - {distance_display} ({race.date})")
        if race.goal_time:
            print_info(f"     🎯 Meta: {race.goal_time} en {race.terrain}")

def display_injury_summary(injuries: List) -> None:
    """Muestra resumen de lesiones registradas."""
    if not injuries:
        print_info("No hay lesiones registradas")
        return
    
    print_section_header(f"Lesiones Registradas ({len(injuries)})")
    for i, injury in enumerate(injuries, 1):
        print_info(f"  {i}. {injury.type} ({injury.date_approx})")
        print_info(f"     🏥 Recuperación: {injury.recovery_desc}")
        status = injury.current_status or "No especificado"
        print_info(f"     📊 Estado actual: {status}")

# ✅ Clases auxiliares para validación
class OptionalIntegerValidator(Validator):
    """
    ✅ CORREGIDO: Validador para enteros opcionales con herencia correcta.
    
    Permite campos vacíos (opcionales) y valida rangos cuando hay valor.
    Compatible con prompt_toolkit async validation.
    """
    
    def __init__(self, min_val: Optional[int] = None, max_val: Optional[int] = None):
        self.min_val = min_val
        self.max_val = max_val
        super().__init__()
    
    def validate(self, document: Document) -> None:
        """Validación síncrona requerida por Validator"""
        text = document.text.strip()
        
        if not text:
            return  # Opcional - permitir campo vacío
        
        try:
            value = int(text)
            if self.min_val and value < self.min_val:
                raise ValidationError(message=f'Valor debe ser ≥ {self.min_val}')
            if self.max_val and value > self.max_val:
                raise ValidationError(message=f'Valor debe ser ≤ {self.max_val}')
        except ValueError:
            raise ValidationError(message='Ingrese un número entero válido')
    
    async def validate_async(self, document: Document) -> None:
        """✅ AÑADIDO: Validación async requerida por prompt_toolkit"""
        # Para validadores simples como este, podemos usar la validación síncrona
        self.validate(document)

class OptionalFloatValidator(Validator):
    """
    ✅ CORREGIDO: Validador para flotantes opcionales con herencia correcta.
    
    Permite campos vacíos (opcionales) y valida rangos cuando hay valor.
    Compatible con prompt_toolkit async validation.
    """
    
    def __init__(self, min_val: Optional[float] = None, max_val: Optional[float] = None):
        self.min_val = min_val
        self.max_val = max_val
        super().__init__()
    
    def validate(self, document: Document) -> None:
        """Validación síncrona requerida por Validator"""
        text = document.text.strip()
        
        if not text:
            return  # Opcional - permitir campo vacío
        
        try:
            # Permitir comas como separador decimal
            value = float(text.replace(',', '.'))
            if self.min_val is not None and value < self.min_val:
                raise ValidationError(message=f'Valor debe ser ≥ {self.min_val}')
            if self.max_val is not None and value > self.max_val:
                raise ValidationError(message=f'Valor debe ser ≤ {self.max_val}')
        except ValueError:
            raise ValidationError(message='Ingrese un número válido (use . o , para decimales)')
    
    async def validate_async(self, document: Document) -> None:
        """✅ AÑADIDO: Validación async requerida por prompt_toolkit"""
        # Para validadores simples como este, podemos usar la validación síncrona
        self.validate(document)

class OptionalStringValidator(Validator):
    """
    ✅ NUEVO: Validador para campos de texto opcionales con longitud.
    
    Útil para campos como current_training_period que pueden estar vacíos
    pero tienen restricciones de longitud cuando tienen contenido.
    """
    
    def __init__(self, min_length: Optional[int] = None, max_length: Optional[int] = None):
        self.min_length = min_length
        self.max_length = max_length
        super().__init__()
    
    def validate(self, document: Document) -> None:
        """Validación síncrona requerida por Validator"""
        text = document.text.strip()
        
        if not text:
            return  # Opcional - permitir campo vacío
        
        if self.min_length is not None and len(text) < self.min_length:
            raise ValidationError(message=f'Mínimo {self.min_length} caracteres')
        if self.max_length is not None and len(text) > self.max_length:
            raise ValidationError(message=f'Máximo {self.max_length} caracteres')
    
    async def validate_async(self, document: Document) -> None:
        """✅ AÑADIDO: Validación async requerida por prompt_toolkit"""
        self.validate(document)

def main():
    """Función principal para testing independiente del módulo CLI."""
    try:
        profile = start_interactive_cli()
        print_success(f"\n¡CLI completada! Perfil de {profile.name} listo.")
        
        if profile.is_complete():
            print_success("Perfil completo y listo para las siguientes fases")
        else:
            print_warning("Perfil incompleto - puede completarse en futuras sesiones")
            
    except Exception as e:
        print_error(f"Error en CLI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()