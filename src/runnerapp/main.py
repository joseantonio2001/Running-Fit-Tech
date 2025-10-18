"""
Main Entry Point - RUNNING Fit-Tech Application (CORREGIDO)

Entry point for the RUNNING Fit-Tech CLI application with all phases integrated.
Handles command line arguments and orchestrates the complete user experience.
"""

import argparse
from pathlib import Path
import sys


def main():
    """Main entry point with Phase 3 integration."""
    parser = argparse.ArgumentParser(description="RUNNING Fit-Tech - AI-Powered Running Training Assistant")
    parser.add_argument("--load", type=str, help="Load specific profile JSON file")
    parser.add_argument("--generate-outputs", action="store_true", help="Generate PDF and JSON outputs")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory for generated files")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")
    
    args = parser.parse_args()
    
    from .cli_helpers import print_success, print_error, print_info, print_title
    from .persistence import load_profile, has_existing_profile
    from .cli import start_interactive_cli
    from .outputgen import generate_outputs, validate_profile_completeness
    
    print_title("RUNNING Fit-Tech")
    print_info("AI-Powered Training Assistant for Runners\n")
    
    try:
        # Handle different execution modes
        if args.demo:
            profile = _load_demo_profile()
            print_success("Demo profile loaded")
            
        elif args.load:
            profile = _load_specific_profile(args.load)
            print_success(f"Profile loaded from: {args.load}")
            
        elif args.generate_outputs:
            # ✅ CORRECCIÓN: Generate outputs from existing profile
            print_info("Modo de generación de salidas activado\n")
            
            if not has_existing_profile():
                print_error("❌ No existing profile found. Create a profile first using:")
                print_info("   python -m src.runnerapp.main")
                return
            
            profile = load_profile()
            
            if not profile.name:
                print_error("❌ Profile found but invalid (no name)")
                return
            
            # ✅ CORRECCIÓN: Validación con feedback detallado
            is_valid, missing = validate_profile_completeness(profile)
            
            if not is_valid:
                print_error("❌ Profile incomplete for output generation:")
                for field in missing:
                    print_error(f"     - {field}")
                print_info("\nComplete the profile using: python -m src.runnerapp.main")
                return
            
            print_info(f"🎯 Generating outputs for: {profile.name}")
            
            # ✅ CORRECCIÓN: Generar salidas con feedback
            success, pdf_path, json_path = generate_outputs(profile, args.output_dir)
            
            if success:
                print_success(f"✅ PDF generated: {pdf_path}")
                print_success(f"✅ JSON generated: {json_path}")
                print_info("\n🎯 Next steps:")
                print_info("   📄 Review the generated PDF")
                print_info("   🤖 Use the JSON with AI systems")
                print_info("   🏃‍♂️ Start your training plan!")
            else:
                print_error("❌ Failed to generate outputs")
            
            return  # ✅ CORRECCIÓN: Return here to exit after generation
        else:
            # Standard interactive mode
            profile = start_interactive_cli()
        
        # ✅ CORRECCIÓN: Offer output generation after CLI completion (only for CLI mode)
        if profile and profile.name:
            is_valid, missing = validate_profile_completeness(profile)
            
            if is_valid:
                from .cli_helpers import confirm_action
                if confirm_action("¿Desea generar las salidas PDF y JSON ahora?", True):
                    print_info(f"\n🎯 Generando salidas para: {profile.name}")
                    
                    success, pdf_path, json_path = generate_outputs(profile, args.output_dir)
                    
                    if success:
                        print_success(f"✅ PDF generado: {pdf_path}")
                        print_success(f"✅ JSON generado: {json_path}")
                        print_info("\n🎯 Próximos pasos:")
                        print_info("   📄 Revisar el PDF generado")
                        print_info("   🤖 Usar el JSON con sistemas de IA")
                        print_info("   🏃‍♂️ ¡Comenzar tu plan de entrenamiento!")
                    else:
                        print_error("❌ Error al generar salidas")
            else:
                print_info("ℹ️  Perfil incompleto para generar salidas profesionales")
                print_info("   Complete más secciones para obtener mejores resultados")
        
    except KeyboardInterrupt:
        print_info("\n\nApplication interrupted by user")
    except Exception as e:
        print_error(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _load_demo_profile():
    """Load demo profile for testing."""
    from .models import create_empty_profile
    # Create a basic demo profile
    profile = create_empty_profile()
    profile.name = "Demo Athlete"
    profile.age = 25
    profile.gender = "Masculino"
    return profile


def _load_specific_profile(filepath: str):
    """Load profile from specific file path."""
    from .persistence import load_profile
    import json
    
    try:
        # Try to load from specific path
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        from .models import AthleteProfile
        profile = AthleteProfile.from_dict(data)
        return profile
        
    except Exception as e:
        print(f"❌ Error loading profile from {filepath}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()