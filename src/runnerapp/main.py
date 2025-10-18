"""
Punto de Entrada Principal - RUNNING Fit-Tech

ACTUALIZADO para Fase 2: Integración completa con CLI interactiva.

Este módulo actúa como el controlador principal de la aplicación,
orquestando el flujo entre todos los módulos del sistema según
la arquitectura monolítica local definida.

Funcionalidades actuales (Fase 2):
- CLI interactiva completa para entrada manual de datos
- Carga/guardado robusto del modelo de datos
- Validación integral y normalización automática
- Flujo conversacional modular y a prueba de errores

Fases futuras expandirán este módulo para incluir:
- Generación de outputs PDF/JSON (Fase 3) 
- Integración con Strava (Fase 4)
- Conexión con IA (Fase 5)
"""

import sys
import logging
import argparse
from pathlib import Path

# Importaciones del paquete runnerapp
from .models import AthleteProfile, create_empty_profile, create_sample_profile
from .persistence import (
    save_profile, 
    load_profile, 
    profile_exists, 
    get_profile_info,
    create_profile_template
)
from .cli import start_interactive_cli
from .cli_helpers import (
    print_title, print_subtitle, print_success, print_error, print_info,
    display_profile_summary, clear_screen
)

logger = logging.getLogger(__name__)


