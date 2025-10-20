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

### 🆕 **FASE 4: POST-IMPLEMENTATION OPTIMIZATIONS & BUG FIXES - COMPLETADA** 
**Refinamientos críticos y nuevas características técnicas implementadas exitosamente**

- **✅ Nuevos Campos Técnicos**: Experiencia deportiva y período de entrenamiento actual
- **✅ Validadores Avanzados**: Sistema compatible con prompt-toolkit async
- **✅ Bug Fixes Críticos**: Solucionados errores de `validate_async` y `personal_bests`
- **✅ Simplificación UX**: Eliminación del campo redundante `competitive_level`
- **✅ Validación Temporal Inteligente**: Reconocimiento de múltiples formatos de tiempo
- **✅ Optimizaciones de Performance**: Mejor manejo de memoria y carga de datos
- **✅ Refinamientos de Interface**: Mejoras en flujo y mensajes de usuario

### 🚀 **FASES FUTURAS: INTEGRACIÓN AVANZADA**
- **Fase 5**: Integración con Strava API para datos de actividades reales
- **Fase 6**: Integración con IA (Perplexity API) para generación de planes
- **Fase 7**: Sistema web/dashboard para visualización avanzada

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
Sesión iniciada: 20/10/2025 17:25

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
  9. 🚪 Finalizar y Salir

Seleccione una opción:
```

### **🔧 Características Avanzadas de la CLI**

**Control de Cambios Inteligente:**
- **💾 Guardado Manual**: Usuario controla cuándo guardar los cambios
- **⚠️ Indicadores Visuales**: Emoji warning cuando hay cambios pendientes
- **🛡️ Protección de Datos**: Opción de descartar cambios accidentales
- **🔄 CTRL+C Elegante**: Manejo inteligente de interrupciones

**🆕 Validación y Normalización Avanzada:**
- **✅ Tiempo Real**: Validación inmediata durante entrada de datos
- **🔧 Normalización**: Acepta múltiples formatos (M/F, Sí/No, 01:30:00, etc.)
- **🧠 Validación Temporal Inteligente**: Reconoce "2 m", "3 weeks", "1 año", "empezando"
- **📊 Cálculos Automáticos**: BMI, zonas cardíacas, estimación VO2máx
- **⚠️ Validaciones Cruzadas**: Coherencia entre FC máxima y reposo
- **🛠️ Validadores Async**: Compatibilidad total con prompt-toolkit moderno

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
│       ├── models.py            # 🆕 Modelo optimizado sin campos redundantes
│       ├── cli.py               # ✅ CLI con nuevos campos técnicos y validación mejorada
│       ├── cli_helpers.py       # ✅ Utilidades de interfaz actualizada
│       ├── persistence.py       # Persistencia JSON robusta
│       ├── calculations.py      # Cálculos, validaciones y normalizaciones
│       ├── validators.py        # 🆕 Validadores compatibles con prompt-toolkit
│       ├── outputgen.py         # ✅ Generación PDF optimizada (FASE 3)
│       ├── pdf_styles.py        # ✅ Estilos minimalistas para PDF
│       ├── json_optimizer.py    # ✅ Optimización JSON para IA actualizada
│       └── 🆕 optional_validators.py  # Validadores async compatibles
├── examples/                    # Ejemplos y datos de muestra
│   ├── mi_perfil.json          # Perfil de ejemplo (José Antonio)
│   └── athlete_profile.json    # Perfil por defecto
├── outputs/                    # Salidas generadas (PDF y JSON)
│   ├── *.pdf                   # Fichas técnicas profesionales
│   └── *_ai.json              # Perfiles optimizados para IA
├── 🆕 profile_template.json    # Plantilla actualizada sin campos redundantes
├── requirements.txt             # Dependencias del proyecto
├── README.md                   # Este archivo
└── .gitignore                  # Archivos excluidos de Git
```

### **🔑 Componentes Clave**

