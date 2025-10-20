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

### 🆕 **OPTIMIZACIONES POST-FASE 3: NUEVAS FUNCIONALIDADES - COMPLETADAS** 
**Refinamientos críticos, nuevas características técnicas y solución de bugs implementados exitosamente**

- **✅ Campo "Estado Actual" en Lesiones**: Seguimiento detallado del estado actual de lesiones previas
- **✅ Reordenamiento Contexto Entrenamiento**: "Período actual" como primer campo del bloque
- **✅ Bug Fixes Críticos**: 
  - ✅ Corrección formato CLI en `format_prompt_with_hint()`
  - ✅ Fix persistencia de datos en `AthleteProfile.to_dict()`
  - ✅ Corrección indicador de guardado con `deepcopy()`
- **✅ Nuevos Campos Técnicos Integrados**: Experiencia deportiva y período de entrenamiento actual  
- **✅ Validadores Avanzados**: Sistema compatible con prompt-toolkit async
- **✅ Simplificación UX**: Eliminación del campo redundante `competitive_level`
- **✅ Validación Temporal Inteligente**: Reconocimiento de múltiples formatos de tiempo
- **✅ Optimizaciones de Performance**: Mejor manejo de memoria y carga de datos
- **✅ Refinamientos de Interface**: Mejoras en flujo y mensajes de usuario

### 🚀 **FASES FUTURAS: INTEGRACIÓN AVANZADA**
- **Fase 4**: Integración con IA (Perplexity API) para generación de planes
- **Fase 5**: Integración con Strava API para datos de actividades reales (Opcional para MVP)
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
ℹ️  🎯 Generating outputs for: José Antonio Torres

🏆 PDF PROFESIONAL generado: outputs/ficha_tecnica_profesional_jose_antonio_torres.pdf
✅ JSON OPTIMIZADO para IA generado: outputs/athlete_profile_jose_antonio_torres_ai.json

