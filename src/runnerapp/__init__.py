"""
RUNNING Fit-Tech - Aplicación de Entrenamiento para Corredores con IA

Aplicación CLI que actúa como herramienta de ingeniería de prompts sofisticada
para atletas de resistencia, transformando datos del corredor en una Ficha Técnica
estructurada que habilita planes de entrenamiento de calidad profesional mediante IA.

Arquitectura: Sistema monolítico local con flujo de datos lineal
- Entrada de Usuario (CLI)
- Módulo de Adquisición de Datos  
- Módulo de Persistencia Local (Single Source of Truth)
- Motor de Lógica y Cálculo
- Módulo de Generación de Salidas
- Módulo de Interfaz con IA

Autor: Arquitecto de Software y Jefe de Producto, Fit-Tech Solutions
Versión: 1.0 - Fase 1: Fundación del Proyecto y Modelo de Datos Central
"""

__version__ = "1.0.0"
__author__ = "Fit-Tech Solutions"
__description__ = "Aplicación de Entrenamiento para Corredores con IA"

# Importaciones principales del paquete
from .models import AthleteProfile, Injury, Race, TrainingZones
from .persistence import save_profile, load_profile

# Configuración de logging básica
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
