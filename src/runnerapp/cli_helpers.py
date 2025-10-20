"""
Utilidades y Helpers para CLI - CORREGIDO: Sin validate_data()

✅ ELIMINADO: profile.validate_data() que no existe en AthleteProfile
✅ CORREGIDO: Función display_profile_summary sin errores
✅ MANTENIDO: Toda la funcionalidad de helpers y estilos
✅ AÑADIDO: Mejor manejo de completitud de perfil

Este módulo proporciona funciones de utilidad para formatear la salida,
crear elementos de interfaz consistentes y manejar la presentación
de datos en la CLI interactiva.

Incluye estilos, colores y formatos estándar para mantener una
experiencia de usuario coherente y profesional.
"""

from typing import Dict, List, Optional, Any
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from datetime import datetime

# Estilo global para la aplicación
APP_STYLE = Style.from_dict({
    'title': '#00aa00 bold',      # Verde para títulos
    'subtitle': '#0066cc bold',   # Azul para subtítulos
    'question': '#ffffff',        # Blanco para preguntas
    'hint': '#666666 italic',     # Gris para pistas/ayuda
    'error': '#ff0066 bold',      # Rojo para errores
    'success': '#00aa00',         # Verde para éxito
    'warning': '#ffaa00',         # Amarillo para advertencias
    'value': '#00aaaa',           # Cian para valores actuales
    'prompt': '#ffffff bold',     # Blanco bold para prompts
    'menu': '#ffaa00',           # Amarillo para opciones de menú
    'separator': '#333333',       # Gris oscuro para separadores
})

def print_title(title: str) -> None:
    """Imprime un título principal con estilo."""
    print_formatted_text(
        FormattedText([
            ('class:title', f"\n{'=' * 60}\n"),
            ('class:title', f"{title.center(60)}\n"),
            ('class:title', f"{'=' * 60}\n")
        ]),
        style=APP_STYLE
    )

def print_subtitle(subtitle: str) -> None:
    """Imprime un subtítulo con estilo."""
    print_formatted_text(
        FormattedText([
            ('class:subtitle', f"\n{'-' * 40}\n"),
            ('class:subtitle', f"{subtitle.upper()}\n"),
            ('class:subtitle', f"{'-' * 40}\n")
        ]),
        style=APP_STYLE
    )

def print_section_header(section: str) -> None:
    """Imprime encabezado de sección."""
    print_formatted_text(
        FormattedText([
            ('class:subtitle', f"\n📋 {section}\n")
        ]),
        style=APP_STYLE
    )

def print_success(message: str) -> None:
    """Imprime mensaje de éxito."""
    print_formatted_text(
        FormattedText([
            ('class:success', f"✅ {message}")
        ]),
        style=APP_STYLE
    )

def print_warning(message: str) -> None:
    """Imprime mensaje de advertencia."""
    print_formatted_text(
        FormattedText([
            ('class:warning', f"⚠️ {message}")
        ]),
        style=APP_STYLE
    )

def print_error(message: str) -> None:
    """Imprime mensaje de error."""
    print_formatted_text(
        FormattedText([
            ('class:error', f"❌ {message}")
        ]),
        style=APP_STYLE
    )

def print_info(message: str) -> None:
    """Imprime mensaje informativo."""
    print_formatted_text(
        FormattedText([
            ('class:question', f"ℹ️ {message}")
        ]),
        style=APP_STYLE
    )

def format_current_value(field_name: str, current_value: Any) -> str:
    """Formatea valor actual para mostrar en prompts."""
    if current_value is None or current_value == "":
        return f"{field_name}"
    else:
        return f"{field_name} (actual: {current_value})"

# Dentro de cli_helpers.py

def format_prompt_with_hint(prompt_text: str, hint: str = "", current_value: Any = None) -> FormattedText:
    """Crea un prompt formateado con pista y valor actual (versión corregida)."""
    parts = []
    # Etiqueta principal del prompt
    prompt_label = f"{prompt_text}"

    # Añadir valor actual si existe y no está vacío
    if current_value is not None and str(current_value).strip() != "":
        parts.append(('class:question', f"{prompt_label} "))
        parts.append(('class:value', f"[actual: {current_value}]"))
    else:
        # Si no hay valor actual, solo la etiqueta
        parts.append(('class:question', prompt_label))

    # Añadir la pista si existe y no está vacía, ANTES de los dos puntos
    if hint and hint.strip():
        parts.append(('class:hint', f" ({hint.strip()})")) # strip() para eliminar espacios extra

    # Añadir los dos puntos al final
    parts.append(('class:question', ": "))

    return FormattedText(parts)