✨ Características implementadas:
   📏 Espaciado perfecto entre bloques (14pt)
   💎 Diseño ultra-minimalista y elegante
   📄 Salto de página después de Zonas de Entrenamiento
   📊 Todos los campos siempre visibles incluido "Estado Actual" de lesiones
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
Sesión iniciada: 21/10/2025 01:10

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
- **⚠️ Indicadores Visuales**: Emoji warning cuando hay cambios pendientes (corregido)
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
│       ├── models.py            # ✅ Modelo con campo "Estado Actual" en lesiones
│       ├── cli.py               # ✅ CLI con validación corregida y nuevos campos
│       ├── cli_helpers.py       # ✅ Formato de prompts corregido
│       ├── persistence.py       # ✅ Persistencia mejorada
│       ├── calculations.py      # Cálculos, validaciones y normalizaciones
│       ├── validators.py        # ✅ Validadores compatibles con prompt-toolkit
│       ├── outputgen.py         # ✅ Generación PDF con "Estado Actual" (FASE 3)
│       ├── pdf_styles.py        # ✅ Estilos minimalistas para PDF
│       └── json_optimizer.py    # ✅ JSON optimizado con "Estado Actual" para IA
├── examples/                    # Ejemplos y datos de muestra
│   ├── mi_perfil.json          # Perfil de ejemplo (José Antonio)
│   └── athlete_profile.json    # Perfil por defecto
├── outputs/                    # Salidas generadas (PDF y JSON)
│   ├── *.pdf                   # Fichas técnicas profesionales
│   └── *_ai.json              # Perfiles optimizados para IA
├── profile_template.json       # ✅ Plantilla con "Estado Actual"
├── requirements.txt             # Dependencias del proyecto
├── README.md                   # Este archivo
└── .gitignore                  # Archivos excluidos de Git
```

### **🔑 Componentes Clave**

| Módulo | Responsabilidad | Estado |
|--------|-----------------|---------
| **models.py** | ✅ Modelo con campo "Estado Actual" en lesiones | ✅ Actualizado |
| **cli.py** | ✅ Interfaz con validación corregida y detección de cambios | ✅ Actualizado |
| **cli_helpers.py** | ✅ Formato de prompts corregido | ✅ Actualizado |
| **persistence.py** | ✅ Guardado/carga con persistencia mejorada | ✅ Actualizado |
| **calculations.py** | Lógica de negocio y validaciones | ✅ Completo |
| **validators.py** | ✅ Validadores compatibles async | ✅ Actualizado |
| **outputgen.py** | ✅ Generación PDF con "Estado Actual" | ✅ Actualizado |
| **pdf_styles.py** | Estilos minimalistas profesionales | ✅ Completo |
| **json_optimizer.py** | ✅ JSON optimizado con "Estado Actual" | ✅ Actualizado |

---

## 📋 **Datos Recolectados - ACTUALIZADOS**

### **Información Personal** (Obligatoria)
- Nombre completo, edad, género
- Altura y peso (opcionales para cálculo de BMI)

### **Métricas Fisiológicas** (Fundamentales)
- **Frecuencia Cardíaca Máxima y en Reposo** (para zonas de entrenamiento)
- VO2 Máximo (opcional, se puede estimar desde marcas)
- **🆕 Umbral de lactato** y **🆕 Variabilidad FC** (opcionales, validación mejorada)

### **🆕 Contexto de Entrenamiento REORGANIZADO** (Crítico)
- **🔄 Período de entrenamiento actual** (PRIMERA PREGUNTA - con validación temporal inteligente)
- Volumen semanal actual en kilómetros  
- Días de entrenamiento por semana
- **🆕 Experiencia deportiva total** (años practicando running)
- Historial y preferencias de entrenamiento de fuerza
- Disponibilidad de días y restricciones horarias

### **Datos de Rendimiento** (Clave para IA)
- **Marcas personales**: 5K, 10K, Media Maratón, Maratón (con fix crítico)
- Estimación automática de VO2máx basada en marcas y datos físicos

### **Objetivos de Carrera** (Orientación del Plan)
- **Objetivo principal**: Carrera, fecha, distancia, tiempo objetivo
- **Carreras intermedias**: Tests y preparación escalonada
- Análisis automático de tiempo disponible para planificación

### **🆕 Historial de Lesiones MEJORADO** (Prevención)
- Registro de lesiones pasadas con fechas y recuperación
- **✅ Estado Actual**: Campo nuevo para seguimiento de molestias actuales
- Información crítica para adaptar entrenamientos y prevenir recurrencias

---

## 🆕 **NUEVAS FUNCIONALIDADES IMPLEMENTADAS**

### **✨ Campo "Estado Actual" en Lesiones**

**Funcionalidad:**
- **Entrada opcional** durante creación/edición de lesiones
- **Seguimiento detallado** del estado actual de lesiones previas
- **Información contextual** para la IA: molestias leves, limitaciones, etc.

**Experiencia de Usuario:**
```
Tipo de lesión: Fascitis Plantar
Fecha aproximada: 2022-10
Descripción de recuperación: Fisioterapia y descanso 6 semanas
Estado actual (opcional - ej: 'molestias leves', 'limitación de movimiento'): Muy leve molestia con alta intensidad
```

**En PDF:**
```
LESIÓN · FASCITIS PLANTAR
FECHA · 2022-10  
RECUPERACIÓN · Fisioterapia y descanso 6 semanas
ESTADO ACTUAL · MUY LEVE MOLESTIA CON ALTA INTENSIDAD
```

**En JSON para IA:**
```json
{
  "injuries": [
    {
      "type": "Fascitis Plantar",
      "date_approx": "2022-10",
      "recovery_desc": "Fisioterapia y descanso 6 semanas", 
      "current_status": "Muy leve molestia con alta intensidad"
    }
  ]
}
```

### **🔄 Reordenamiento Contexto de Entrenamiento**

**Nueva Secuencia Optimizada:**
1. **🥇 Período de entrenamiento actual** (PRIMERA PREGUNTA)
2. Volumen semanal promedio actual  
3. Días de entrenamiento por semana
4. Experiencia deportiva en running
5. Disponibilidad y preferencias

**Beneficios:**
- **Contexto inmediato** para el resto de preguntas
- **Flujo más lógico** de información
- **Mejor experiencia** para el usuario

---

## 🐛 **BUG FIXES CRÍTICOS IMPLEMENTADOS**

### **🔧 Problema 1: Formato Incorrecto en CLI**
**Síntoma:** Prompts mal formateados con pistas desplazadas
**✅ Solución:** Refactorización completa de `format_prompt_with_hint()` en `cli_helpers.py`

### **🔧 Problema 2: Persistencia de Datos Rota**
**Síntoma:** Campo "Estado Actual" no se guardaba en `athlete_profile.json`
**✅ Solución:** Corrección en `AthleteProfile.to_dict()` en `models.py`

### **🔧 Problema 3: Bug Indicador de Guardado**
**Síntoma:** Icono ⚠️ persistía después del guardado exitoso
**✅ Solución:** Implementación de `deepcopy()` para actualizar baseline en `cli.py`

### **Resultado:**
- **✅ Interfaz CLI** funcionando perfectamente
- **✅ Persistencia de datos** completamente operativa
- **✅ Indicadores visuales** precisos y consistentes
- **✅ Experiencia de usuario** fluida y profesional

---

## 🆕 **VALIDACIÓN TEMPORAL INTELIGENTE MANTENIDA**

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

## 🎯 **ESTRUCTURA DEL MODELO DE DATOS ACTUALIZADA**

### **🆕 Campo Añadido en Injury:**

```python
@dataclass
class Injury:
    """Representa una lesión previa del atleta."""
    
    type: str  # Tipo de lesión
    date_approx: str  # Fecha aproximada  
    recovery_desc: str  # Descripción de recuperación
    current_status: Optional[str] = None  # ✅ NUEVO CAMPO - Estado actual
