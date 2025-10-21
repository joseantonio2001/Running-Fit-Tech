"""
Main Entry Point - RUNNING Fit-Tech Application (Actualizado Fase 5)

Punto de entrada de la aplicación CLI. Maneja argumentos de línea de comandos
y orquesta la experiencia de usuario, incluyendo:
- CLI interactiva (Fase 2)
- Generación de Ficha Técnica (Fase 3)
- Generación de Plan de Entrenamiento (Fase 5)
"""

import argparse
from pathlib import Path
import sys
from typing import Optional


def main():
    """Punto de entrada principal con integración de Fase 5."""
    parser = argparse.ArgumentParser(description="RUNNING Fit-Tech - AI-Powered Running Training Assistant")
    
    # Argumentos existentes
    parser.add_argument("--load", type=str, help="Cargar archivo de perfil JSON específico")
    parser.add_argument("--generate-outputs", action="store_true", help="Generar Ficha Técnica (PDF/JSON)")
    parser.add_argument("--demo", action="store_true", help="Ejecutar demo con datos de muestra")
    
    # --- NUEVO ARGUMENTO FASE 5 ---
    parser.add_argument(
        "--generate-plan",
        action="store_true",
        help="Generar Plan de Entrenamiento (PDF/JSON/MD) usando IA"
    )
    
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directorio de salida para archivos generados")
    
    args = parser.parse_args()
    
    # Importaciones diferidas para mejorar velocidad de arranque
    from .cli_helpers import print_success, print_error, print_info, print_title
    from .persistence import load_profile, has_existing_profile
    from .cli import start_interactive_cli
    from .outputgen import generate_outputs, validate_profile_completeness, generate_plan_outputs
    
    # --- NUEVA IMPORTACIÓN FASE 5 ---
    from .ai_interface import generate_training_plan
    
    print_title("RUNNING Fit-Tech")
    print_info("AI-Powered Training Assistant for Runners\n")
    
    try:
        profile = None
        
        # --- NUEVO MODO: GENERAR PLAN (FASE 5) ---
        if args.generate_plan:
            print_info("🤖 Modo de Generación de Plan de Entrenamiento activado\n")
            
            profile = _load_profile_for_generation(args.load)
            if not profile:
                return
            
            # Validar perfil antes de llamar a la IA
            is_valid, missing = validate_profile_completeness(profile)
            if not is_valid:
                _print_validation_errors(missing)
                return
            
            print_info(f"🎯 Preparando generación de plan para: {profile.name}")
            
            # 1. Llamar a la IA (Fase 5)
            plan_data = generate_training_plan(profile)
            
            if plan_data:
                # 2. Generar archivos de salida del plan (Fase 5)
                success, files = generate_plan_outputs(
                    plan_data['plan_markdown'],
                    plan_data['plan_structured'],
                    profile.name,
                    args.output_dir
                )
                if success:
                    print_info(f"\n🚀 ¡Plan de entrenamiento generado exitosamente en '{args.output_dir}'!")
                else:
                    print_error("❌ Error al guardar los archivos del plan.")
            else:
                print_error("❌ No se pudo generar el plan de entrenamiento desde la IA.")
            
            return # Salir después de generar el plan

        # --- MODO: GENERAR FICHA TÉCNICA (FASE 3) ---
        elif args.generate_outputs:
            print_info("📄 Modo de Generación de Ficha Técnica activado\n")
            
            profile = _load_profile_for_generation(args.load)
            if not profile:
                return
            
            is_valid, missing = validate_profile_completeness(profile)
            if not is_valid:
                _print_validation_errors(missing)
                return
                
            print_info(f"🎯 Generando Ficha Técnica para: {profile.name}")
            
            success, pdf_path, json_path = generate_outputs(profile, args.output_dir)
            
            if success:
                print_success(f"✅ Ficha PDF generada: {pdf_path}")
                print_success(f"✅ Ficha JSON generada: {json_path}")
            else:
                print_error("❌ Error al generar las salidas de la Ficha Técnica")
            
            return # Salir después de generar ficha

        # --- MODO: DEMO ---
        elif args.demo:
            profile = _load_demo_profile()
            print_success("Perfil de Demo cargado")
            # (El flujo continuará al modo interactivo con este perfil)

        # --- MODO: INTERACTIVO (POR DEFECTO) ---
        
        # Cargar perfil si se especificó --load, si no, CLI se encarga
        loaded_profile = None
        if args.load:
            loaded_profile = _load_specific_profile(args.load)
            print_success(f"Perfil cargado desde: {args.load}")
        
        # Iniciar CLI interactiva
        # (Si loaded_profile es None, la CLI cargará por defecto o creará uno)
        profile = start_interactive_cli(loaded_profile)

        print_info("\n👋 Saliendo de RUNNING Fit-Tech. ¡Hasta pronto!")

    except KeyboardInterrupt:
        print_info("\n\nAplicación interrumpida por el usuario. Adiós.")
        sys.exit(0)
    except Exception as e:
        print_error(f"❌ Error fatal en la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _load_profile_for_generation(load_arg: Optional[str]):
    """Carga un perfil para modos de generación (--generate-plan o --generate-outputs)."""
    from .persistence import load_profile, has_existing_profile
    from .cli_helpers import print_error, print_info

    if load_arg:
        # Cargar perfil específico
        profile = _load_specific_profile(load_arg)
        if not profile:
            print_error(f"No se pudo cargar el perfil desde {load_arg}")
            return None
    else:
        # Cargar perfil por defecto
        if not has_existing_profile():
            print_error("❌ No se encontró 'athlete_profile.json' por defecto.")
            print_info("   Use el modo interactivo primero para crear un perfil:")
            print_info("   python -m src.runnerapp.main")
            return None
        profile = load_profile()

    if not profile or not profile.name:
        print_error("❌ El perfil cargado es inválido o no tiene nombre.")
        return None
        
    return profile

def _print_validation_errors(missing: list):
    """Imprime errores de validación de perfil."""
    from .cli_helpers import print_error, print_info
    print_error("❌ El perfil está incompleto. Faltan datos esenciales:")
    for field in missing:
        print_error(f"     - {field}")
    print_info("\nComplete el perfil usando el modo interactivo:")
    print_info("   python -m src.runnerapp.main")

def _load_demo_profile():
    """Carga un perfil de demo para pruebas."""
    from .models import create_empty_profile, Race, TrainingZones
    profile = create_empty_profile()
    profile.name = "Demo Athlete"
    profile.age = 30
    profile.gender = "Masculino"
    profile.height_cm = 180
    profile.weight_kg = 75.0
    profile.max_hr = 190
    profile.resting_hr = 50
    profile.training_zones = TrainingZones(
        zone1_hr="120-134", zone2_hr="134-148", zone3_hr="148-162",
        zone4_hr="162-176", zone5_hr="176-190"
    )
    profile.avg_weekly_km = 40.0
    profile.training_days_per_week = "4"
    profile.running_experience_years = 3.0
    profile.current_training_period = "2 meses"
    profile.available_training_days = "4"
    profile.include_strength_training = True
    profile.personal_bests = {"10k": "00:45:30"}
    profile.main_objective = Race(
        name="Media Maratón de Valencia",
        date="2025-10-26",
        distance_km=21.097,
        goal_time="01:40:00",
        terrain="Llano"
    )
    return profile


def _load_specific_profile(filepath: str):
    """Carga un perfil desde una ruta de archivo específica."""
    from .models import AthleteProfile
    from .cli_helpers import print_error
    import json
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        profile = AthleteProfile.from_dict(data)
        return profile
    except FileNotFoundError:
        print_error(f"Error: Archivo no encontrado en {filepath}")
        return None
    except json.JSONDecodeError:
        print_error(f"Error: El archivo {filepath} no es un JSON válido.")
        return None
    except Exception as e:
        print_error(f"Error inesperado al cargar {filepath}: {e}")
        return None


if __name__ == "__main__":
    main()