def create_menu_options(options: Dict[str, str], title: str = "Opciones disponibles") -> FormattedText:
    """Crea menú de opciones formateado."""
    parts = [
        ('class:subtitle', f"\n{title}:\n")
    ]
    
    for key, description in options.items():
        parts.extend([
            ('class:menu', f"  {key}. "),
            ('class:question', f"{description}\n")
        ])
    
    parts.append(('class:question', "\nSeleccione una opción: "))
    return FormattedText(parts)

def display_profile_summary(profile) -> None:
    """
    ✅ CORREGIDO: Muestra resumen del perfil SIN validate_data().
    
    Esta función ya no llama a profile.validate_data() porque 
    ese método no existe en la clase AthleteProfile actualizada.
    """
    from .models import AthleteProfile
    
    print_subtitle("RESUMEN DEL PERFIL")
    
    # Información básica
    if profile.name:
        print_formatted_text(
            FormattedText([
                ('class:question', "👤 Atleta: "),
                ('class:value', f"{profile.name}")
            ]),
            style=APP_STYLE
        )
    
    if profile.age and profile.gender:
        print_formatted_text(
            FormattedText([
                ('class:question', "📊 Perfil: "),
                ('class:value', f"{profile.gender}, {profile.age} años")
            ]),
            style=APP_STYLE
        )
    
    if profile.height_cm and profile.weight_kg:
        from .calculations import calculate_bmi
        bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
        print_formatted_text(
            FormattedText([
                ('class:question', "📏 Físico: "),
                ('class:value', f"{profile.height_cm} cm, {profile.weight_kg} kg (BMI: {bmi:.1f})")
            ]),
            style=APP_STYLE
        )
    
    # Métricas fisiológicas
    physio_parts = []
    if profile.max_hr:
        physio_parts.append(f"FCmáx: {profile.max_hr} ppm")
    if profile.resting_hr:
        physio_parts.append(f"FCrep: {profile.resting_hr} ppm")
    if profile.vo2_max:
        physio_parts.append(f"VO2máx: {profile.vo2_max} ml/kg/min")
    
    if physio_parts:
        print_formatted_text(
            FormattedText([
                ('class:question', "💓 Fisiología: "),
                ('class:value', ", ".join(physio_parts))
            ]),
            style=APP_STYLE
        )
    
    # Entrenamiento
    training_parts = []
    if profile.avg_weekly_km:
        training_parts.append(f"{profile.avg_weekly_km} km/semana")
    if profile.training_days_per_week:
        training_parts.append(f"{profile.training_days_per_week} días")
    
    if training_parts:
        print_formatted_text(
            FormattedText([
                ('class:question', "🏃 Entrenamiento: "),
                ('class:value', ", ".join(training_parts))
            ]),
            style=APP_STYLE
        )
    
    # ✅ NUEVOS CAMPOS TÉCNICOS en el resumen
    experience_parts = []
    if hasattr(profile, 'running_experience_years') and profile.running_experience_years:
        experience_parts.append(f"Experiencia: {profile.running_experience_years} años")
    if hasattr(profile, 'current_training_period') and profile.current_training_period:
        experience_parts.append(f"Período actual: {profile.current_training_period}")
    if hasattr(profile, 'competitive_level') and profile.competitive_level:
        experience_parts.append(f"Nivel: {profile.competitive_level}")
    
    if experience_parts:
        print_formatted_text(
            FormattedText([
                ('class:question', "🎯 Experiencia: "),
                ('class:value', ", ".join(experience_parts))
            ]),
            style=APP_STYLE
        )
    
    # Objetivo principal
    if profile.main_objective:
        obj = profile.main_objective
        print_formatted_text(
            FormattedText([
                ('class:question', "🎯 Objetivo: "),
                ('class:value', f"{obj.name} ({obj.date})")
            ]),
            style=APP_STYLE
        )
        
        if obj.goal_time:
            from .calculations import format_distance_for_display
            distance_display = format_distance_for_display(obj.distance_km)
            print_formatted_text(
                FormattedText([
                    ('class:question', "⏱️ Meta: "),
                    ('class:value', f"{obj.goal_time} en {distance_display}")
                ]),
                style=APP_STYLE
            )
    
    # Marcas personales
    if profile.personal_bests:
        pb_list = []
        for distance, time in profile.personal_bests.items():
            if time:
                display_name = distance.replace('_', ' ').title()
                pb_list.append(f"{display_name}: {time}")
        
        if pb_list:
            print_formatted_text(
                FormattedText([
                    ('class:question', "🏆 Marcas: "),
                    ('class:value', ", ".join(pb_list))
                ]),
                style=APP_STYLE
            )
    
    # Estado de completitud
    print("")
    if profile.is_complete():
        print_success("Perfil completo y listo para generar plan de entrenamiento")
    else:
        print_warning("Perfil incompleto - faltan datos esenciales")
    
    # ✅ ELIMINADO: Sección de validación que llamaba a validate_data()
    # Esta parte causaba el error porque profile.validate_data() no existe
    # errors = profile.validate_data()  # ❌ LÍNEA PROBLEMÁTICA ELIMINADA
    # if errors: ...  # ❌ CÓDIGO ELIMINADO