| Módulo | Responsabilidad | Estado |
|--------|-----------------|---------
| **models.py** | 🆕 Modelo optimizado con nuevos campos técnicos | ✅ Actualizado |
| **cli.py** | 🆕 Interfaz con validación avanzada y nuevos campos | ✅ Actualizado |
| **persistence.py** | Guardado/carga de perfiles en JSON | ✅ Completo |
| **calculations.py** | Lógica de negocio y validaciones | ✅ Completo |
| **validators.py** | 🆕 Validadores compatibles async | ✅ Actualizado |
| **cli_helpers.py** | Utilidades de formato e interfaz | ✅ Completo |
| **outputgen.py** | 🆕 Generación PDF optimizada | ✅ Actualizado |
| **pdf_styles.py** | Estilos minimalistas profesionales | ✅ Completo |
| **json_optimizer.py** | 🆕 Optimización actualizada para IA | ✅ Actualizado |
| **🆕 optional_validators.py** | Validadores async para campos opcionales | ✅ Nuevo |

---

## 📋 **Datos Recolectados - ACTUALIZADOS**

### **Información Personal** (Obligatoria)
- Nombre completo, edad, género
- Altura y peso (opcionales para cálculo de BMI)

### **Métricas Fisiológicas** (Fundamentales)
- **Frecuencia Cardíaca Máxima y en Reposo** (para zonas de entrenamiento)
- VO2 Máximo (opcional, se puede estimar desde marcas)
- **🆕 Umbral de lactato** y **🆕 Variabilidad FC** (opcionales, validación mejorada)

### **🆕 Contexto de Entrenamiento MEJORADO** (Crítico)
- Volumen semanal actual en kilómetros
- Días de entrenamiento por semana
- **🆕 Experiencia deportiva total** (años practicando running)
- **🆕 Período de entrenamiento actual** (con validación temporal inteligente)
- Historial y preferencias de entrenamiento de fuerza
- Disponibilidad de días y restricciones horarias

### **Datos de Rendimiento** (Clave para IA)
- **Marcas personales**: 5K, 10K, Media Maratón, Maratón (con fix crítico)
- Estimación automática de VO2máx basada en marcas y datos físicos

### **Objetivos de Carrera** (Orientación del Plan)
- **Objetivo principal**: Carrera, fecha, distancia, tiempo objetivo
- **Carreras intermedias**: Tests y preparación escalonada
- Análisis automático de tiempo disponible para planificación

### **Historial de Lesiones** (Prevención)
- Registro de lesiones pasadas con fechas y recuperación
- Información crítica para adaptar entrenamientos y prevenir recurrencias

---

## 🆕 **CAMBIOS DESDE FASE 3 POST-IMPLEMENTATION**

### **✨ Nuevas Características Implementadas**

#### **🔧 Campos Técnicos Añadidos:**
- **`running_experience_years`**: Experiencia total en atletismo (0-50 años)
- **`current_training_period`**: Período actual con validación temporal inteligente
- **`lactate_threshold_bpm`**: Umbral de lactato (opcional, 100-220 bpm)
- **`hrv_ms`**: Variabilidad de frecuencia cardíaca (opcional, 10-200 ms)

#### **🧠 Validación Temporal Inteligente:**
```bash
# Ejemplos de entrada soportados:
"2 m" → "2 meses"
"3 weeks" → "3 semanas"  
"1 año" → "1 año"
"empezando" → "Empezando ahora"
"5 d" → "5 días"
```

#### **🐛 Bugs Críticos Solucionados:**
- **✅ Fix validate_async**: Validadores opcionales ahora compatibles con prompt-toolkit
- **✅ Fix personal_bests**: Solucionado problema de mutabilidad en diccionarios
- **✅ Fix lactate_threshold_bpm**: Corrección de typo en nombre de campo
- **✅ Eliminación competitive_level**: Campo redundante removido de toda la aplicación

