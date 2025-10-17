# RUNNING Fit-Tech - Aplicación de Entrenamiento para Corredores con IA

> Herramienta de ingeniería de prompts sofisticada que transforma datos del corredor en planes de entrenamiento de calidad profesional mediante IA.

## Visión del Producto

La aplicación actúa como un puente de alta fidelidad entre atletas de resistencia y entrenadores virtuales de IA, consolidando información de rendimiento, métricas fisiológicas y contexto personal en una **Ficha Técnica** estandarizada que desbloquea el potencial de modelos de lenguaje para generar planes de entrenamiento personalizados y adaptativos.

## Estado Actual: Fase 1 - Fundación Completa ✅

### Funcionalidades Implementadas

- **✅ Modelo de Datos Central**: Dataclasses Python tipadas que implementan la especificación completa de la Ficha Técnica
- **✅ Sistema de Persistencia**: Módulo robusto para guardar/cargar perfiles con validación y manejo de errores
- **✅ Arquitectura Modular**: Estructura `src layout` preparada para escalabilidad
- **✅ Validación de Datos**: Verificación de integridad fisiológica y coherencia
- **✅ Documentación Completa**: Código auto-documentado con propósito de cada componente

### Arquitectura del Sistema

```
Flujo de Datos Lineal (Monolítico Local):
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Entrada CLI   │───▶│ Adquisición de  │───▶│  Persistencia   │
│                 │    │     Datos       │    │  Local (JSON)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Interfaz con IA │◀───│ Generación de   │◀───│ Motor de Lógica │
│                 │    │    Salidas      │    │  y Cálculo      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Configuración Rápida

### Prerrequisitos
- Python 3.11 o superior
- Git (para control de versiones)

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd runner-app

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/MacOS:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python -m src.runnerapp.main
```

### Ejecución con Demo Completo

```bash
python -m src.runnerapp.main --demo
```

## Modelo de Datos - Ficha Técnica

La **Ficha Técnica** es el corazón del sistema, diseñada como prompt estructurado para IA:

### Secciones Principales

| Sección | Propósito | Campos Clave |
|---------|-----------|--------------|
| **Resumen del Atleta** | Identificación y timestamp | `name`, `generated_at` |
| **Información Personal** | Datos demográficos básicos | `age`, `gender`, `height_cm`, `weight_kg` |
| **Métricas Fisiológicas** | Perfil de resistencia y potencial | `max_hr`, `resting_hr`, `vo2_max`, `lactate_threshold_bpm` |
| **Historial de Lesiones** | Patrones de riesgo y adaptaciones | `injuries[]` con tipo, fecha, recuperación |
| **Contexto de Entrenamiento** | Disponibilidad y preferencias | `avg_weekly_km`, `training_days_per_week`, `quality_session_preference` |
| **Datos de Rendimiento** | Marcas personales y zonas | `personal_bests{}`, `training_zones` |
| **Objetivos de Carrera** | Metas competitivas | `main_objective`, `intermediate_races[]` |

### Ejemplo de Salida JSON Estructurada

```json
{
  "athlete_summary": {
    "name": "Tomás Solórzano",
    "generated_at": "2024-05-24T10:00:00Z"
  },
  "physiological_metrics": {
    "meta_description": "Métricas fisiológicas clave que definen el perfil de resistencia y el potencial del atleta.",
    "max_hr": 184,
    "resting_hr": 41,
    "vo2_max": 60.0,
    "lactate_threshold_bpm": 179
  },
  "race_goals": {
    "main_objective": {
      "name": "Media Maratón de Valencia",
      "date": "2024-11-30",
      "distance_km": 21.097,
      "goal_time": "01:28:00",
      "terrain": "Llano"
    }
  }
}
```

## Principios de Diseño

### 1. Single Source of Truth
- El archivo `athlete_profile.json` es la fuente canónica de datos
- Strava actúa como "pre-rellenado" controlado por el usuario
- Usuario mantiene control total de su perfil

### 2. Ingeniería de Prompts Incorporada
- Claves JSON descriptivas y auto-explicativas
- Meta-descripciones que guían la interpretación de la IA
- Anidamiento lógico que crea contexto estructurado

### 3. Robustez y Escalabilidad
- Validación temprana con dataclasses tipadas
- Manejo de errores sin bloqueo de flujo
- API modular que facilita migración futura

## Hoja de Ruta - Próximas Fases

### Fase 2: CLI Interactiva (Próxima) 🔄
- Cuestionario guiado con `prompt-toolkit`
- Normalización y validación de entradas en tiempo real
- Manejo elegante de datos opcionales

### Fase 3: Generación de Salidas 📄
- PDF profesional con `ReportLab`
- JSON optimizado para IA
- Cálculo de zonas de entrenamiento (Fórmula Karvonen)

### Fase 4: Integración Strava 🔗
- Autenticación OAuth2 segura para CLI
- Pre-rellenado automático de marcas personales
- Gestión inteligente de tokens de refresco

### Fase 5: Entrenador de IA 🤖
- Integración con API de Perplexity
- Construcción de prompts de alta calidad
- Generación de planes personalizados

## Tecnologías Clave

| Componente | Librería | Justificación |
|------------|----------|---------------|
| **CLI Interactiva** | `prompt-toolkit` | Control total para experiencia conversacional rica |
| **Generación PDF** | `ReportLab` | Control granular para documentos profesionales |
| **Cliente Strava** | `stravalib` | Cliente completo con OAuth2 y gestión de tokens |
| **HTTP Requests** | `requests` | Estándar industria para comunicación API |
| **Modelo de Datos** | `dataclasses` | Tipado estático y validación automática |

## Testing y Validación

```bash
# Ejecutar tests (cuando estén implementados)
pytest tests/

# Validación de tipos
mypy src/

# Formateo de código
black src/ tests/
```

## Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para detalles.

## Soporte

Para preguntas, issues o sugerencias:
- 📧 Email: soporte@fit-tech.com
- 🐛 Issues: [GitHub Issues](https://github.com/fit-tech/runner-app/issues)
- 📖 Documentación: [Wiki del Proyecto](https://github.com/fit-tech/runner-app/wiki)

---

**RUNNING Fit-Tech** - Transformando el entrenamiento de resistencia con IA de próxima generación.