```

### **🛠️ Integración Completa:**
- **✅ Serialización JSON**: Campo incluido en `to_dict()` y `from_dict()`
- **✅ CLI Interactiva**: Pregunta opcional durante creación/edición
- **✅ Validación**: Acepta entrada vacía (valor por defecto: "No especificado")
- **✅ Outputs**: Mostrado en PDF y JSON optimizado para IA
- **✅ Template**: Incluido en `profile_template.json`

---

## 📊 **CAMBIOS TÉCNICOS IMPLEMENTADOS**

### **📁 Módulos Modificados:**

#### **src/runnerapp/models.py**
- **✅ Añadido**: Campo `current_status` en clase `Injury`
- **✅ Corregido**: Método `to_dict()` incluye el nuevo campo
- **✅ Actualizado**: Método `from_dict()` carga el nuevo campo

#### **src/runnerapp/cli.py**
- **✅ Añadido**: Pregunta "Estado actual" en `create_injury()` y `edit_injury()`
- **✅ Corregido**: Bug de detección de cambios con `deepcopy()`
- **✅ Reordenado**: Secuencia de preguntas en contexto de entrenamiento

#### **src/runnerapp/cli_helpers.py**
- **✅ Refactorizado**: Función `format_prompt_with_hint()` para formato correcto
- **✅ Mejorado**: Ensamblaje robusto de partes del prompt

#### **src/runnerapp/outputgen.py**
- **✅ Añadido**: Campo "ESTADO ACTUAL" en sección lesiones del PDF
- **✅ Mantenido**: Diseño minimalista y espaciado perfecto

#### **src/runnerapp/json_optimizer.py**
- **✅ Añadido**: Campo `current_status` en JSON optimizado para IA
- **✅ Mantenido**: Estructura auto-explicativa para modelos de IA

#### **profile_template.json**
- **✅ Actualizado**: Plantilla incluye `current_status: null` por defecto

---

## 🧪 **TESTING Y VALIDACIÓN ACTUALIZADOS**

### **Comandos de Verificación Post-Optimizaciones**
```bash
# Verificar instalación completa con nuevos cambios
python -c "from src.runnerapp.cli import start_interactive_cli; print('✅ Instalación correcta con optimizaciones')"