#### **⚡ Optimizaciones de Performance:**
- **Validadores Async Compatibles**: `OptionalFloatValidator`, `OptionalIntegerValidator`
- **Mejor Gestión de Memoria**: Copias temporales para evitar mutación accidental
- **Validación Mejorada**: Reconocimiento inteligente de patrones temporales
- **UX Simplificado**: Una pregunta menos en el cuestionario (competitive_level)

---

## 🆕 **Validación Temporal Inteligente**

### **Formatos Soportados en Período de Entrenamiento:**

| Entrada Usuario | Resultado Normalizado |
|-----------------|---------------------|
| `"2 meses"` | `"2 meses"` |
| `"2 m"` | `"2 meses"` |
| `"3 weeks"` | `"3 semanas"` |
| `"1 year"` | `"1 año"` |
| `"5 days"` | `"5 días"` |
| `"empezando"` | `"Empezando ahora"` |
| `"starting"` | `"Empezando ahora"` |
| `"3"` | `"3 meses"` (por defecto) |

### **Características del Sistema:**
- **🌐 Multiidioma**: Soporte español e inglés completo
- **📝 Abreviaciones**: Reconoce `m`, `s`, `a`, `d` y equivalentes en inglés
- **🔤 Case-insensitive**: `MESES`, `MeSeS`, `meses` funcionan igual
- **🔢 Singular/Plural**: Ajuste automático según el número
- **⚠️ Validación**: Rechaza entradas no válidas con mensaje claro

---

## 🎯 **Estructura del Modelo de Datos ACTUALIZADA**

### **🆕 Nuevos Campos AthleteProfile:**

```python
@dataclass
class AthleteProfile:
    # === NUEVOS CAMPOS TÉCNICOS ===
    running_experience_years: Optional[float] = None    # 🆕 Experiencia total
    current_training_period: str = ""                   # 🆕 Período actual (normalizado)
    lactate_threshold_bpm: Optional[int] = None         # 🆕 Umbral lactato
    hrv_ms: Optional[int] = None                        # 🆕 Variabilidad FC
    
    # === CAMPO ELIMINADO ===
    # competitive_level: str = ""  # ❌ ELIMINADO - se deduce de marcas
```

### **🛠️ Validadores Añadidos:**

```python
# 🆕 NUEVOS VALIDADORES ASYNC-COMPATIBLES
OptionalFloatValidator(min_val=0, max_val=50)      # Experiencia deportiva
TrainingPeriodValidator()                          # Período temporal inteligente  
OptionalIntegerValidator(100, 220)                 # Umbral lactato
OptionalIntegerValidator(10, 200)                  # Variabilidad FC
```

---

## 📊 **Bug Fixes y Optimizaciones Implementadas**

### **🐛 Bugs Críticos Solucionados:**

#### **1. Error `validate_async` en Validadores Opcionales**
**Problema:** `'OptionalFloatValidator' object has no attribute 'validate_async'`

**✅ Solución:** Creación de validadores compatibles con herencia correcta:
```python
class OptionalFloatValidator(Validator):  # ✅ Herencia correcta
    async def validate_async(self, document: Document) -> None:  # ✅ Método requerido
        self.validate(document)
```

#### **2. Bug en `personal_bests` (Mutabilidad de Diccionarios)**
**Problema:** Modificaciones no se guardaban correctamente

**✅ Solución:** Pattern copy-modify-assign:
```python
# ✅ CORRECCIÓN: Copia temporal para evitar mutación
temp_personal_bests = profile.personal_bests.copy()
# ... modificaciones en temp_personal_bests ...
profile.personal_bests = temp_personal_bests  # ✅ Asignación final
```

#### **3. Typo en `lactate_threshold_bpm`**
**Problema:** Campo referenciado como `lactate_threshold_bmp` (sin 'p')

**✅ Solución:** Corrección consistente en todos los archivos

#### **4. Eliminación Campo Redundante**
**Problema:** `competitive_level` era redundante (deducible de marcas)

**✅ Solución:** Eliminación sistemática de toda la aplicación:
- ❌ Removido del modelo de datos
- ❌ Pregunta eliminada del CLI  
- ❌ Eliminado de PDF y JSON
- ❌ Removido de template y helpers

