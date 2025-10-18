# RUNNING Fit-Tech 🏃‍♂️

**Aplicación CLI de Entrenamiento para Corredores con Inteligencia Artificial**

Transforme sus datos personales en planes de entrenamiento científicamente personalizados mediante la recolección inteligente de datos y análisis con IA.

---

## 🎯 **Estado Actual del Proyecto**

### ✅ **FASE 1: MODELO DE DATOS Y PERSISTENCIA - COMPLETADA**
**Base técnica sólida y robusta implementada exitosamente**

- **✅ Modelo de datos completo**: Estructura AthleteProfile como "Single Source of Truth"
- **✅ Persistencia JSON**: Serialización/deserialización completa y robusta  
- **✅ Validaciones integrales**: Validación de tipos, rangos y coherencia de datos
- **✅ Cálculos automáticos**: BMI, zonas de entrenamiento, estimaciones VO2máx
- **✅ Ingeniería de prompts**: JSON optimizado como input estructurado para IA
- **✅ Calidad de producción**: Type hints, documentación completa, manejo de errores

### ✅ **FASE 2: CLI INTERACTIVA - COMPLETADA**
**Experiencia de usuario completa y profesional implementada exitosamente**

- **✅ CLI conversacional completa**: 6 secciones modulares de entrada de datos
- **✅ Validación en tiempo real**: prompt-toolkit con validadores personalizados
- **✅ Control completo de guardado**: Usuario controla cuándo guardar/descartar cambios
- **✅ Indicadores de progreso**: Visualización en tiempo real de completitud de secciones
- **✅ Manejo elegante de interrupciones**: CTRL+C con opciones de guardar/descartar
- **✅ Navegación intuitiva**: Flujo de usuario profesional con colores y formato
- **✅ Normalización de datos**: Acepta múltiples formatos de entrada de usuario
- **✅ Carga de archivos específicos**: Soporte completo para `--load archivo.json`
- **✅ Experiencia de producción**: Mensajes claros, recuperación de errores, UX pulida

### 🔄 **FASE 3: GENERACIÓN DE SALIDAS - EN PLANIFICACIÓN**
**Sistema de outputs profesionales con PDF y JSON optimizado**

- **📋 PDF Professional**: ReportLab con diseño profesional y datos completos
- **🤖 JSON Optimizado para IA**: Prompt estructurado y auto-explicativo
- **📊 Cálculos Avanzados**: Zonas de entrenamiento detalladas y métricas derivadas
- **✅ Validaciones Finales**: Verificación de completitud antes de generar salidas

### 🚀 **FASES FUTURAS: INTEGRACIÓN AVANZADA**
- **Fase 4**: Integración con Strava API para datos de actividades reales
- **Fase 5**: Integración con IA (Perplexity API) para generación de planes
- **Fase 6**: Sistema web/dashboard para visualización avanzada

---

## 🛠️ **Instalación y Configuración**

### **Prerrequisitos**
- **Python 3.10+** (recomendado 3.11 o superior)
- **pip** (gestor de paquetes Python)
- **git** para clonar el repositorio

### **Instalación**

```bash
# 1. Clonar el repositorio
git clone https://github.com/joseantonio2001/running-fit-tech.git
cd running-fit-tech

# 2. Crear y activar entorno virtual
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/macOS  
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 **Guía de Uso**

### **Comandos Principales**

```bash
# Modo interactivo completo (recomendado)
python -m src.runnerapp.main

# Cargar perfil específico
python -m src.runnerapp.main --load mi_perfil.json

# Modo demo con datos de ejemplo
python -m src.runnerapp.main --demo

# Generar perfil de muestra
python -m src.runnerapp.main --sample
```

### **Experiencia de Usuario Completa**

**🎮 Interfaz Interactiva Profesional:**
```
============================================================
                      RUNNING Fit-Tech                      
============================================================

Aplicación de Entrenamiento para Corredores con IA
Transforme sus datos en planes de entrenamiento personalizados
Sesión iniciada: 18/10/2025 02:50

