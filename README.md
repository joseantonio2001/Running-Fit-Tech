# RUNNING Fit-Tech 🏃‍♂️

**Aplicación CLI de Entrenamiento para Corredores con Inteligencia Artificial**

Transforme sus datos personales en planes de entrenamiento científicamente personalizados mediante la recolección inteligente de datos, análisis con IA y generación de informes profesionales.

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

### ✅ **FASE 3: GENERACIÓN DE SALIDAS - COMPLETADA** 🆕
**Sistema de outputs profesionales con PDF ultra-minimalista y JSON optimizado para IA**

- **✅ PDF Ultra-Minimalista**: Diseño profesional con ReportLab y estética elegante
- **✅ Espaciado Perfecto**: Diseño balanceado con máxima legibilidad y respiración visual
- **✅ Encabezado Inteligente**: Branding izquierda, copyright derecha, numeración centrada
- **✅ Todos los Campos Visibles**: Información completa siempre mostrada, no omitida
- **✅ Salto de Página Inteligente**: Zonas de entrenamiento en página separada
- **✅ JSON Optimizado para IA**: Estructura auto-explicativa con contexto completo
- **✅ Validaciones Finales**: Verificación de completitud antes de generar salidas
- **✅ Generación Automática**: Comando `--generate-outputs` para salidas instantáneas
- **✅ Cálculos Derivados**: Zonas Karvonen, BMI separado, ritmos automáticos
- **✅ Paleta Minimalista**: Esquema de colores dark elegante y profesional

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
venv\Scripts\activate

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

# 🆕 GENERAR SALIDAS PDF Y JSON
python -m src.runnerapp.main --generate-outputs

# Modo demo con datos de ejemplo
python -m src.runnerapp.main --demo

# Generar perfil de muestra
python -m src.runnerapp.main --sample
```

### **🆕 Generación de Salidas Profesionales**

**Comando de Generación:**
```bash
python -m src.runnerapp.main --generate-outputs
```

**Salida del Sistema:**
```
============================================================      
                      RUNNING Fit-Tech                            
============================================================      

ℹ️  AI-Powered Training Assistant for Runners
ℹ️  Modo de generación de salidas activado
ℹ️  🎯 Generating outputs for: Tomás Solórza

🏆 PDF PROFESIONAL generado: outputs/ficha_tecnica_profesional_tomas_solorzano.pdf
✅ JSON OPTIMIZADO para IA generado: outputs/athlete_profile_tomas_solorzano_ai.json

✨ Características implementadas:
   📏 Espaciado perfecto entre bloques (14pt)
   💎 Diseño ultra-minimalista y elegante
   📄 Salto de página después de Zonas de Entrenamiento
   📊 Todos los campos siempre visibles
   🔝 Encabezado con branding y copyright
   📍 Numeración centrada en la parte inferior
   🎨 Paleta de colores dark profesional
   ✅ JSON estructurado para máxima efectividad de IA
```

### **Experiencia de Usuario Completa**

**🎮 Interfaz Interactiva Profesional:**
```
============================================================
                      RUNNING Fit-Tech                      
============================================================

Aplicación de Entrenamiento para Corredores con IA
Transforme sus datos en planes de entrenamiento personalizados
Sesión iniciada: 18/10/2025 17:25

💾 Todos los cambios están guardados
ℹ️  Progreso del perfil: 6/6 secciones completadas