---

## 🔧 **Características Técnicas Avanzadas**

### **🆕 Validación Temporal Inteligente**

**Clase `TrainingPeriodValidator`:**
- **Reconocimiento Multiidioma**: Español + Inglés
- **Flexibilidad de Entrada**: Abreviaciones, plurales, mayúsculas  
- **Normalización Automática**: Convierte a formato estándar español
- **Validación Robusta**: Rechaza entradas inválidas con mensajes claros

**Ejemplos de Reconocimiento:**
```python
"1 manzana"  → ❌ "Formato no reconocido. Ejemplos: '2 meses', '3 weeks'"
"2 m"        → ✅ "Período normalizado a: '2 meses'"
"3 semanas"  → ✅ "3 semanas" (ya correcto)
"1 year"     → ✅ "Período normalizado a: '1 año'"
```

### **🛠️ Validadores Async Compatibles**

**Nuevos Validadores Añadidos:**
```python
# runner-app/src/runnerapp/optional_validators.py
class OptionalFloatValidator(Validator):     # ✅ Herencia correcta
class OptionalIntegerValidator(Validator):   # ✅ Herencia correcta  
class OptionalStringValidator(Validator):    # ✅ Nueva funcionalidad
class TrainingPeriodValidator(Validator):    # ✅ Validación temporal inteligente
```

**Características:**
- **✅ Compatibilidad Async**: Método `validate_async` implementado
- **✅ Campos Opcionales**: Permite valores vacíos sin errores
- **✅ Validación de Rangos**: Límites mínimos y máximos configurables
- **✅ Mensajes Claros**: Feedback específico para cada tipo de error

### **📈 Mejoras en Experiencia de Usuario**

**Nuevos Campos con Validación Inteligente:**
1. **Experiencia Deportiva** (0-50 años, acepta decimales)
2. **Período Actual** (validación temporal multiformat)
3. **Umbral de Lactato** (100-220 bpm, opcional)
4. **Variabilidad FC** (10-200 ms, opcional)

**Eliminaciones para Simplificar UX:**
- ❌ **Competitive Level**: Eliminado - era redundante con las marcas personales

---

## 🆕 **Características de la Fase 4: Outputs Profesionales MEJORADOS**

### **🎨 PDF Ultra-Minimalista ACTUALIZADO**

**Nuevos Campos Mostrados:**
- **✅ Experiencia Deportiva**: Años totales en running
- **✅ Período Actual**: Tiempo entrenando actualmente (normalizado)
- **✅ Umbral de Lactato**: Si está disponible (opcional)
- **✅ Variabilidad FC**: Si está disponible (opcional)
- **❌ Nivel Competitivo**: Eliminado del PDF (redundante)