💾 Todos los cambios están guardados
ℹ️  Progreso del perfil: 3/6 secciones completadas

Opciones disponibles:
  1. 📝 Información Personal ✅
  2. 💓 Métricas Fisiológicas ✅  
  3. 🏃 Contexto de Entrenamiento ✅
  4. 🏆 Datos de Rendimiento ⭕
  5. 🎯 Objetivos de Carrera ⭕
  6. 🤕 Historial de Lesiones ⭕
  7. 📊 Ver Resumen del Perfil
  8. 💾 Guardar Cambios ✅
  9. 🚪 Finalizar y Salir

Seleccione una opción:
```

### **🔧 Características Avanzadas de la CLI**

**Control de Cambios Inteligente:**
- **💾 Guardado Manual**: Usuario controla cuándo guardar los cambios
- **⚠️ Indicadores Visuales**: Emoji warning cuando hay cambios pendientes
- **🛡️ Protección de Datos**: Opción de descartar cambios accidentales
- **🔄 CTRL+C Elegante**: Manejo inteligente de interrupciones

**Validación y Normalización:**
- **✅ Tiempo Real**: Validación inmediata durante entrada de datos
- **🔧 Normalización**: Acepta múltiples formatos (M/F, Sí/No, 01:30:00, etc.)
- **📊 Cálculos Automáticos**: BMI, zonas cardíacas, estimación VO2máx
- **⚠️ Validaciones Cruzadas**: Coherencia entre FC máxima y reposo

**Navegación y Experiencia:**
- **📈 Progreso Visual**: Indicadores ✅/⭕ de completitud por sección
- **↩️ Navegación Flexible**: CTRL+C descarta cambios de sección y vuelve al menú
- **🎨 Interfaz Profesional**: Colores, formato y mensajes consistentes
- **🔍 Resumen Dinámico**: Vista completa del perfil en cualquier momento

---

## 📊 **Estructura del Proyecto**

```
running-fit-tech/
├── src/
│   └── runnerapp/
│       ├── __init__.py
│       ├── main.py              # Punto de entrada principal  
│       ├── models.py            # Modelo de datos central (AthleteProfile)
│       ├── cli.py               # ✅ CLI interactiva completa (FASE 2)
│       ├── cli_helpers.py       # ✅ Utilidades de interfaz y formato
│       ├── persistence.py       # Persistencia JSON robusta
│       ├── calculations.py      # Cálculos, validaciones y normalizaciones
│       └── validators.py        # Validadores específicos para prompt-toolkit
├── examples/                    # Ejemplos y datos de muestra
│   ├── mi_perfil.json          # Perfil de ejemplo (José Antonio)
│   └── athlete_profile.json    # Perfil por defecto
├── requirements.txt             # Dependencias del proyecto
├── README.md                   # Este archivo
└── .gitignore                  # Archivos excluidos de Git
```

### **🔑 Componentes Clave**

| Módulo | Responsabilidad | Estado |
|--------|-----------------|---------|
| **models.py** | Definición de estructuras de datos centrales | ✅ Completo |
| **cli.py** | Interfaz de línea de comandos interactiva | ✅ Completo |
| **persistence.py** | Guardado/carga de perfiles en JSON | ✅ Completo |
| **calculations.py** | Lógica de negocio y validaciones | ✅ Completo |
| **validators.py** | Validadores para entrada de usuario | ✅ Completo |
| **cli_helpers.py** | Utilidades de formato e interfaz | ✅ Completo |

---

## 📋 **Datos Recolectados**

### **Información Personal** (Obligatoria)
- Nombre completo, edad, género
- Altura y peso (opcionales para cálculo de BMI)

### **Métricas Fisiológicas** (Fundamentales)
- **Frecuencia Cardíaca Máxima y en Reposo** (para zonas de entrenamiento)
- VO2 Máximo (opcional, se puede estimar desde marcas)
- Umbral de lactato y Variabilidad FC (opcionales)

### **Contexto de Entrenamiento** (Crítico)
- Volumen semanal actual en kilómetros
- Días de entrenamiento por semana
- Historial y preferencias de entrenamiento de fuerza
- Preferencia de días para sesiones de calidad

### **Datos de Rendimiento** (Clave para IA)
- **Marcas personales**: 5K, 10K, Media Maratón, Maratón
- Estimación automática de VO2máx basada en marcas y datos físicos

### **Objetivos de Carrera** (Orientación del Plan)
- **Objetivo principal**: Carrera, fecha, distancia, tiempo objetivo
- **Carreras intermedias**: Tests y preparación escalonada
- Análisis automático de tiempo disponible para planificación

### **Historial de Lesiones** (Prevención)
- Registro de lesiones pasadas con fechas y recuperación
- Información crítica para adaptar entrenamientos y prevenir recurrencias

---

## 🎮 **Características de la Interfaz CLI**

### **Experiencia de Usuario Avanzada**
- **🎨 Interfaz Colorida**: Estilos profesionales con colores semánticos
- **📊 Progreso en Tiempo Real**: Indicadores visuales de completitud
- **🔍 Autocompletado**: Sugerencias inteligentes en campos relevantes
- **📝 Valores Predeterminados**: Muestra valores actuales para edición
- **⚡ Validación Instantánea**: Feedback inmediato de errores de entrada

### **Control Total de Datos**
- **💾 Guardado Manual**: Usuario decide cuándo guardar cambios
- **⚠️ Advertencias Visuales**: Indicadores claros de cambios pendientes
- **🗑️ Descarte Seguro**: Opción de descartar cambios accidentales
- **🔄 Recuperación Elegante**: CTRL+C maneja interrupciones sin pérdida de control

### **Navegación Inteligente**
- **📈 Secciones Modulares**: Cada sección puede completarse independientemente
- **↩️ CTRL+C Inteligente**: Desde menú muestra opciones, desde sección cancela y vuelve
- **🎯 Estado Visual**: ✅ completado, ⭕ pendiente, ⚠️ cambios sin guardar
- **📱 Flujo Intuitivo**: Diseño inspirado en mejores prácticas de UX

---

## 🧪 **Testing y Validación**

### **Comandos de Verificación**
```bash
# Verificar instalación
python -c "from src.runnerapp.cli import start_interactive_cli; print('✅ Instalación correcta')"