Opciones disponibles:
  1. 📝 Información Personal ✅
  2. 💓 Métricas Fisiológicas ✅  
  3. 🏃 Contexto de Entrenamiento ✅
  4. 🏆 Datos de Rendimiento ✅
  5. 🎯 Objetivos de Carrera ✅
  6. 🤕 Historial de Lesiones ✅
  7. 📊 Ver Resumen del Perfil
  8. 💾 Guardar Cambios ✅
  9. 🆕 📄 Generar Salidas (PDF + JSON)
  10. 🚪 Finalizar y Salir

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
│       ├── validators.py        # Validadores específicos para prompt-toolkit
│       ├── 🆕 outputgen.py      # ✅ Generación PDF y JSON (FASE 3)
│       ├── 🆕 pdf_styles.py     # ✅ Estilos minimalistas para PDF
│       └── 🆕 json_optimizer.py # ✅ Optimización JSON para IA
├── examples/                    # Ejemplos y datos de muestra
│   ├── mi_perfil.json          # Perfil de ejemplo (José Antonio)
│   └── athlete_profile.json    # Perfil por defecto
├── 🆕 outputs/                 # Salidas generadas (PDF y JSON)
│   ├── *.pdf                   # Fichas técnicas profesionales
│   └── *_ai.json              # Perfiles optimizados para IA
├── requirements.txt             # Dependencias del proyecto
├── README.md                   # Este archivo
└── .gitignore                  # Archivos excluidos de Git
```

### **🔑 Componentes Clave**

| Módulo | Responsabilidad | Estado |
|--------|-----------------|---------
| **models.py** | Definición de estructuras de datos centrales | ✅ Completo |
| **cli.py** | Interfaz de línea de comandos interactiva | ✅ Completo |
| **persistence.py** | Guardado/carga de perfiles en JSON | ✅ Completo |
| **calculations.py** | Lógica de negocio y validaciones | ✅ Completo |
| **validators.py** | Validadores para entrada de usuario | ✅ Completo |
| **cli_helpers.py** | Utilidades de formato e interfaz | ✅ Completo |
| **🆕 outputgen.py** | Generación de PDF y JSON optimizado | ✅ Completo |
| **🆕 pdf_styles.py** | Estilos minimalistas profesionales | ✅ Completo |
| **🆕 json_optimizer.py** | Optimización de datos para IA | ✅ Completo |

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

## 🆕 **Características de la Fase 3: Outputs Profesionales**

### **🎨 PDF Ultra-Minimalista**

**Diseño Profesional:**
- **Paleta Dark Elegante**: Fondo negro profundo (#0A0A0A) con textos claros
- **Tipografía Helvetica**: Fuente profesional con diferentes pesos y tamaños
- **Espaciado Perfecto**: 14pt entre títulos y contenido, balance visual óptimo
- **Encabezado Inteligente**: RUNNING FIT-TECH (izq.) + © 2025 PREMIUM (der.)
- **Numeración Centrada**: Página numerada en parte inferior central

**Estructura de Contenido:**
- **Página 1**: Info personal, métricas fisiológicas, zonas de entrenamiento
- **Página 2+**: Contexto entrenamiento, rendimiento, objetivos, lesiones
- **Todas las Secciones Siempre Visibles**: Nunca se omite información
- **"No proporcionado"** para campos vacíos (transparencia total)

**Elementos Técnicos:**
- **BMI como Campo Separado**: No concatenado, cálculo independiente
- **Zonas Karvonen Detalladas**: Tabla profesional con colores sutiles por zona
- **Ritmos Automáticos**: Calculados desde marcas personales
- **Salto de Página Inteligente**: Zonas en página separada para mejor organización

### **🤖 JSON Optimizado para IA**

**Estructura Auto-Explicativa:**
```json
{
  "ai_prompt_context": {
    "purpose": "Generar plan entrenamiento personalizado running",
    "athlete_profile_summary": "Análisis completo del perfil deportivo",
    "data_completeness": "95%",
    "key_insights": ["VO2máx estimado alto", "Experiencia intermedia"]
  },
  "athlete_summary": {
    "name": "Tomás Solórza", 
    "profile_completeness": 0.95,
    "training_level": "intermediate",
    "generated_at": "2025-10-18T17:25:00"
  },
  "optimization_insights": {
    "strengths": ["Alta capacidad aeróbica", "Experiencia consistente"],
    "areas_to_improve": ["Velocidad en distancias cortas"],
    "training_focus": ["Desarrollo de potencia aeróbica máxima"]
  }
}
```

**Características del JSON:**
- **Contexto Completo**: Información explicativa para la IA
- **Métricas Derivadas**: Cálculos automáticos y insights
- **Estructura Jerárquica**: Datos organizados lógicamente
- **Auto-Explicativo**: Cada sección incluye su propósito
- **Validación Integrada**: Verificación de completitud y coherencia

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
# Verificar instalación completa
python -c "from src.runnerapp.cli import start_interactive_cli; print('✅ Instalación correcta')"

# Test generación de salidas
python -m src.runnerapp.main --generate-outputs

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
- ✅ **🆕 Generación PDF**: Salida profesional minimalista
- ✅ **🆕 Optimización IA**: JSON estructurado y auto-explicativo

---

## 📈 **Casos de Uso Principales**

### **1. Creación de Perfil Nuevo**
Experiencia guiada completa para corredores que usan la aplicación por primera vez. Recolección sistemática de todos los datos necesarios con validación en tiempo real.

### **2. Actualización de Perfil Existente**
Modificación selectiva de secciones específicas manteniendo datos previos. Perfecto para actualizaciones regulares de métricas y objetivos.

### **3. 🆕 Generación de Outputs Profesionales**
Comando directo para generar ficha técnica en PDF ultra-minimalista y archivo JSON optimizado para sistemas de IA, listos para uso inmediato.

### **4. Exploración y Testing**
Modo demo y carga de ejemplos para familiarización con la aplicación sin comprometer datos personales.

### **5. Preparación para IA**
Recolección estructurada de datos optimizada para generar prompts efectivos para sistemas de IA en fases posteriores.

---

## ⚙️ **Configuración Técnica**

### **Dependencias Principales**
```txt
prompt-toolkit>=3.0.0    # CLI interactiva avanzada
reportlab>=4.0.0         # 🆕 Generación de PDF profesional
dataclasses              # Estructuras de datos (built-in)
typing                   # Type hints (built-in) 
json                     # Persistencia (built-in)
datetime                 # Manejo de fechas (built-in)
pathlib                  # 🆕 Manejo de rutas (built-in)
```

### **Arquitectura de Módulos**
- **models.py**: Single Source of Truth con dataclasses
- **cli.py**: Experiencia interactiva con prompt-toolkit
- **persistence.py**: Serialización robusta con validación
- **calculations.py**: Lógica de negocio y transformaciones
- **validators.py**: Validadores específicos de dominio
- **cli_helpers.py**: Utilidades de presentación e interfaz
- **🆕 outputgen.py**: Generación de salidas PDF y JSON
- **🆕 pdf_styles.py**: Sistema de estilos minimalistas
- **🆕 json_optimizer.py**: Optimización inteligente para IA

---

## 🎪 **Ejemplos de Salida**

### **🆕 Ficha Técnica PDF (Extracto)**
```
RUNNING FIT-TECH                               © 2025 PREMIUM
────────────────────────────────────────────────────────────────────────

                    FICHA TÉCNICA DEPORTIVA
                T O M Á S   S O L Ó R Z A N O
                      18 · OCTUBRE · 2025

                    INFORMACIÓN PERSONAL