**Diseño Mantenido:**
- **Paleta Dark Elegante**: Fondo negro profundo (#0A0A0A) 
- **Espaciado Perfecto**: 14pt entre secciones para respiración visual
- **Información Completa**: "No proporcionado" para campos vacíos
- **Profesionalismo Total**: Encabezado, numeración y branding

### **🤖 JSON para IA OPTIMIZADO**

**Nuevas Secciones Añadidas:**
```json
{
  "experience_and_background": {
    "running_experience_years": 8.1,
    "current_training_period": "1 mes",
    "experience_notes": "Atleta experimentado con base sólida"
  },
  "enhanced_physiological_data": {
    "lactate_threshold_bpm": 175,
    "hrv_ms": 45,
    "advanced_metrics_available": true
  }
}
```

**Optimizaciones:**
- **❌ Competitive Level Removido**: Ya no incluido en JSON
- **✅ Nuevos Insights**: Análisis automático de experiencia
- **✅ Datos Técnicos**: Métricas avanzadas cuando están disponibles
- **✅ Contexto Mejorado**: Información más rica para la IA

---

## 🧪 **Testing y Validación ACTUALIZADOS**

### **Comandos de Verificación**
```bash
# Verificar instalación completa
python -c "from src.runnerapp.cli import start_interactive_cli; print('✅ Instalación correcta')"

# 🆕 Test validadores temporales
python -c "from src.runnerapp.optional_validators import TrainingPeriodValidator; print('✅ Validadores funcionando')"

# Test generación de salidas
python -m src.runnerapp.main --generate-outputs

# Test básico de funcionamiento
python -m src.runnerapp.main --demo

# Test de carga de archivos
python -m src.runnerapp.main --load examples/mi_perfil.json
```

### **🆕 Casos de Uso Validados Post-Fase 3**
- ✅ **Nuevos Campos Técnicos**: Entrada y validación correcta
- ✅ **Validación Temporal**: Reconocimiento multiformat funcional
- ✅ **Validadores Async**: Sin errores de `validate_async`
- ✅ **Personal Bests Fix**: Guardado correcto de marcas
- ✅ **Eliminación Competitive Level**: Sin errores en PDF/JSON
- ✅ **Compatibilidad Prompt-Toolkit**: Funcionamiento perfecto
- ✅ **UX Optimizada**: Flujo más rápido y directo

---

## 🔄 **Changelog Detallado Post-Fase 3**

### **🆕 v4.0.0 - Post-Implementation Optimizations (20/10/2025)**

#### **✨ Nuevas Características:**
- **Campos Técnicos Avanzados**: `running_experience_years`, `current_training_period`
- **Validación Temporal Inteligente**: Sistema multiformat para períodos de tiempo
- **Métricas Fisiológicas Ampliadas**: `lactate_threshold_bmp`, `hrv_ms`
- **Validadores Async Compatibles**: Sistema completamente compatible con prompt-toolkit

#### **🐛 Bug Fixes Críticos:**
- **Fixed**: Error `validate_async` en validadores opcionales
- **Fixed**: Problema de mutabilidad en `personal_bests` 
- **Fixed**: Typo en `lactate_threshold_bmp` → `lactate_threshold_bpm`
- **Fixed**: Referencias inconsistentes en outputgen y json_optimizer

#### **🗑️ Eliminaciones para UX:**
- **Removed**: Campo `competitive_level` (redundante con marcas personales)
- **Removed**: Pregunta correspondiente del CLI
- **Removed**: Referencias en PDF, JSON y template

#### **⚡ Optimizaciones:**
- **Improved**: Compatibilidad total con prompt-toolkit moderno
- **Improved**: Manejo de memoria en modificación de diccionarios
- **Improved**: Experiencia de usuario más rápida (una pregunta menos)
- **Improved**: Validación más robusta y mensajes más claros

---

## 📈 **Casos de Uso Principales ACTUALIZADOS**

### **1. Creación de Perfil Nuevo MEJORADA**
Experiencia guiada con **nuevos campos técnicos** y **validación temporal inteligente**. Flujo más rápido sin pregunta de nivel competitivo redundante.

### **2. Actualización de Perfil Existente OPTIMIZADA**
Modificación con **validadores async compatibles** que eliminan errores técnicos y permiten entrada más flexible en formatos temporales.

### **3. Generación de Outputs Profesionales REFINADA**
PDF y JSON actualizados con **nuevos campos técnicos** pero sin información redundante, manteniendo profesionalismo y optimización para IA.

### **4. Exploración y Testing MEJORADO**
Sin errores técnicos de validación, experiencia fluida en todos los flujos de usuario.

---

## ⚙️ **Configuración Técnica ACTUALIZADA**

### **🆕 Dependencias Mantenidas**
```txt
prompt-toolkit>=3.0.0    # CLI interactiva (validación async compatible)
reportlab>=4.0.0         # Generación de PDF profesional
dataclasses              # Estructuras de datos (built-in)
typing                   # Type hints (built-in) 
json                     # Persistencia (built-in)
datetime                 # Manejo de fechas (built-in)
pathlib                  # Manejo de rutas (built-in)
re                       # 🆕 Expresiones regulares para validación temporal
```

### **🔧 Arquitectura de Módulos ACTUALIZADA**
- **models.py**: 🆕 Nuevos campos técnicos, campo redundante eliminado
- **cli.py**: 🆕 Validación avanzada, nuevos campos, UX optimizada
- **persistence.py**: ✅ Sin cambios (funciona perfectamente)
- **calculations.py**: ✅ Funciones auxiliares mantenidas
- **validators.py**: 🆕 Compatibilidad async garantizada
- **cli_helpers.py**: 🆕 Display actualizado sin competitive_level
- **outputgen.py**: 🆕 PDF con nuevos campos, sin redundancias
- **json_optimizer.py**: 🆕 JSON optimizado con nuevos datos técnicos
- **🆕 optional_validators.py**: Nuevo módulo de validadores async

---

## 🎪 **Ejemplos de Salida ACTUALIZADOS**

### **🆕 CLI con Nuevos Campos (Extracto)**
```
📋 Contexto de Entrenamiento

Volumen semanal promedio actual [actual: 56.0] (kilómetros por semana - ej: 50.0): 56.0
Días de entrenamiento por semana [actual: 4] (contexto actual - ej: 4 o 4-5 para rango): 4
🆕 Experiencia deportiva en running [actual: 8.0] (años totales practicando running - ej: 5 o 2.5): 8.1
🆕 Período de entrenamiento actual [actual: ] (ej: '3 semanas', '2 meses', '2 m', 'empezando'): 2 months
✅ Período normalizado a: '2 meses'
```

### **🆕 PDF Mejorado (Extracto)**
```
                   CONTEXTO DE ENTRENAMIENTO

VOLUMEN SEMANAL · 56.0 km/semana
DÍAS ENTRENAMIENTO · 4 días/semana
🆕 EXPERIENCIA DEPORTIVA · 8.1 años
🆕 PERÍODO ACTUAL · 2 meses
HISTORIAL FUERZA · NO
```

### **🆕 JSON para IA Optimizado (Extracto)**
```json
{
  "experience_and_background": {
    "running_experience_years": 8.1,
    "current_training_period": "2 meses", 
    "experience_notes": "Atleta experimentado con base sólida"
  },
  "enhanced_physiological_data": {
    "lactate_threshold_bpm": 175,
    "hrv_ms": 45,
    "advanced_metrics_available": true,
    "physiological_insights": "Perfil fisiológico completo con métricas avanzadas"
  }
}
```

---

## 🤝 **Contribución ACTUALIZADA**

El proyecto está en desarrollo activo. Para contribuir:

1. **Fork** del repositorio
2. **Crear branch** para nuevas características: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -am 'Añadir nueva característica'`
4. **Push** al branch: `git push origin feature/nueva-caracteristica`
5. **Crear Pull Request** con descripción detallada

### **🆕 Áreas de Contribución Post-Fase 4**
- **Validadores Avanzados**: Nuevos tipos de validación temporal y fisiológica
- **Campos Técnicos**: Métricas especializadas para diferentes deportes
- **Optimizaciones IA**: Mejoras en estructura JSON para modelos específicos
- **UX Refinements**: Mejoras continuas en flujo de usuario
- **Performance**: Optimizaciones de memoria y velocidad

---

## 📄 **Licencia**

Este proyecto es de uso educativo y de investigación. 

**Desarrollado con ❤️ para la comunidad de corredores y entusiastas del fitness.**

---

## 📞 **Contacto y Soporte**

- **Issues**: [GitHub Issues](https://github.com/joseantonio2001/running-fit-tech/issues)
- **Documentación**: Ver archivos de documentación técnica en `/docs`
- **Ejemplos**: Revisar `/examples` para casos de uso completos
- **Outputs**: Revisar `/outputs` para ejemplos de PDF y JSON generados
- **🆕 Bug Reports**: Para errores relacionados con nuevos validadores o campos

**¡Transforma tu entrenamiento con ciencia, tecnología y outputs profesionales optimizados!** 🏃‍♂️🤖📄✨