# RUNNING Fit-Tech 🏃‍♂️

**AI-Powered Training Assistant for Runners**

Una aplicación CLI profesional que transforma los datos del atleta en fichas técnicas detalladas y planes de entrenamiento personalizados usando inteligencia artificial.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![CLI Application](https://img.shields.io/badge/interface-CLI-green.svg)](https://en.wikipedia.org/wiki/Command-line_interface)
[![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![PDF Generation](https://img.shields.io/badge/output-PDF%2FJSON-red.svg)](https://github.com/joseantonio2001/Running-Fit-Tech)

---

## 📋 **Tabla de Contenidos**

- [🚀 Características Principales](#-características-principales)
- [🎯 ¿Qué Hace Esta Aplicación?](#-qué-hace-esta-aplicación)
- [📦 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [🎮 Guía de Uso](#-guía-de-uso)
- [📊 Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [🧠 Inteligencia Artificial](#-inteligencia-artificial)
- [📁 Archivos de Salida](#-archivos-de-salida)
- [🔧 Estructura del Proyecto](#-estructura-del-proyecto)
- [🤝 Contribución](#-contribución)
- [📋 Changelog](#-changelog)

---

## 🚀 **Características Principales**

### ✨ **Funcionalidades Implementadas (Fases 1-5)**

- **🏃‍♂️ Perfil de Atleta Completo**: Captura datos personales, fisiológicos, entrenamiento y objetivos
- **📊 Análisis Deportivo Avanzado**: Cálculos automáticos de zonas de FC, VO2máx, y métricas de rendimiento
- **🎯 Gestión de Objetivos**: Sistema completo para carreras principales e intermedias
- **🏥 Historial Médico**: Registro detallado de lesiones y estado actual
- **📄 Generación de Fichas PDF**: Documentos profesionales con diseño personalizable
- **🤖 Planes de Entrenamiento con IA**: Generación automática usando Google Gemini
- **💾 Múltiples Formatos**: Salidas en JSON, Markdown y PDF
- **🖥️ Interfaz CLI Intuitiva**: Experiencia de usuario guiada y profesional

### 🆕 **Novedad Fase 5: Integración con IA**

- **🧠 Google Gemini AI**: Migración de Perplexity para mejor calidad de planes
- **📋 Planes Detallados**: Informes técnicos con estructura profesional
- **⚙️ Configuración Automática**: Manejo inteligente del estado actual del atleta
- **📊 Múltiples Salidas**: Markdown renderizado, JSON estructurado y PDF optimizado

---

## 🎯 **¿Qué Hace Esta Aplicación?**

RUNNING Fit-Tech es un **asistente de entrenamiento integral** que:

1. **📝 Recopila tu información deportiva** mediante un cuestionario interactivo inteligente
2. **🧮 Calcula automáticamente** tus zonas de entrenamiento, ritmos y métricas clave
3. **📊 Genera una ficha técnica profesional** en formato PDF lista para compartir
4. **🤖 Crea planes de entrenamiento personalizados** usando inteligencia artificial avanzada
5. **💾 Exporta todo en múltiples formatos** para máxima compatibilidad

### 🎯 **Casos de Uso Perfectos**

- **🏃‍♂️ Corredores**: Desde principiantes hasta atletas experimentados
- **👨‍⚕️ Entrenadores**: Documentación profesional de atletas
- **🏥 Médicos Deportivos**: Fichas técnicas para evaluaciones
- **🏃‍♀️ Clubes de Running**: Gestión de perfiles de miembros
- **📊 Análisis Personal**: Seguimiento detallado de progreso

---

## 📦 **Instalación**

### **Requisitos del Sistema**

- **Python 3.9+** (Recomendado: Python 3.11+)
- **Sistema Operativo**: Windows 10+, macOS, Linux
- **Espacio en Disco**: ~50MB para dependencias
- **Conexión a Internet**: Requerida para funcionalidades de IA

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/joseantonio2001/Running-Fit-Tech.git
cd Running-Fit-Tech
```

### **Paso 2: Crear Entorno Virtual (Recomendado)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Paso 3: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### **Dependencias Principales:**

```
# Interfaz CLI Avanzada
prompt-toolkit>=3.0.0

# Generación de PDFs
reportlab>=4.0.0
weasyprint

# Funcionalidades de IA
google-generativeai
python-dotenv>=1.0.0

# Renderizado Markdown
markdown-it-py 
mdit-py-plugins
linkify-it-py

# Utilidades
requests>=2.31.0
```

### **Paso 4: Verificar Instalación**

```bash
python -m src.runnerapp.main --help
```

Si todo está correcto, verás la ayuda de la aplicación con todas las opciones disponibles.

---

## ⚙️ **Configuración**

### **🔑 API Key de Google Gemini (Para Planes IA)**

Para usar la funcionalidad de **generación de planes con IA**, necesitas una API key de Google Gemini:

#### **1. Obtener API Key:**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API key
4. Copia la clave generada

#### **2. Configurar API Key:**

**🌟 Opción Recomendada: Archivo `.env`**

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Archivo .env
GOOGLE_API_KEY=tu-api-key-aqui
```

**🔧 Opción Alternativa: Variables de Entorno**

```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY="tu-api-key-aqui"

# Windows (CMD)
set GOOGLE_API_KEY=tu-api-key-aqui

# macOS/Linux
export GOOGLE_API_KEY='tu-api-key-aqui'
```

#### **3. Verificar Configuración:**

```bash
python -m src.runnerapp.main --test-ai
```

---

## 🎮 **Guía de Uso**

### **🚀 Inicio Rápido**

```bash
# Modo interactivo completo (Recomendado para primera vez)
python -m src.runnerapp.main

# Generar solo ficha técnica PDF + JSON
python -m src.runnerapp.main --generate-outputs

# Generar plan de entrenamiento con IA
python -m src.runnerapp.main --generate-plan

# Probar conexión con IA
python -m src.runnerapp.main --test-ai
```

### **📋 Flujo de Trabajo Típico**

#### **1. 📝 Crear Perfil de Atleta (Primera Vez)**

```bash
python -m src.runnerapp.main
```

La aplicación te guiará a través de **6 secciones principales**:

1. **👤 Información Personal** (Nombre, edad, género, medidas físicas)
2. **💓 Métricas Fisiológicas** (FC máx/reposo, VO2máx, umbrales)
3. **🏃‍♂️ Contexto de Entrenamiento** (Volumen, experiencia, disponibilidad)
4. **🏆 Datos de Rendimiento** (Marcas personales en diferentes distancias)
5. **🎯 Objetivos de Carrera** (Carrera principal + carreras intermedias)
6. **🏥 Historial de Lesiones** (Lesiones previas y estado actual)

#### **2. 📊 Generar Ficha Técnica**

Al finalizar el perfil, la aplicación ofrece generar automáticamente:
- **📄 Ficha Técnica PDF**: Documento profesional completo
- **💾 Perfil Optimizado JSON**: Datos estructurados para IA

#### **3. 🤖 Crear Plan de Entrenamiento**

```bash
python -m src.runnerapp.main --generate-plan
```

La IA generará un plan personalizado que incluye:
- **📅 Cronograma semanal detallado**
- **🎯 Sesiones específicas por día**
- **📊 Volúmenes y intensidades**
- **💡 Justificaciones técnicas**
- **🏥 Adaptaciones por lesiones**

---

## 📊 **Funcionalidades Detalladas**

### **🏃‍♂️ Análisis Deportivo Automático**

La aplicación calcula automáticamente:

#### **💓 Zonas de Frecuencia Cardíaca**
- **Zona 1 (Recuperación)**: 50-60% FCmáx
- **Zona 2 (Aeróbico Base)**: 60-70% FCmáx  
- **Zona 3 (Aeróbico)**: 70-80% FCmáx
- **Zona 4 (Umbral Anaeróbico)**: 80-90% FCmáx
- **Zona 5 (Anaeróbico)**: 90-100% FCmáx

#### **🏃‍♂️ Ritmos de Entrenamiento**
- **Ritmo de Maratón**: Basado en VO2máx y experiencia
- **Ritmo de Media Maratón**: Ajustado por perfil fisiológico
- **Ritmo de 10K**: Calculado con fórmulas deportivas validadas
- **Ritmo de 5K**: Optimizado para distancias cortas

#### **📈 Métricas de Rendimiento**
- **VDOT**: Predictor de rendimiento de Jack Daniels
- **Índice de Eficiencia**: Relación VO2máx/FC
- **Progresión Semanal**: Incrementos seguros de volumen
- **Tiempo de Recuperación**: Basado en edad y experiencia

### **🎯 Gestión Inteligente de Objetivos**

#### **🏁 Carrera Principal**
- Definición de objetivo específico (nombre, fecha, distancia, tiempo meta)
- Cálculo automático de semanas disponibles para entrenamiento
- Análisis de viabilidad del objetivo basado en marcas actuales
- Sugerencias de estrategia de carrera

#### **🏃‍♀️ Carreras Intermedias**
- Sistema completo CRUD (Crear, Leer, Actualizar, Eliminar)
- Integración inteligente con el plan principal
- Análisis de impacto en la periodización
- Recomendaciones de distancias preparatorias

### **🏥 Manejo Profesional de Lesiones**

#### **📋 Registro Detallado**
- **Historial completo**: Lesiones previas con fechas y gravedad
- **Estado actual**: Molestias, dolores o limitaciones activas
- **Impacto en entrenamiento**: Análisis de actividades restringidas
- **Recomendaciones**: Adaptaciones automáticas en planes

#### **🤖 Adaptaciones Automáticas en IA**
- La IA considera automáticamente el historial médico
- Modifica intensidades y volúmenes según limitaciones
- Incluye ejercicios de prevención específicos
- Sugiere alternativas de bajo impacto cuando es necesario

---

## 🧠 **Inteligencia Artificial**

### **🚀 Google Gemini Integration**

RUNNING Fit-Tech usa **Google Gemini**, la IA más avanzada de Google, para generar planes de entrenamiento de calidad profesional.

#### **🎯 ¿Por Qué Google Gemini?**

- **📊 Respuestas Estructuradas**: Control total sobre formato JSON
- **🧠 Comprensión Contextual**: Entiende matices del entrenamiento deportivo
- **🔄 Consistencia**: Resultados reproducibles y fiables
- **⚡ Velocidad**: Generación rápida de planes detallados
- **🎯 Especialización**: Optimizado para tareas técnicas complejas

#### **🔧 Ingeniería de Prompts Avanzada**

El sistema usa **prompts iterativamente refinados** que incluyen:

1. **📋 Contexto Deportivo Completo**: Todo el perfil del atleta estructurado
2. **🎯 Objetivos Específicos**: Carrera meta con fechas y distancias exactas
3. **🏥 Consideraciones Médicas**: Historial de lesiones y limitaciones
4. **📅 Disponibilidad Real**: Días y horarios disponibles para entrenar
5. **📈 Estado Actual**: Carga de entrenamiento y forma física actual

#### **🎨 Características del Prompt**

```
✅ Contexto de estado actual del atleta
✅ Reglas de excepción para semanas de competición  
✅ Progresión gradual y segura
✅ Estructura JSON controlada con plan_markdown y plan_structured
✅ Detalle técnico: Calentamiento, Parte Principal, Enfriamiento
✅ Métricas específicas: RPE, FC, ritmos por zona
✅ Justificación pedagógica de cada sesión
```

### **📊 Estructura del Plan Generado**

#### **🗂️ Plan Markdown (Legible)**

```markdown
# Informe de Planificación de Entrenamiento

## 📊 Análisis del Atleta
[Análisis personalizado basado en datos]

## 📅 Cronograma Detallado

### Semana 1: Base Aeróbica
**Volumen objetivo:** 45 km

| Día | Entrenamiento | Duración | Zona FC | RPE | Notas |
|-----|---------------|----------|---------|-----|-------|
| Lun | Trote Suave | 45 min | Z2 | 6/10 | Activación semanal |
| Mar | Intervalos | 60 min | Z4-Z5 | 8/10 | 6x800m en pista |
| ... | ... | ... | ... | ... | ... |

### Consideraciones Especiales
- Prevención de lesiones específica
- Estrategia nutricional
- Protocolo de recuperación
```

#### **🤖 Plan Estructurado (JSON)**

```json
{
  "plan_metadata": {
    "athlete_name": "José Antonio Torres",
    "race_goal": "Media Maratón Valencia 2024",
    "plan_duration": "12 semanas",
    "generated_date": "2024-11-25"
  },
  "weekly_structure": [
    {
      "week": 1,
      "theme": "Base Aeróbica",
      "total_volume": "45 km",
      "sessions": [...]
    }
  ]
}
```

---

## 📁 **Archivos de Salida**

RUNNING Fit-Tech genera múltiples formatos para máxima flexibilidad:

### **📄 Ficha Técnica (Perfil del Atleta)**

#### **1. Ficha PDF Profesional** 
```
outputs/ficha_tecnica_profesional_[nombre]_[fecha].pdf
```

**🎨 Características:**
- **Diseño profesional** con colores y tipografías optimizadas
- **Tablas estructuradas** con datos organizados
- **Gráficos automáticos** de zonas de FC
- **Secciones claramente definidas** y navegables
- **Información de contacto** y datos técnicos completos
- **Optimizado para impresión** y compartir digitalmente

#### **2. Perfil JSON Optimizado para IA**
```
outputs/athlete_profile_[nombre]_ai.json
```

**🤖 Características:**
- **Estructura optimizada** para consumo por IA
- **Datos normalizados** y validados
- **Campos expandidos** con contexto adicional
- **Metadatos incluidos** (fecha generación, versión)
- **Compatible** con sistemas de terceros

### **🤖 Plan de Entrenamiento (Generado por IA)**

#### **1. Plan PDF Detallado**
```
outputs/plan_entrenamiento_[nombre]_[fecha].pdf
```

**📋 Contenido:**
- **Informe ejecutivo** con análisis del atleta
- **Cronograma semanal** con tablas detalladas por día
- **Sesiones específicas** con calentamiento, parte principal y enfriamiento
- **Métricas por sesión**: RPE, zonas FC, ritmos específicos
- **Consideraciones especiales** médicas y nutricionales
- **Estrategia de carrera** para el objetivo meta

#### **2. Plan Markdown (Editable)**
```
outputs/plan_entrenamiento_[nombre]_[fecha].md
```

**✏️ Ventajas:**
- **Formato editable** para personalización
- **Compatible con editores** (Notion, Obsidian, VS Code)
- **Estructura clara** con headers y tablas
- **Fácil conversión** a otros formatos
- **Control de versiones** amigable

#### **3. Plan JSON Estructurado**
```
outputs/plan_entrenamiento_[nombre]_[fecha].json
```

**🔧 Usos:**
- **Integración con apps** de entrenamiento
- **Análisis automatizado** de datos
- **Desarrollo de herramientas** personalizadas
- **Backup estructurado** de información

---

## 🔧 **Estructura del Proyecto**

```
Running-Fit-Tech/
├── 📁 src/runnerapp/           # Código principal
│   ├── 🏃 main.py             # Punto de entrada
│   ├── 🖥️ cli.py              # Interfaz de línea de comandos
│   ├── 📊 models.py           # Modelos de datos (AthleteProfile)
│   ├── 🧮 calculations.py     # Cálculos deportivos y fisiológicos
│   ├── 💾 persistence.py      # Guardado y carga de datos
│   ├── 📄 outputgen.py        # Generación de PDFs y archivos
│   ├── 🤖 ai_interface.py     # Integración con Google Gemini
│   ├── 🎨 pdf_styles.py       # Estilos para documentos PDF
│   └── 🔧 cli_helpers.py      # Utilidades para interfaz CLI
├── 📁 outputs/                # Archivos generados
│   ├── 📄 *.pdf              # Fichas técnicas y planes
│   ├── 📝 *.md               # Planes en Markdown
│   └── 💾 *.json             # Datos estructurados
├── 📁 assets/                 # Recursos estáticos
│   ├── 🎨 plan_style.css     # Estilos CSS para planes PDF
│   └── 📊 *.json             # Templates y configuraciones
├── ⚙️ requirements.txt        # Dependencias Python
├── 🔑 .env                    # Variables de entorno (crear)
├── 📋 athlete_profile.json    # Perfil actual del atleta
└── 📖 README.md              # Esta documentación
```

### **🧩 Módulos Principales**

#### **🏃 `main.py`** - Coordinador General
- **🎯 Punto de entrada** único de la aplicación
- **🚀 Parsing de argumentos** de línea de comandos
- **🔄 Coordinación de flujos** (perfil → ficha → plan)
- **🖥️ Interfaz con usuario** y manejo de errores

#### **🖥️ `cli.py`** - Experiencia de Usuario
- **📝 Cuestionario interactivo** guiado por secciones
- **✅ Validación en tiempo real** de todas las entradas
- **🎨 Interfaz rica** con colores y formateo
- **💾 Gestión de estado** y guardado automático
- **🔄 Navegación intuitiva** entre secciones

#### **📊 `models.py`** - Estructura de Datos
- **🏗️ AthleteProfile**: Clase principal con todos los datos
- **🎯 Campos especializados**: Objetivos, lesiones, rendimiento
- **✅ Validación automática** de tipos y rangos
- **🔄 Serialización JSON** optimizada

#### **🧮 `calculations.py`** - Motor de Cálculos
- **💓 Zonas de FC**: Fórmulas validadas científicamente
- **🏃‍♂️ Ritmos de entrenamiento**: Basados en VO2máx y VDOT
- **📈 Predicciones de rendimiento**: Algoritmos de Jack Daniels
- **⚖️ Normalizaciones**: BMI, eficiencia cardíaca, etc.

#### **🤖 `ai_interface.py`** - Motor de IA
- **🔧 Configuración automática** de Google Gemini
- **📝 Construcción de prompts** altamente especializados
- **🔄 Manejo de respuestas** JSON estructuradas
- **⚡ Reintentos automáticos** y manejo de errores
- **🎯 Optimización de contexto** para mejores resultados

#### **📄 `outputgen.py`** - Generación de Documentos
- **🎨 PDFs profesionales** con ReportLab y WeasyPrint
- **📝 Renderizado Markdown** a HTML/PDF
- **💾 Exportación JSON** optimizada
- **🔧 Gestión de archivos** y directorios
- **🎯 Templates personalizables** y reutilizables

---

## 🤝 **Contribución**

¡Las contribuciones son bienvenidas! Este proyecto sigue las mejores prácticas de desarrollo colaborativo:

### **🔄 Proceso de Contribución**

1. **🍴 Fork** el repositorio
2. **🌿 Crea una rama** para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **💾 Commit** tus cambios: `git commit -m 'Add: Nueva funcionalidad increíble'`
4. **📤 Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **📝 Abre un Pull Request** con descripción detallada

### **📋 Estándares de Código**

- **🐍 PEP 8**: Seguir estándares de estilo Python
- **📝 Documentación**: Docstrings en todas las funciones públicas
- **✅ Tipado**: Type hints obligatorios en funciones principales
- **🧪 Testing**: Tests unitarios para funcionalidades críticas
- **🔧 Modularidad**: Separación clara de responsabilidades

### **🎯 Areas de Mejora Priorizadas**

#### **🏆 Alta Prioridad**
- **🌐 Integración Strava**: Importación automática de datos
- **📱 Interfaz Web**: Dashboard complementario al CLI
- **📊 Analytics Avanzados**: Gráficos de progreso y tendencias
- **🔄 Sincronización**: Backup en la nube automático

#### **⭐ Media Prioridad**  
- **🗣️ Soporte multiidioma**: i18n completo
- **🎨 Temas personalizables**: Dark mode, colores custom
- **📈 Métricas adicionales**: Más cálculos deportivos
- **🏃‍♀️ Deportes adicionales**: Ciclismo, natación, triatlón

#### **💡 Funcionalidades Futuras**
- **📱 App móvil**: Companion app para seguimiento
- **🤖 Más proveedores IA**: OpenAI, Anthropic, etc.
- **👥 Equipos/Clubes**: Gestión multi-atleta
- **📊 Integración wearables**: Garmin, Polar, Fitbit

---

## 📋 **Changelog**

### **🚀 v1.0.0 - Fase 5: Integración IA Completa** *(Octubre 2025)*

#### **🆕 Nuevas Características**
- **🤖 Integración Google Gemini**: Planes de entrenamiento con IA de última generación
- **📊 Planes Detallados**: Informes técnicos profesionales con estructura completa
- **🔧 Configuración .env**: Manejo robusto de claves API con python-dotenv
- **📄 PDFs Optimizados**: Renderizado perfecto de tablas Markdown a PDF
- **🎯 Comando --generate-plan**: Generación directa desde CLI
- **⚡ Comando --test-ai**: Verificación de conexión con IA

#### **🔧 Mejoras Técnicas**
- **📝 Prompt Engineering**: Prompts iterativamente refinados para mejores resultados  
- **🔄 Manejo de Estado**: Consideración automática del entrenamiento actual
- **🏥 Adaptaciones Médicas**: IA considera automáticamente historial de lesiones
- **📊 Múltiples Formatos**: Markdown, JSON estructurado y PDF en una sola generación

#### **🐛 Correcciones**
- **📄 Bug tablas PDF**: Solucionado renderizado con preset 'gfm-like'
- **📏 Márgenes optimizados**: CSS mejorado para mejor presentación
- **📃 Saltos de página**: Evita cortes en medio de tablas
- **🔧 Importaciones JIT**: Solucionados errores de WeasyPrint en Windows

#### **📦 Dependencias Actualizadas**
```
+ google-generativeai      # Motor de IA principal
+ python-dotenv>=1.0.0     # Manejo de variables de entorno
+ linkify-it-py            # Procesamiento de enlaces en Markdown  
+ mdit-py-plugins          # Plugins para renderizado Markdown
```

---

### **📊 v0.9.0 - Fase 4: Funcionalidades Avanzadas** *(Octubre 2025)*

#### **🆕 Características Añadidas**
- **🎯 Sistema completo de objetivos**: Carrera principal + intermedias
- **🏥 Historial médico detallado**: Lesiones y estado actual
- **📊 Análisis deportivo avanzado**: VDOT, eficiencia, predicciones
- **🔄 Gestión CRUD completa**: Crear, editar, eliminar objetivos/lesiones
- **⚡ Validación mejorada**: Campos especializados con rangos específicos

#### **🔧 Mejoras de Sistema**
- **📐 Arquitectura modular**: Separación clara de responsabilidades
- **💾 Persistencia robusta**: Sistema de guardado automático
- **🎨 Interfaz enriquecida**: Colores, iconos y formateo avanzado
- **⚠️ Manejo de errores**: Recuperación inteligente de fallos

---

### **📄 v0.7.0 - Fase 3: Generación PDF** *(Octubre 2025)*

#### **🆕 Funcionalidades Clave**
- **📄 Generación PDF profesional**: Fichas técnicas con diseño personalizado
- **💾 Exportación JSON**: Datos estructurados para integración
- **📊 Cálculos automáticos**: Zonas FC, ritmos, métricas deportivas
- **🎨 Diseño personalizable**: Estilos CSS para documentos

#### **🔧 Arquitectura**
- **📦 Sistema modular**: Separación outputgen, calculations, pdf_styles
- **🏗️ Clases especializadas**: Modelos de datos robustos
- **⚡ Optimización**: Generación rápida de documentos complejos

---

### **🖥️ v0.5.0 - Fase 2: CLI Avanzada** *(Octubre 2025)*

#### **🆕 Características CLI**
- **🖥️ Interfaz rica con prompt-toolkit**: Experiencia de usuario profesional  
- **📝 Cuestionario guiado**: 6 secciones organizadas lógicamente
- **✅ Validación en tiempo real**: Prevención de errores de entrada
- **🔄 Navegación fluida**: Sistema de menús intuitivo

---

### **🏗️ v0.3.0 - Fase 1: Fundación** *(Octubre 2025)*

#### **🆕 Estructura Base**
- **🏃‍♂️ Modelo AthleteProfile**: Estructura de datos completa
- **💾 Sistema de persistencia**: JSON con validación automática  
- **🧮 Cálculos básicos**: FC, BMI, métricas fundamentales
- **📁 Organización del proyecto**: Arquitectura escalable establecida

---

## 📞 **Soporte y Contacto**

### **🐛 Reportar Bugs**
- **📧 GitHub Issues**: [Crear nuevo issue](https://github.com/joseantonio2001/Running-Fit-Tech/issues)
- **📋 Template de Bug**: Usar template proporcionado con pasos para reproducir
- **🔍 Información útil**: Incluir versión Python, OS, logs de error

### **💡 Solicitar Funcionalidades**
- **🌟 Feature Requests**: [Abrir discusión](https://github.com/joseantonio2001/Running-Fit-Tech/discussions)
- **🗳️ Votación**: Votar funcionalidades existentes para priorizarlas
- **📝 Propuestas**: Incluir casos de uso y mockups cuando sea posible

### **📚 Documentación Adicional**
- **🔧 API Reference**: [Wiki del proyecto](https://github.com/joseantonio2001/Running-Fit-Tech/wiki)
- **📹 Video tutoriales**: [Canal de YouTube](https://youtube.com/@runningfittech) (próximamente)
- **💬 Comunidad**: [Discord Server](https://discord.gg/runningfittech) (próximamente)

---

## 📄 **Licencia**

Este proyecto está bajo la **Licencia MIT**. Ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License - Copyright (c) 2025 José Antonio Torres

Se concede permiso, libre de cargos, a cualquier persona que obtenga una 
copia de este software y de los archivos de documentación asociados, 
para utilizar el Software sin restricción, incluyendo sin limitación 
los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, 
sublicenciar, y/o vender copias del Software...
```

---

<div align="center">

## 🏃‍♂️ **¡Transforma tu Entrenamiento con IA!**

**Desarrollado con ❤️ por la comunidad de corredores**

[![⭐ Star en GitHub](https://img.shields.io/github/stars/joseantonio2001/Running-Fit-Tech?style=social)](https://github.com/joseantonio2001/Running-Fit-Tech)
[![🍴 Fork el Proyecto](https://img.shields.io/github/forks/joseantonio2001/Running-Fit-Tech?style=social)](https://github.com/joseantonio2001/Running-Fit-Tech/fork)
[![👥 Contributors](https://img.shields.io/github/contributors/joseantonio2001/Running-Fit-Tech)](https://github.com/joseantonio2001/Running-Fit-Tech/graphs/contributors)

</div>

---

*🏃‍♂️ RUNNING Fit-Tech - Donde la ciencia del deporte se encuentra con la inteligencia artificial*