EDAD · 30 años
GÉNERO · Masculino
ALTURA · 175 cm
PESO · 70 kg
BMI · 22.9

                   MÉTRICAS FISIOLÓGICAS

Parámetros fisiológicos que definen el perfil de resistencia cardiovascular
y el potencial de rendimiento aeróbico del atleta.

FC MÁXIMA · 190 bpm
FC REPOSO · 50 bpm
VO2 MÁXIMO · 55 ml/kg/min
UMBRAL LACTATO · 175 bpm
VFC (HRV) · 45 ms

                                                                          1
```

### **🆕 JSON Optimizado para IA (Extracto)**
```json
{
  "ai_prompt_context": {
    "purpose": "Generar plan de entrenamiento personalizado para running",
    "athlete_summary": "Corredor intermedio-avanzado con experiencia en medias maratones",
    "data_completeness": 0.95,
    "key_training_insights": [
      "VO2máx alto indica potencial para distancias medias",
      "FC reposo baja sugiere buena condición aeróbica base",
      "Objetivo tiempo agresivo requiere trabajo específico de ritmo"
    ],
    "training_focus_areas": [
      "Desarrollo de potencia aeróbica máxima (VO2máx)",
      "Trabajo de ritmo específico de carrera objetivo",
      "Mantener base aeróbica sólida existente"
    ]
  },
  "athlete_profile": {
    "personal_info": {
      "age": 30,
      "gender": "Masculino",
      "height_cm": 175,
      "weight_kg": 70.0,
      "bmi": 22.9,
      "training_experience_level": "intermediate_advanced"
    },
    "physiological_metrics": {
      "max_hr": 190,
      "resting_hr": 50,
      "hr_reserve": 140,
      "vo2_max": 55.0,
      "lactate_threshold_bpm": 175,
      "hrv_ms": 45,
      "estimated_fitness_level": "well_trained"
    },
    "training_zones_karvonen": {
      "zone1_recovery": {
        "name": "Recuperación Activa",
        "hr_range": "50-106 bpm",
        "intensity_percentage": "50-60%",
        "purpose": "Regeneración y base aeróbica"
      },
      "zone2_aerobic": {
        "name": "Aeróbico Base", 
        "hr_range": "106-134 bpm",
        "intensity_percentage": "60-70%",
        "purpose": "Resistencia fundamental"
      }
    }
  }
}
```

---

## 🏆 **Logros Técnicos de la Fase 3**

### **Problemas Complejos Resueltos**
- **✅ Diseño PDF Minimalista**: Sistema de estilos coherente y profesional
- **✅ Espaciado Matemático**: Cálculo preciso de distribución vertical de contenido
- **✅ Optimización para IA**: JSON auto-explicativo con contexto completo
- **✅ Generación Automática**: Pipeline completo desde datos a outputs finales
- **✅ Validación Previa**: Verificación de completitud antes de generar salidas
- **✅ Cálculos Derivados**: Métricas automáticas como ritmos y zonas avanzadas

### **Arquitectura de Salidas Implementada**
- **Separación de Responsabilidades**: Generación PDF, optimización JSON y estilos independientes
- **Extensibilidad**: Fácil añadir nuevos formatos de salida y estilos
- **Robustez**: Manejo de errores y validaciones en cada etapa
- **Profesionalismo**: Calidad de producción en diseño y funcionalidad

---

## 🔮 **Próximos Pasos**

### **Fase 4: Integración Strava API (Próxima)**
1. **Conexión Strava**: Autenticación OAuth2 y acceso a actividades
2. **Análisis de Actividades**: Procesamiento de datos reales de entrenamientos  
3. **Métricas Automáticas**: Cálculo de zonas y umbrales desde datos reales
4. **Sincronización**: Actualización automática del perfil con datos de Strava

### **Roadmap a Largo Plazo**
- **Q4 2024**: Fase 4 completada, integración Strava funcional
- **Q1 2025**: Integración IA para planes automáticos (Fase 5) 
- **Q2 2025**: Dashboard web y características avanzadas (Fase 6)
- **Q3 2025**: Análisis avanzado y predicciones de rendimiento

---

## 🆕 **Características Destacadas de la Fase 3**

### **🎨 Sistema de Diseño PDF**
- **Paleta de Colores Balanceada**: 10 tonos coordinados para máxima legibilidad
- **Tipografía Jerárquica**: Helvetica con 6 estilos diferentes y propósitos específicos
- **Espaciado Matemático**: Sistema de 14pt entre bloques para respiración visual perfecta
- **Elementos Visuales Sutiles**: Líneas separadoras y fondos que no compiten con el contenido

### **🤖 Optimización Inteligente para IA**
- **Contexto Auto-Generado**: Información explicativa automática para la IA
- **Insights Derivados**: Análisis automático de fortalezas y áreas de mejora
- **Estructura Jerárquica**: Datos organizados por relevancia para entrenamiento
- **Metadatos Completos**: Información sobre completitud y calidad de datos

### **⚙️ Pipeline de Generación**
- **Validación Previa**: Verificación de datos antes de generar outputs
- **Generación Paralela**: PDF y JSON generados simultáneamente
- **Nombrado Automático**: Archivos nombrados automáticamente por atleta y fecha
- **Carpeta de Salida**: Sistema organizado en directorio `outputs/`

---

## 🤝 **Contribución**

El proyecto está en desarrollo activo. Para contribuir:

1. **Fork** del repositorio
2. **Crear branch** para nuevas características: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -am 'Añadir nueva característica'`
4. **Push** al branch: `git push origin feature/nueva-caracteristica`
5. **Crear Pull Request** con descripción detallada

### **🆕 Áreas de Contribución Fase 3**
- **Nuevos Estilos PDF**: Temas claros, coloridos o específicos por deporte
- **Formatos de Salida**: Integración con Excel, Word o formatos web
- **Optimizaciones IA**: Mejoras en la estructura JSON para diferentes modelos de IA
- **Métricas Avanzadas**: Nuevos cálculos derivados y análisis predictivos

---

## 📄 **Licencia**

Este proyecto es de uso educativo y de investigación. 

**Desarrollado con ❤️ para la comunidad de corredores y entusiastas del fitness.**

---

## 📞 **Contacto y Soporte**

- **Issues**: [GitHub Issues](https://github.com/joseantonio2001/running-fit-tech/issues)
- **Documentación**: Ver archivos de documentación técnica en `/docs`
- **Ejemplos**: Revisar `/examples` para casos de uso completos
- **🆕 Outputs**: Revisar `/outputs` para ejemplos de PDF y JSON generados

**¡Transforma tu entrenamiento con ciencia, tecnología y outputs profesionales!** 🏃‍♂️🤖📄