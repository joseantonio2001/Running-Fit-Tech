"""
Punto de Entrada Principal - RUNNING Fit-Tech

Este módulo actúa como el controlador principal de la aplicación,
orquestando el flujo entre todos los módulos del sistema según
la arquitectura monolítica local definida.

En la Fase 1, implementa funcionalidad básica para:
- Demostrar carga/guardado del modelo de datos
- Validar la implementación del sistema de persistencia
- Proporcionar base sólida para desarrollo de fases posteriores

Fases futuras expandirán este módulo para incluir:
- CLI interactiva completa (Fase 2)
- Generación de outputs PDF/JSON (Fase 3) 
- Integración con Strava (Fase 4)
- Conexión con IA (Fase 5)
"""

import sys
import logging
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

logger = logging.getLogger(__name__)


def main():
    """
    Función principal de la aplicación.
    
    En Fase 1, demuestra funcionalidad básica del modelo de datos
    y persistencia. En fases posteriores, evolucionará para incluir
    el flujo completo de la CLI interactiva.
    """
    print("=" * 60)
    print("RUNNING Fit-Tech - Aplicación de Entrenamiento con IA")
    print("Fase 1: Fundación del Proyecto y Modelo de Datos Central")
    print("=" * 60)
    print()
    
    # Verificar si existe perfil existente
    if profile_exists():
        print("✓ Perfil existente encontrado")
        
        # Mostrar información del perfil
        info = get_profile_info()
        if "athlete_name" in info and info["athlete_name"]:
            print(f"  Atleta: {info['athlete_name']}")
        print(f"  Archivo: {info.get('filepath', 'N/A')}")
        print(f"  Tamaño: {info.get('size_bytes', 0)} bytes")
        print()
        
        # Cargar perfil existente
        profile = load_profile()
        print(f"Perfil cargado: {profile.name or 'Sin nombre'}")
        
    else:
        print("⚪ No se encontró perfil existente")
        print("Creando perfil de muestra basado en documentación...")
        print()
        
        # Crear perfil de muestra (Tomás Solórzano del documento)
        profile = create_sample_profile()
        print(f"Perfil de muestra creado: {profile.name}")
    
    # Mostrar resumen del perfil
    print("\n" + "-" * 40)
    print("RESUMEN DEL PERFIL")
    print("-" * 40)
    
    print(f"Nombre: {profile.name}")
    print(f"Edad: {profile.age} años" if profile.age else "Edad: No especificada")
    print(f"Género: {profile.gender}" if profile.gender else "Género: No especificado")
    
    if profile.height_cm and profile.weight_kg:
        print(f"Físico: {profile.height_cm} cm, {profile.weight_kg} kg")
    
    # Métricas fisiológicas
    physio_metrics = []
    if profile.max_hr:
        physio_metrics.append(f"FCmáx: {profile.max_hr} ppm")
    if profile.resting_hr:
        physio_metrics.append(f"FCrep: {profile.resting_hr} ppm")
    if profile.vo2_max:
        physio_metrics.append(f"VO2máx: {profile.vo2_max} ml/kg/min")
    
    if physio_metrics:
        print("Métricas fisiológicas: " + ", ".join(physio_metrics))
    
    # Contexto de entrenamiento
    if profile.avg_weekly_km:
        print(f"Volumen actual: {profile.avg_weekly_km} km/semana")
    if profile.training_days_per_week:
        print(f"Días de entrenamiento: {profile.training_days_per_week}")
    
    # Objetivo principal
    if profile.main_objective:
        obj = profile.main_objective
        print(f"Objetivo: {obj.name} ({obj.date})")
        if obj.goal_time:
            print(f"  Meta: {obj.goal_time} en {obj.distance_km} km")
    
    # Marcas personales
    pb_list = []
    for distance, time in profile.personal_bests.items():
        if time:
            pb_list.append(f"{distance}: {time}")
    
    if pb_list:
        print("Marcas personales: " + ", ".join(pb_list))
    
    # Validar datos
    print("\n" + "-" * 40)
    print("VALIDACIÓN DE DATOS")
    print("-" * 40)
    
    validation_errors = profile.validate_data()
    if validation_errors:
        print("⚠️  Errores encontrados:")
        for error in validation_errors:
            print(f"  - {error}")
    else:
        print("✓ Todos los datos son válidos")
    
    # Verificar completitud
    if profile.is_complete():
        print("✓ Perfil completo para generar plan de entrenamiento")
    else:
        print("⚪ Perfil incompleto - necesita más datos para generar plan")
    
    # Guardar perfil
    print("\n" + "-" * 40)
    print("PERSISTENCIA")
    print("-" * 40)
    
    if save_profile(profile):
        print("✓ Perfil guardado exitosamente")
        
        # Mostrar estructura JSON generada
        profile_dict = profile.to_dict()
        print(f"✓ Estructura JSON generada con {len(profile_dict)} secciones principales:")
        for key in profile_dict.keys():
            print(f"  - {key}")
            
    else:
        print("❌ Error al guardar perfil")
    
    # Crear plantilla para usuarios avanzados
    print("\n" + "-" * 40)
    print("HERRAMIENTAS ADICIONALES")
    print("-" * 40)
    
    if create_profile_template():
        print("✓ Plantilla 'profile_template.json' creada para usuarios avanzados")
    
    print("\n" + "=" * 60)
    print("FASE 1 COMPLETADA EXITOSAMENTE")
    print("Base sólida establecida para desarrollo de fases posteriores")
    print("=" * 60)


def demo_serialization():
    """
    Función de demostración para validar serialización/deserialización.
    
    Crea un perfil, lo serializa a JSON, lo deserializa y verifica
    que los datos se mantienen íntegros en el proceso.
    """
    print("\n" + "=" * 50)
    print("DEMOSTRACIÓN DE SERIALIZACIÓN")
    print("=" * 50)
    
    # Crear perfil de prueba
    original_profile = create_sample_profile()
    print(f"Perfil original: {original_profile.name}")
    
    # Serializar a diccionario
    profile_dict = original_profile.to_dict()
    print(f"✓ Serializado a diccionario con {len(profile_dict)} secciones")
    
    # Deserializar de vuelta
    restored_profile = AthleteProfile.from_dict(profile_dict)
    print(f"✓ Deserializado de vuelta: {restored_profile.name}")
    
    # Verificar integridad
    integrity_checks = [
        original_profile.name == restored_profile.name,
        original_profile.age == restored_profile.age,
        original_profile.max_hr == restored_profile.max_hr,
        len(original_profile.injuries) == len(restored_profile.injuries),
        original_profile.main_objective is not None and restored_profile.main_objective is not None
    ]
    
    if all(integrity_checks):
        print("✓ Integridad de datos verificada - serialización correcta")
    else:
        print("❌ Pérdida de integridad detectada en serialización")
    
    print("=" * 50)


if __name__ == "__main__":
    # Configurar logging para ejecución directa
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        main()
        
        # Ejecutar demostración adicional si se solicita
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            demo_serialization()
            
    except KeyboardInterrupt:
        print("\n\n⚡ Aplicación interrumpida por usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error inesperado en aplicación: {e}")
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)