# Test campo "Estado Actual" en lesiones  
python -c "from src.runnerapp.models import Injury; i = Injury('test', 'date', 'rec', 'status'); print('✅ Campo Estado Actual funcionando')"

# Test generación de salidas con nuevos campos
python -m src.runnerapp.main --generate-outputs

# Test básico de funcionamiento con bug fixes
python -m src.runnerapp.main --demo

# Test de carga con nuevos campos
python -m src.runnerapp.main --load examples/mi_perfil.json
```

### **✅ Casos de Uso Validados**
- **✅ Campo "Estado Actual"**: Entrada, validación, guardado y outputs correctos
- **✅ Reordenamiento CLI**: "Período actual" como primera pregunta funcional
- **✅ Bug Fixes**: Sin errores de formato, persistencia ni indicadores
- **✅ Compatibilidad**: Carga perfecta de perfiles existentes
- **✅ Outputs**: PDF y JSON incluyendo nuevos campos correctamente
- **✅ UX Optimizada**: Flujo mejorado y más intuitivo

---

## 🔄 **Changelog Detallado**

### **🆕 v3.1.0 - Campo Estado Actual & Bug Fixes Críticos (21/10/2025)**

#### **✨ Nuevas Características:**
- **Campo "Estado Actual" en Lesiones**: Seguimiento detallado del estado actual
- **Reordenamiento Contexto Entrenamiento**: "Período actual" como primera pregunta
- **Integración Completa**: Nuevos campos en CLI, PDF, JSON y template

#### **🐛 Bug Fixes Críticos:**
- **Fixed**: Error de formato en `format_prompt_with_hint()` 
- **Fixed**: Problema de persistencia en `AthleteProfile.to_dict()`
- **Fixed**: Bug indicador de guardado persistente con `deepcopy()`
- **Fixed**: Compatibilidad con archivos de perfil existentes

#### **⚡ Optimizaciones:**
- **Improved**: Experiencia de usuario más fluida e intuitiva
- **Improved**: Orden lógico de preguntas en contexto de entrenamiento
- **Improved**: Detección precisa de cambios pendientes
- **Improved**: Robustez en formato de prompts CLI

#### **🔧 Mantenimiento:**
- **Updated**: Documentación completa con nuevas funcionalidades
- **Updated**: Casos de uso y ejemplos de salida
- **Updated**: Template y estructura de datos
- **Updated**: Testing y validación integral

---

## 📈 **Casos de Uso Principales ACTUALIZADOS**

### **1. Gestión Avanzada de Lesiones**
Registro completo con **seguimiento del estado actual**, permitiendo a la IA generar planes que consideren **molestias actuales** y **limitaciones residuales**.

### **2. Contexto de Entrenamiento Optimizado**  
Secuencia reorganizada que **prioriza el período actual**, proporcionando contexto inmediato para el resto de preguntas y mejorando la lógica del flujo.

### **3. Experiencia sin Errores**
Interface completamente **libre de bugs** con formato correcto, persistencia confiable e indicadores visuales precisos.

### **4. Outputs Profesionales Completos**
PDF y JSON que incluyen **toda la información recolectada**, incluyendo estado actual de lesiones para análisis integral de la IA.

---

## ⚙️ **Configuración Técnica ACTUALIZADA**

### **🆕 Dependencias Mantenidas**
```txt
prompt-toolkit>=3.0.0    # CLI interactiva (formato corregido)
reportlab>=4.0.0         # Generación de PDF profesional (con nuevos campos)
dataclasses              # Estructuras de datos (built-in)
typing                   # Type hints (built-in) 
json                     # Persistencia (mejorada)
datetime                 # Manejo de fechas (built-in)
pathlib                  # Manejo de rutas (built-in)
re                       # Expresiones regulares para validación temporal
copy                     # ✅ NUEVO: deepcopy para detección de cambios
```

### **🔧 Arquitectura de Módulos Actualizada**
- **models.py**: ✅ Campo "Estado Actual" en lesiones añadido
- **cli.py**: ✅ Bugs críticos solucionados, reordenamiento implementado
- **cli_helpers.py**: ✅ Formato de prompts completamente corregido
- **persistence.py**: ✅ Serialización mejorada con nuevos campos
- **outputgen.py**: ✅ PDF actualizado con "Estado Actual" 
- **json_optimizer.py**: ✅ JSON optimizado con información completa
- **validators.py**: ✅ Validadores async mantenidos y estables
- **calculations.py**: ✅ Funciones auxiliares sin cambios (estables)

---

## 🎪 **Ejemplos de Salida ACTUALIZADOS**

### **🆕 CLI con Campo "Estado Actual" (Extracto)**
```
📋 Historial de Lesiones