def main():
    """
    Función principal de la aplicación.
    
    Fase 2: CLI interactiva completa como experiencia principal.
    Mantiene compatibilidad con modo demo de Fase 1.
    """
    
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='RUNNING Fit-Tech - Aplicación de Entrenamiento para Corredores con IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python -m src.runnerapp.main                    # Modo interactivo (por defecto)
  python -m src.runnerapp.main --demo            # Modo demo (Fase 1)
  python -m src.runnerapp.main --sample          # Crear perfil de muestra
  python -m src.runnerapp.main --template        # Crear plantilla JSON
  python -m src.runnerapp.main --info            # Información del perfil existente
  python -m src.runnerapp.main --load perfil.json  # Cargar desde archivo específico
        """
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true',
        help='Ejecutar modo demo de Fase 1 (crear perfil de muestra y mostrar info)'
    )
    
    parser.add_argument(
        '--sample', 
        action='store_true',
        help='Crear y guardar perfil de muestra (Tomás Solórzano)'
    )
    
    parser.add_argument(
        '--template', 
        action='store_true',
        help='Crear plantilla JSON para usuarios avanzados'
    )
    
    parser.add_argument(
        '--info', 
        action='store_true',
        help='Mostrar información del perfil existente sin cargar CLI'
    )
    
    parser.add_argument(
        '--load', 
        metavar='FILE',
        help='Cargar perfil desde archivo específico'
    )
    
    parser.add_argument(
        '--clear', 
        action='store_true',
        help='Limpiar pantalla al inicio'
    )
    
    args = parser.parse_args()
    
    # Limpiar pantalla si se solicita
    if args.clear:
        clear_screen()
    
    try:
        if args.demo:
            run_demo_mode()
        elif args.sample:
            create_sample_profile_mode()
        elif args.template:
            create_template_mode()
        elif args.info:
            show_profile_info_mode()
        elif args.load:
            run_interactive_mode_with_file(args.load)
        else:
            run_interactive_mode()
            
    except KeyboardInterrupt:
        print_info("\n\n⚡ Aplicación interrumpida por usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error inesperado en aplicación: {e}")
        print_error(f"\n❌ Error crítico: {e}")
        sys.exit(1)


def run_interactive_mode():
    """
    Ejecuta el modo interactivo principal (Fase 2).
    
    Inicia la CLI conversacional completa que permite al usuario
    crear/editar su perfil de atleta de manera guiada.
    """
    print_title("RUNNING Fit-Tech - Modo Interactivo")
    
    print_info("Iniciando experiencia de CLI interactiva...")
    print_info("Use Ctrl+C en cualquier momento para salir de forma segura")
    
    # ✅ Sin perfil existente, usa comportamiento por defecto
    profile = start_interactive_cli(existing_profile=None)
    
    # Finalización
    print_title("Sesión Completada")
    
    if profile and profile.name:
        print_success(f"Perfil de {profile.name} procesado correctamente")
        
        # Mostrar resumen final
        display_profile_summary(profile)
        
        # Estado para próximas fases
        if profile.is_complete():
            print_success("\n✅ Perfil completo y listo para:")
            print_info("  🎯 Fase 3: Generación de PDF y JSON optimizado para IA")
            print_info("  🔗 Fase 4: Integración opcional con Strava")
            print_info("  🤖 Fase 5: Generación de plan de entrenamiento con IA")
        else:
            print_info("\n⚪ Perfil guardado - puede completarse en futuras sesiones")
        
        # Guardar final
        if save_profile(profile):
            print_success("Perfil guardado exitosamente")
        else:
            print_error("Error al guardar perfil")
    
    print_info("\nGracias por usar RUNNING Fit-Tech")


def run_interactive_mode_with_file(filepath: str):
    """Ejecuta modo interactivo cargando desde archivo específico."""
    print_title("RUNNING Fit-Tech - Carga desde Archivo")
    
    try:
        # Cargar perfil desde archivo específico
        profile = load_profile(filepath)
        print_success(f"Perfil cargado desde: {filepath}")
        
        if profile.name:
            print_info(f"Trabajando con perfil de: {profile.name}")
            display_profile_summary(profile)
        
        # ✅ CORRECCIÓN: Pasar el perfil cargado a la CLI
        profile = start_interactive_cli(existing_profile=profile)
        
        # Guardar en ubicación por defecto
        if save_profile(profile):
            print_success("Perfil actualizado guardado en ubicación por defecto")
        
    except Exception as e:
        print_error(f"Error al cargar archivo {filepath}: {e}")
        print_info("Iniciando con perfil nuevo...")
        run_interactive_mode()


def run_demo_mode():
    """
    Ejecuta el modo demo de Fase 1.
    
    Mantiene la funcionalidad original de demostración para
    validar el modelo de datos y persistencia.
    """
    print_title("RUNNING Fit-Tech - Modo Demo (Fase 1)")
    print_info("Ejecutando demostración del modelo de datos y persistencia")
    
    # Verificar si existe perfil existente
    if profile_exists():
        print_success("✓ Perfil existente encontrado")
        
        # Mostrar información del perfil
        info = get_profile_info()
        if "athlete_name" in info and info["athlete_name"]:
            print_info(f"  Atleta: {info['athlete_name']}")
        print_info(f"  Archivo: {info.get('filepath', 'N/A')}")
        print_info(f"  Tamaño: {info.get('size_bytes', 0)} bytes")
        
        # Cargar perfil existente
        profile = load_profile()
        print_success(f"Perfil cargado: {profile.name or 'Sin nombre'}")
        
    else:
        print_info("⚪ No se encontró perfil existente")
        print_info("Creando perfil de muestra basado en documentación...")
        
        # Crear perfil de muestra (Tomás Solórzano del documento)
        profile = create_sample_profile()
        print_success(f"Perfil de muestra creado: {profile.name}")
    
    # Mostrar resumen del perfil
    display_profile_summary(profile)
    
    # Validar datos
    print_subtitle("VALIDACIÓN DE DATOS")
    
    validation_errors = profile.validate_data()
    if validation_errors:
        print_error("⚠️  Errores encontrados:")
        for error in validation_errors:
            print_error(f"  - {error}")
    else:
        print_success("✓ Todos los datos son válidos")
    
    # Verificar completitud
    if profile.is_complete():
        print_success("✓ Perfil completo para generar plan de entrenamiento")
    else:
        print_info("⚪ Perfil incompleto - necesita más datos para generar plan")
    
    # Guardar perfil
    print_subtitle("PERSISTENCIA")
    
    if save_profile(profile):
        print_success("✓ Perfil guardado exitosamente")
        
        # Mostrar estructura JSON generada
        profile_dict = profile.to_dict()
        print_success(f"✓ Estructura JSON generada con {len(profile_dict)} secciones principales:")
        for key in profile_dict.keys():
            print_info(f"  - {key}")
            
    else:
        print_error("❌ Error al guardar perfil")
    
    # Crear plantilla para usuarios avanzados
    print_subtitle("HERRAMIENTAS ADICIONALES")
    
    if create_profile_template():
        print_success("✓ Plantilla 'profile_template.json' creada para usuarios avanzados")
    
    print_title("DEMO COMPLETADO")
    print_success("Modelo de datos y persistencia funcionando correctamente")
    print_info("Puede continuar con el modo interactivo usando: python -m src.runnerapp.main")


def create_sample_profile_mode():
    """Crea y guarda perfil de muestra."""
    print_title("Crear Perfil de Muestra")
    
    profile = create_sample_profile()
    
    if save_profile(profile):
        print_success(f"Perfil de muestra '{profile.name}' creado y guardado")
        display_profile_summary(profile)
    else:
        print_error("Error al guardar perfil de muestra")


def create_template_mode():
    """Crea plantilla JSON para usuarios avanzados."""
    print_title("Crear Plantilla JSON")
    
    if create_profile_template():
        print_success("Plantilla 'profile_template.json' creada exitosamente")
        print_info("Puede editar este archivo y cargarlo con: --load profile_template.json")
    else:
        print_error("Error al crear plantilla")


def show_profile_info_mode():
    """Muestra información del perfil existente."""
    print_title("Información del Perfil")
    
    if profile_exists():
        info = get_profile_info()
        profile = load_profile()
        
        print_success("Perfil encontrado:")
        print_info(f"  📄 Archivo: {info.get('filepath', 'N/A')}")
        print_info(f"  📊 Tamaño: {info.get('size_bytes', 0)} bytes")
        
        if profile.name:
            print_info(f"  👤 Atleta: {profile.name}")
        
        if 'generated_at' in info:
            print_info(f"  📅 Generado: {info['generated_at']}")
        
        print_info(f"  ✅ Completo: {'Sí' if profile.is_complete() else 'No'}")
        
        errors = profile.validate_data()
        print_info(f"  🔍 Válido: {'Sí' if not errors else f'No ({len(errors)} errores)'}")
        
        display_profile_summary(profile)
        
    else:
        print_info("No se encontró perfil existente")
        print_info("Puede crear uno usando el modo interactivo o --sample")


def demo_serialization():
    """
    Función de demostración para validar serialización/deserialización.
    
    Mantiene funcionalidad de Fase 1 para testing.
    """
    print_subtitle("DEMOSTRACIÓN DE SERIALIZACIÓN")
    
    # Crear perfil de prueba
    original_profile = create_sample_profile()
    print_success(f"Perfil original: {original_profile.name}")
    
    # Serializar a diccionario
    profile_dict = original_profile.to_dict()
    print_success(f"✓ Serializado a diccionario con {len(profile_dict)} secciones")
    
    # Deserializar de vuelta
    restored_profile = AthleteProfile.from_dict(profile_dict)
    print_success(f"✓ Deserializado de vuelta: {restored_profile.name}")
    
    # Verificar integridad
    integrity_checks = [
        original_profile.name == restored_profile.name,
        original_profile.age == restored_profile.age,
        original_profile.max_hr == restored_profile.max_hr,
        len(original_profile.injuries) == len(restored_profile.injuries),
        original_profile.main_objective is not None and restored_profile.main_objective is not None
    ]
    
    if all(integrity_checks):
        print_success("✓ Integridad de datos verificada - serialización correcta")
    else:
        print_error("❌ Pérdida de integridad detectada en serialización")


if __name__ == "__main__":
    # Configurar logging para ejecución directa
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    main()