def display_validation_errors(errors: List[str]) -> None:
    """Muestra errores de validación con formato."""
    if not errors:
        return
        
    print_error("Se encontraron los siguientes problemas:")
    for error in errors:
        print_formatted_text(
            FormattedText([
                ('class:error', f"  • {error}")
            ]),
            style=APP_STYLE
        )

def display_progress_bar(current: int, total: int, description: str = "") -> None:
    """Muestra barra de progreso simple."""
    if total == 0:
        return
    
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    progress_text = f"Progreso: |{bar}| {percentage:.0f}% "
    if description:
        progress_text += f"({description})"
    
    print_formatted_text(
        FormattedText([
            ('class:question', progress_text)
        ]),
        style=APP_STYLE
    )

def confirm_action(message: str, default: bool = False) -> bool:
    """Solicita confirmación del usuario."""
    from prompt_toolkit import prompt
    from .validators import yes_no_validator
    
    default_text = " (S/n)" if default else " (s/N)"
    
    try:
        response = prompt(
            format_prompt_with_hint(
                message + default_text,
                "S/Sí para confirmar, N/No para cancelar"
            ),
            validator=yes_no_validator,
            style=APP_STYLE
        ).strip().lower()
        
        if not response:
            return default
        
        return response in ['sí', 'si', 's', 'yes', 'y', '1', 'true']
        
    except (KeyboardInterrupt, EOFError):
        return False

def display_welcome_message() -> None:
    """Muestra mensaje de bienvenida de la aplicación."""
    print_title("RUNNING Fit-Tech")
    print_formatted_text(
        FormattedText([
            ('class:subtitle', "Aplicación de Entrenamiento para Corredores con IA\n"),
            ('class:question', "Transforme sus datos en planes de entrenamiento personalizados\n"),
            ('class:hint', f"Sesión iniciada: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        ]),
        style=APP_STYLE
    )

def display_completion_message(section_name: str) -> None:
    """
    Muestra mensaje de finalización de sección SIN guardado automático.
    CORREGIDO: El mensaje ahora insta al guardado manual.
    """
    print_formatted_text(
        FormattedText([
            ('class:success', f"\n✅ Sección '{section_name}' completada correctamente\n"),
            ('class:warning', "⚠️ Recuerde guardar los cambios usando la opción 8\n")
        ]),
        style=APP_STYLE
    )

def display_injury_summary(injuries: List) -> None:
    """Muestra resumen de lesiones registradas."""
    if not injuries:
        print_info("No hay lesiones registradas")
        return
    
    print_section_header(f"Lesiones Registradas ({len(injuries)})")
    for i, injury in enumerate(injuries, 1):
        print_formatted_text(
            FormattedText([
                ('class:menu', f"{i}. "),
                ('class:value', f"{injury.type}"),
                ('class:question', f" ({injury.date_approx}) - "),
                ('class:hint', f"{injury.recovery_desc}")
            ]),
            style=APP_STYLE
        )

def display_race_summary(races: List) -> None:
    """Muestra resumen de carreras registradas."""
    if not races:
        print_info("No hay carreras intermedias registradas")
        return
    
    print_section_header(f"Carreras Intermedias ({len(races)})")
    for i, race in enumerate(races, 1):
        from .calculations import format_distance_for_display
        distance_display = format_distance_for_display(race.distance_km)
        
        print_formatted_text(
            FormattedText([
                ('class:menu', f"{i}. "),
                ('class:value', f"{race.name}"),
                ('class:question', f" - {distance_display} "),
                ('class:hint', f"({race.date})")
            ]),
            style=APP_STYLE
        )
        
        if race.goal_time:
            print_formatted_text(
                FormattedText([
                    ('class:question', "     Meta: "),
                    ('class:value', f"{race.goal_time}")
                ]),
                style=APP_STYLE
            )

def clear_screen() -> None:
    """Limpia la pantalla de la terminal."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')