Tipo de lesión: Fascitis Plantar
Fecha aproximada: De 2022 a Febrero de 2025  
Descripción de recuperación: Reposo y uso de plantillas para correr
Estado actual (opcional - ej: 'molestias leves', 'limitación de movimiento'): Muy leve molestia que se agrava las semanas de más intensidad, pero no llega a impedirme correr
```

### **🆕 PDF Mejorado con Estado Actual (Extracto)**
```
                     HISTORIAL MÉDICO

LESIÓN · FASCITIS PLANTAR
FECHA · De 2022 a Febrero de 2025
RECUPERACIÓN · Reposo y uso de plantillas para correr
ESTADO ACTUAL · MUY LEVE MOLESTIA QUE SE AGRAVA LAS SEMANAS DE MÁS INTENSIDAD
```

### **🆕 JSON para IA con Información Completa (Extracto)**
```json
{
  "injury_history": {
    "injuries": [
      {
        "type": "Fascitis Plantar",
        "date_approx": "De 2022 a Febrero de 2025",
        "recovery_desc": "Reposo y uso de plantillas para correr",
        "current_status": "Muy leve molestia que se agrava las semanas de más intensidad"
      }
    ],
    "injury_analysis": "Atleta con lesión crónica manejada que requiere monitoreo en entrenamientos de alta intensidad"
  }
}
```

### **🔄 Contexto de Entrenamiento Reordenado (Extracto)**
```
📋 Contexto de Entrenamiento

Período de entrenamiento actual (ej: '3 semanas', '2 meses', '2 m', 'empezando'): 1 semana
Volumen semanal promedio actual (kilómetros por semana - ej: 50.0): 56.0
Días de entrenamiento por semana (contexto actual - ej: 4 o 4-5 para rango): 4
Experiencia deportiva en running (años totales practicando running - ej: 5 o 2.5): 8.0
```

---

## 🤝 **Contribución ACTUALIZADA**

El proyecto está en desarrollo activo con **optimizaciones post-Fase 3 completadas exitosamente**. Para contribuir:

1. **Fork** del repositorio actualizado
2. **Crear branch** para nuevas características: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -am 'Añadir nueva característica'`
4. **Push** al branch: `git push origin feature/nueva-caracteristica`
5. **Crear Pull Request** con descripción detallada

### **🆕 Áreas de Contribución Post-Optimizaciones**
- **Campos de Seguimiento**: Nuevos tipos de información para seguimiento de lesiones
- **Optimizaciones UX**: Mejoras continuas en flujo de usuario y experiencia
- **Integración IA**: Preparación para Fase 4 con generación de planes
- **Análisis Avanzado**: Procesamiento inteligente de estado actual de lesiones
- **Performance**: Optimizaciones continuas de memoria y velocidad

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
- **🆕 Bug Reports**: Para reportar problemas con nuevos campos o funcionalidades

**¡Transforma tu entrenamiento con ciencia, tecnología y seguimiento detallado de tu estado actual!** 🏃‍♂️🤖📄✨