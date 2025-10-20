"""
Módulo de Persistencia Local - CORREGIDO: Sin validate_data()

✅ ELIMINADO: profile.validate_data() que no existe en AthleteProfile
✅ CORREGIDO: Compatibilidad con nuevos campos técnicos  
✅ MANTENIDO: Toda la funcionalidad de persistencia robusta
✅ AÑADIDO: Función has_existing_profile() para CLI

Implementa el mecanismo de "Single Source of Truth" de la aplicación,
gestionando el almacenamiento y recuperación del estado del perfil del atleta
en el sistema de archivos local.

Funciones principales:
- save_profile(): Serializa y guarda el perfil como JSON
- load_profile(): Carga y deserializa el perfil desde JSON
- Manejo robusto de errores SIN validación que no existe

La elección de JSON prioriza simplicidad, legibilidad humana y facilidad
de depuración para el MVP. La API modular facilita futura migración a
bases de datos más complejas sin afectar otros módulos.
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional

from .models import AthleteProfile, create_empty_profile

logger = logging.getLogger(__name__)

# Configuración por defecto
DEFAULT_PROFILE_FILENAME = "athlete_profile.json"
DEFAULT_PROFILE_DIR = Path.cwd()

def save_profile(profile: AthleteProfile, filepath: Optional[str] = None) -> bool:
    """
    Guarda el perfil del atleta en formato JSON.
    
    Serializa la instancia de AthleteProfile a un archivo JSON con formato
    legible (indentación) para facilitar inspección manual y depuración.
    
    Args:
        profile: Instancia del perfil del atleta a guardar
        filepath: Ruta del archivo (opcional). Si no se especifica,
                 usa DEFAULT_PROFILE_FILENAME en directorio actual
    
    Returns:
        bool: True si se guardó exitosamente, False si hubo error
    
    Raises:
        Registra errores en el logger pero no re-lanza excepciones
        para mantener robustez en la interfaz de usuario
    """
    if filepath is None:
        filepath = DEFAULT_PROFILE_DIR / DEFAULT_PROFILE_FILENAME
    else:
        filepath = Path(filepath)
    
    try:
        # Crear directorio padre si no existe
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convertir perfil a diccionario estructurado
        profile_dict = profile.to_dict()
        
        # Serializar con formato legible
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile_dict, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Perfil guardado exitosamente en: {filepath}")
        return True
    
    except (IOError, OSError) as e:
        logger.error(f"Error de archivo al guardar perfil en {filepath}: {e}")
        return False
    except (TypeError, ValueError) as e:
        logger.error(f"Error de serialización JSON: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado al guardar perfil: {e}")
        return False

def load_profile(filepath: Optional[str] = None) -> AthleteProfile:
    """
    Carga el perfil del atleta desde archivo JSON.
    
    Si el archivo existe, lo deserializa y reconstruye la instancia de
    AthleteProfile. Si no existe o hay error, devuelve un perfil vacío
    nuevo para permitir continuar el flujo de la aplicación.
    
    ✅ CORREGIDO: Sin llamada a validate_data() que no existe
    
    Args:
        filepath: Ruta del archivo (opcional). Si no se especifica,
                 usa DEFAULT_PROFILE_FILENAME en directorio actual
    
    Returns:
        AthleteProfile: Instancia del perfil cargado o nuevo perfil vacío
    
    Notes:
        - No lanza excepciones, siempre devuelve un perfil válido
        - Registra errores en el logger para depuración
        - Compatible con nuevos campos técnicos añadidos
    """
    if filepath is None:
        filepath = DEFAULT_PROFILE_DIR / DEFAULT_PROFILE_FILENAME
    else:
        filepath = Path(filepath)
    
    # Si el archivo no existe, devolver perfil vacío
    if not filepath.exists():
        logger.info(f"Archivo de perfil no encontrado: {filepath}. Creando perfil nuevo.")
        return create_empty_profile()
    
    try:
        # Cargar y deserializar JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            profile_dict = json.load(f)
        
        # Reconstruir instancia de AthleteProfile
        profile = AthleteProfile.from_dict(profile_dict)
        
        # ✅ ELIMINADO: Validación que no existe
        # validation_errors = profile.validate_data()  # NO EXISTE
        # if validation_errors:
        #     logger.warning(f"Datos cargados contienen errores de validación: {validation_errors}")
        
        logger.info(f"Perfil cargado exitosamente desde: {filepath}")
        return profile
    
    except (IOError, OSError) as e:
        logger.error(f"Error de archivo al cargar perfil desde {filepath}: {e}")
        return create_empty_profile()
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error de formato JSON en {filepath}: {e}")
        return create_empty_profile()
    except Exception as e:
        logger.error(f"Error inesperado al cargar perfil: {e}")
        return create_empty_profile()

def profile_exists(filepath: Optional[str] = None) -> bool:
    """
    Verifica si existe un archivo de perfil en la ruta especificada.
    
    Args:
        filepath: Ruta del archivo (opcional). Si no se especifica,
                 usa DEFAULT_PROFILE_FILENAME en directorio actual
    
    Returns:
        bool: True si el archivo existe y es legible, False en caso contrario
    """
    if filepath is None:
        filepath = DEFAULT_PROFILE_DIR / DEFAULT_PROFILE_FILENAME
    else:
        filepath = Path(filepath)
    
    return filepath.exists() and filepath.is_file()

def backup_profile(profile: AthleteProfile, backup_suffix: Optional[str] = None) -> bool:
    """
    Crea una copia de seguridad del perfil actual.
    
    Útil antes de realizar operaciones que modifiquen datos críticos,
    como integración con Strava o actualizaciones importantes.
    
    Args:
        profile: Perfil a respaldar
        backup_suffix: Sufijo para el nombre del backup (opcional).
                      Si no se especifica, usa timestamp actual
    
    Returns:
        bool: True si el backup se creó exitosamente
    """
    if backup_suffix is None:
        from datetime import datetime
        backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construir nombre del archivo backup
    backup_filename = f"athlete_profile_backup_{backup_suffix}.json"
    backup_filepath = DEFAULT_PROFILE_DIR / backup_filename
    
    return save_profile(profile, str(backup_filepath))

def get_profile_info(filepath: Optional[str] = None) -> dict:
    """
    Obtiene información metadata del archivo de perfil sin cargarlo completo.
    
    Útil para mostrar información rápida en CLI (nombre del atleta,
    última modificación, etc.) sin el overhead de deserialización completa.
    
    Args:
        filepath: Ruta del archivo (opcional)
    
    Returns:
        dict: Información del perfil o diccionario vacío si hay error
    """
    if filepath is None:
        filepath = DEFAULT_PROFILE_DIR / DEFAULT_PROFILE_FILENAME
    else:
        filepath = Path(filepath)
    
    if not filepath.exists():
        return {}
    
    try:
        # Obtener estadísticas del archivo
        stat = filepath.stat()
        file_info = {
            "exists": True,
            "size_bytes": stat.st_size,
            "modified": stat.st_mtime,
            "filepath": str(filepath)
        }
        
        # Intentar extraer nombre del atleta sin cargar perfil completo
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Compatibilidad con diferentes formatos de archivo
            if "name" in data:
                file_info["athlete_name"] = data["name"]
            elif "athlete_summary" in data and "name" in data["athlete_summary"]:
                file_info["athlete_name"] = data["athlete_summary"]["name"]
                
            if "athlete_summary" in data and "generated_at" in data["athlete_summary"]:
                file_info["generated_at"] = data["athlete_summary"]["generated_at"]
                
        except (json.JSONDecodeError, KeyError):
            # Si no se puede extraer nombre, continuar con info básica
            pass
        
        return file_info
    
    except (IOError, OSError):
        return {"exists": False}

def create_profile_template(filepath: Optional[str] = None) -> bool:
    """
    Crea un archivo de plantilla JSON con todos los campos vacíos.
    
    Permite a usuarios avanzados rellenar datos cómodamente en su
    editor de texto preferido antes de cargar en la aplicación.
    
    Args:
        filepath: Ruta donde crear la plantilla (opcional).
                 Por defecto: "profile_template.json"
    
    Returns:
        bool: True si la plantilla se creó exitosamente
    """
    if filepath is None:
        filepath = DEFAULT_PROFILE_DIR / "profile_template.json"
    else:
        filepath = Path(filepath)
    
    # Crear perfil vacío como base para la plantilla
    empty_profile = create_empty_profile()
    
    # Añadir comentarios explicativos en campos clave
    template_dict = empty_profile.to_dict()
    
    # Añadir comentarios como campos especiales (serán ignorados al cargar)
    template_dict["_INSTRUCTIONS"] = {
        "description": "Plantilla para crear perfil de atleta manualmente",
        "usage": "1. Rellena los campos necesarios, 2. Guarda el archivo, 3. Carga en la aplicación",
        "notes": "Los campos null/None son opcionales. Elimina este campo '_INSTRUCTIONS' antes de cargar."
    }
    
    template_dict["_FIELD_EXAMPLES"] = {
        "gender": "Opciones: 'Masculino', 'Femenino', 'Otro'",
        "running_experience_years": "Ejemplos: 5, 2.5, 0.5 (años totales practicando running)",
        "current_training_period": "Ejemplos: '3 semanas', '2 meses', '0 - empezando'",
        "competitive_level": "Opciones: 'RECREATIVO', 'AMATEUR', 'COMPETITIVO', 'PROFESIONAL'",
        "training_days_per_week": "Ejemplos: '4', '5', '4-5'",
        "personal_bests": "Formato: 'HH:MM:SS' (ej: '00:18:30')",
        "date_formats": "Fechas en formato YYYY-MM-DD (ej: '2024-11-30')"
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template_dict, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Plantilla de perfil creada en: {filepath}")
        return True
    
    except (IOError, OSError) as e:
        logger.error(f"Error al crear plantilla en {filepath}: {e}")
        return False

# Funciones de conveniencia para la CLI
def quick_save(profile: AthleteProfile) -> bool:
    """Guarda el perfil usando la ruta por defecto."""
    return save_profile(profile)

def quick_load() -> AthleteProfile:
    """Carga el perfil usando la ruta por defecto."""
    return load_profile()

def has_existing_profile() -> bool:
    """
    ✅ AÑADIDO: Verifica si existe un perfil en la ubicación por defecto.
    
    Esta función es requerida por CLI pero faltaba en persistence.py
    """
    return profile_exists()