# Test básico de funcionamiento
python -m src.runnerapp.main --demo

# Test de carga de archivos
python -m src.runnerapp.main --load examples/mi_perfil.json
```

### **Casos de Uso Validados**
- ✅ **Perfil desde cero**: Creación completa paso a paso
- ✅ **Carga de perfil existente**: Modificación de datos guardados
- ✅ **Control de cambios**: Guardado/descarte funcional
- ✅ **Interrupciones**: CTRL+C manejado elegantemente
- ✅ **Validación de datos**: Rangos, formatos y coherencia
- ✅ **Persistencia**: Datos guardados correctamente entre sesiones

---

## 📈 **Casos de Uso Principales**

### **1. Creación de Perfil Nuevo**
Experiencia guiada completa para corredores que usan la aplicación por primera vez. Recolección sistemática de todos los datos necesarios con validación en tiempo real.

### **2. Actualización de Perfil Existente**
Modificación selectiva de secciones específicas manteniendo datos previos. Perfecto para actualizaciones regulares de métricas y objetivos.

### **3. Exploración y Testing**
Modo demo y carga de ejemplos para familiarización con la aplicación sin comprometer datos personales.

### **4. Preparación para IA**
Recolección estructurada de datos optimizada para generar prompts efectivos para sistemas de IA en fases posteriores.

---

## ⚙️ **Configuración Técnica**

### **Dependencias Principales**
```txt
prompt-toolkit>=3.0.0    # CLI interactiva avanzada
dataclasses              # Estructuras de datos (built-in)
typing                   # Type hints (built-in) 
json                     # Persistencia (built-in)
datetime                 # Manejo de fechas (built-in)
```

### **Arquitectura de Módulos**
- **models.py**: Single Source of Truth con dataclasses
- **cli.py**: Experiencia interactiva con prompt-toolkit
- **persistence.py**: Serialización robusta con validación
- **calculations.py**: Lógica de negocio y transformaciones
- **validators.py**: Validadores específicos de dominio
- **cli_helpers.py**: Utilidades de presentación e interfaz

---

## 🎪 **Ejemplos de Salida**

### **Perfil Completado**
```json
{
  "athlete_summary": {
    "name": "José Antonio",
    "generated_at": "2025-10-18T02:50:00.000000"
  },
  "personal_info": {
    "age": 24,
    "gender": "Masculino", 
    "height_cm": 184,
    "weight_kg": 72.0
  },
  "physiological_metrics": {
    "max_hr": 194,
    "resting_hr": 41,
    "vo2_max": 58.5,
    "training_zones": {
      "recovery": "41-129 ppm",
      "aerobic": "129-153 ppm", 
      "anaerobic": "153-174 ppm",
      "vo2max": "174-194 ppm"
    }
  },
  "performance_data": {
    "personal_bests": {
      "5k": "00:19:30",
      "10k": "00:42:15",
      "half_marathon": "01:28:45"
    }
  },
  "race_goals": {
    "main_objective": {
      "name": "Media Maratón de Valencia",
      "date": "2024-12-01", 
      "distance_km": 21.097,
      "goal_time": "01:25:00",
      "terrain": "Llano"
    }
  }
}
```

---

## 🏆 **Logros Técnicos de la Fase 2**

### **Problemas Complejos Resueltos**
- **✅ Control de Estado Complejo**: Sistema de tracking de cambios en tiempo real
- **✅ Manejo de Interrupciones**: CTRL+C con comportamientos diferenciados por contexto
- **✅ Validación Avanzada**: Coherencia entre métricas y normalización de formatos múltiples
- **✅ Persistencia Inteligente**: Carga de archivos específicos con fallback elegante
- **✅ UX Profesional**: Indicadores visuales precisos y mensajes contextuales

### **Arquitectura Robusta Implementada**
- **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad específica
- **Extensibilidad**: Fácil añadir nuevas secciones y validadores
- **Mantenibilidad**: Código limpio con documentación completa
- **Testabilidad**: Funciones modulares fáciles de verificar

---

## 🔮 **Próximos Pasos**

### **Fase 3: Generación de Salidas (Próxima)**
1. **PDF Profesional**: ReportLab con diseño visual atractivo
2. **JSON Optimizado**: Prompt estructurado para máxima efectividad de IA  
3. **Cálculos Avanzados**: Zonas detalladas y métricas derivadas
4. **Validación Final**: Verificación de datos antes de output

### **Roadmap a Largo Plazo**
- **Q4 2024**: Fase 3 completada, sistema básico funcional
- **Q1 2025**: Integración Strava (Fase 4) 
- **Q2 2025**: Integración IA para planes automáticos (Fase 5)
- **Q3 2025**: Dashboard web y características avanzadas (Fase 6)

---

## 🤝 **Contribución**

El proyecto está en desarrollo activo. Para contribuir:

1. **Fork** del repositorio
2. **Crear branch** para nuevas características: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -am 'Añadir nueva característica'`
4. **Push** al branch: `git push origin feature/nueva-caracteristica`
5. **Crear Pull Request** con descripción detallada

---

## 📄 **Licencia**

Este proyecto es de uso educativo y de investigación. 

**Desarrollado con ❤️ para la comunidad de corredores y entusiastas del fitness.**

---

## 📞 **Contacto y Soporte**

- **Issues**: [GitHub Issues](https://github.com/joseantonio2001/running-fit-tech/issues)
- **Documentación**: Ver archivos de documentación técnica en `/docs`
- **Ejemplos**: Revisar `/examples` para casos de uso completos

**¡Transforma tu entrenamiento con ciencia y tecnología!** 🏃‍♂️🤖