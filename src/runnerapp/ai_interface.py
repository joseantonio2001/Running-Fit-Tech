"""
Módulo de Interfaz con IA (Fase 5)

Gestiona la comunicación con la API de Perplexity, incluyendo:
- Ingeniería de prompts de alta calidad.
- Solicitud de un formato JSON estructurado a la IA.
- Gestión segura de claves API (variables de entorno).
- Feedback al usuario durante la espera.
- Parseo y validación robusta de la respuesta JSON de la IA.
"""

import os
import json
import requests
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv

import google.generativeai as genai

from .models import AthleteProfile
from .json_optimizer import optimize_profile_for_ai
from .cli_helpers import print_error, print_info, print_success

# URL de la API de Perplexity
#PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# Modelo recomendado para tareas complejas de generación de planes
# (Requiere un modelo con gran contexto y capacidad de seguir instrucciones JSON)
MODEL_NAME = "gemini-2.5-pro"

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def _configure_gemini() -> bool:
    """
    Configura la API de Gemini usando la clave del archivo .env.
    
    Returns:
        bool: True si la configuración fue exitosa, False en caso contrario.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print_error("Error: Variable GOOGLE_API_KEY no encontrada.")
        print_info("Asegúrese de que exista un archivo .env en la raíz del proyecto")
        print_info("con el contenido: GOOGLE_API_KEY=\"su_clave_aqui\"")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print_error(f"Error configurando la API de Gemini: {e}")

def _build_prompt_for_gemini(profile: AthleteProfile) -> str:
    """
    Construye el prompt optimizado y detallado para Gemini v2.

    Solicita JSON, estructura semanal separada, y mayor detalle técnico.
    Incluye la excepción para días no disponibles en semanas de competición.

    Args:
        profile: El perfil del atleta optimizado.

    Returns:
        str: El prompt listo para enviar a Gemini.
    """
    ai_optimized_profile = optimize_profile_for_ai(profile)
    profile_json_string = json.dumps(ai_optimized_profile, indent=2, ensure_ascii=False)

    prompt_text = f"""
    Eres un entrenador de running de élite mundial, Doctor en fisiología del ejercicio,
    con certificación USATF Nivel 3 y especialización en biomecánica y prevención de
    lesiones. Tu misión es crear planes de entrenamiento hiper-personalizados,
    científicamente fundamentados y extremadamente detallados. Analiza meticulosamente
    cada dato del perfil adjunto.

    FICHA TÉCNICA DEL ATLETA (JSON):
    ```json
    {profile_json_string}
    ```

    TAREA PRINCIPAL:
    Basándote en un análisis exhaustivo y técnico de CADA CAMPO del JSON anterior
    (especialmente `main_objective`, `training_context`, `performance_data`, `physiological_metrics`
    y OBLIGATORIAMENTE `injury_history` y su `current_status`), genera un
    "Informe de Planificación de Entrenamiento" completo y detallado para que el atleta
    alcance su `main_objective`.

    REGLAS IMPORTANTES PARA EL PLAN:
    1.  **Disponibilidad General:** Respeta estrictamente los días indicados en `training_context.availability_constraints.unavailable_days` como días de DESCANSO OBLIGATORIO.
    2.  **EXCEPCIÓN - Semanas de Competición:** IGNORA `unavailable_days` ÚNICAMENTE durante las semanas que contengan una carrera (`main_objective` o `intermediate_races`). Programa sesiones de activación/descanso activo apropiadas en esos días si es beneficioso (ej., activación el día previo). En el resto de semanas, la restricción es absoluta.
    3.  **Gestión de Lesiones:** MÁXIMA PRIORIDAD. Dada la `injury_history` y el `current_status`, diseña una progresión de volumen e intensidad extremadamente cautelosa. Incluye:
        * Notas específicas de prevención DENTRO de la tabla semanal (ej., "Vigilar molestias tibiales", "Priorizar superficie blanda si es posible").
        * Una sección detallada en la justificación inicial explicando la estrategia anti-lesión.
    4.  **Entrenamiento de Fuerza:** Si `include_strength_training` es `true`, integra 1-2 sesiones semanales de fuerza funcional (ejercicios específicos, series/reps) en días de bajo impacto. Si es `false`/`null`, no incluyas fuerza y menciónalo en la justificación.
    5.  **Detalle de Sesiones:** Para CADA sesión de entrenamiento (excepto descanso), especifica:
        * **Calentamiento (Cal.):** Duración y tipo.
        * **Parte Principal:** Descripción clara, duración/distancia, RITMOS específicos (ej., 4:15/km - 4:25/km) y/o RANGOS DE FC precisos (ej., 155-170 bpm) derivados de los datos del perfil (zonas Karvonen, umbral si disponible), y RPE objetivo (escala 1-10).
        * **Enfriamiento (Enf.):** Duración y tipo.
    6.  **Ritmos/Zonas:** Basa los ritmos/zonas en los PBs, VO2max, FCmax/reposo, Umbrales, HRV y objetivo del atleta. Sé lo más específico posible.

    REQUISITOS OBLIGATORIOS PARA LA ESTRUCTURA DE SALIDA (JSON):
    Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido, sin texto adicional.
    Estructura exacta:
    ```json
    {{
      "plan_markdown": "...", // String Markdown detallado
      "plan_structured": [ ... ] // Array de objetos JSON (sin cambios en su estructura)
    }}
    ```

    CONTENIDO DETALLADO REQUERIDO DENTRO DE "plan_markdown":

    1.  **Título Técnico:** Usa "## Informe de Planificación de Entrenamiento para [Nombre Atleta]".
    2.  **Justificación Detallada:** Sección "### Justificación y Estrategia Fisiológica". Explica en detalle cómo el plan aborda: objetivo vs. PBs, métricas disponibles (VO2max, umbral de lactato, HRV ...),  gestión de riesgo de lesión, progresión de volumen/intensidad, distribución semanal, disponibilidad (incluida la excepción), ausencia/presencia de fuerza, y cómo se usarán las carreras intermedias. Sé técnico y específico.
    3.  **Plan Semanal Detallado:**
        * Usa un encabezado `## Plan Detallado Semanal`.
        * Para CADA SEMANA, incluye:
            * Un encabezado `### Semana X (DD/MM - DD/MM) - Enfoque: [Breve descripción del objetivo semanal]`.
            * Un PÁRRAFO introductorio corto resumiendo la carga, enfoque e hitos de esa semana.
            * Una TABLA MARKDOWN separada para esa semana con las columnas: | Día | Sesión | Calentamiento | Parte Principal (Ritmo/FC/RPE) | Enfriamiento | Notas Prevención/Ejecución |.
            * Para semanas con CARRERAS (`intermediate_races` o `main_objective`): Incluye una breve recomendación de ESTRATEGIA DE RITMO en las notas del día de la carrera.

    CONTENIDO DETALLADO REQUERIDO DENTRO DE "plan_structured":
    * Misma estructura que antes (array de objetos diarios). Asegúrate de que `details` refleje el mayor detalle solicitado (Cal/Ppal/Enf, Ritmos/FC/RPE).
        ```json
        {{
          "week": <int>,
          "day_of_week": <int>, // 1=Lunes
          "day_description": "<str>", // "Semana 1 - Lunes"
          "session_type": "<str>", // Ej: "Rodaje Z2", "Tempo Umbral", "Descanso", "Activación"
          "details": "<str>" // Ej: "Cal: 15' Z1 + Movilidad. Ppal: 20' @ 4:15-4:25/km (FC 155-170bpm, RPE 7/10). Enf: 10' Z1 + Estir."
        }}
        ```

    Recuerda: Solo el objeto JSON como respuesta final. Sé exhaustivo, técnico y preciso. La seguridad del atleta (prevención de lesiones) es primordial.
    """
    return prompt_text     

def _get_api_key() -> Optional[str]:
    """
    Obtiene la clave de API de Perplexity de forma segura desde variables de entorno.
    
    Returns:
        Optional[str]: La clave de API, o None si no se encuentra.
    """
    load_dotenv()

    api_key = os.getenv("PERPLEXITY_API_KEY") # Usar os.getenv es más seguro
    if not api_key:
        print_error("Error: Variable PERPLEXITY_API_KEY no encontrada.")
        print_info("Asegúrese de que exista un archivo .env en la raíz del proyecto")
        print_info("con el contenido: PERPLEXITY_API_KEY=\"su_clave_aqui\"")
        print_info("O configure la variable de entorno del sistema.")
        return None
    return api_key

def _build_prompt_for_gemini(profile: AthleteProfile) -> str:
    """
    Construye el prompt optimizado y detallado para Gemini v2.

    Solicita JSON, estructura semanal separada, y mayor detalle técnico.
    Incluye la excepción para días no disponibles en semanas de competición.

    Args:
        profile: El perfil del atleta optimizado.

    Returns:
        str: El prompt listo para enviar a Gemini.
    """
    ai_optimized_profile = optimize_profile_for_ai(profile)
    # Convertir a JSON string para el prompt
    # Nota: Asegúrate de que json_optimizer incluye 'unavailable_days', 'main_objective', 'intermediate_races'
    profile_json_string = json.dumps(ai_optimized_profile, indent=2, ensure_ascii=False)

    # Combinamos rol, tarea y formato de salida en un único prompt
    prompt_text = f"""
    Eres un entrenador de running de élite mundial, Doctor en fisiología del ejercicio,
    con certificación USATF Nivel 3 y especialización en biomecánica y prevención de
    lesiones. Tu misión es crear planes de entrenamiento hiper-personalizados,
    científicamente fundamentados y extremadamente detallados. Analiza meticulosamente
    cada dato del perfil adjunto.

    FICHA TÉCNICA DEL ATLETA (JSON):
    ```json
    {profile_json_string}
    ```

    TAREA PRINCIPAL:
    Basándote en un análisis exhaustivo y técnico de CADA CAMPO del JSON anterior
    (especialmente `main_objective`, `training_context`, `performance_data`, `physiological_metrics`
    y OBLIGATORIAMENTE `injury_history` y su `current_status`), genera un
    "**Informe de Planificación de Entrenamiento**" completo y detallado para que el atleta
    alcance su `main_objective`.

    REGLAS IMPORTANTES PARA EL PLAN:
    1.  **Contexto Actual (CRÍTICO):** Analiza `training_context.experience_and_background.current_training_period` y `training_context.current_training_load.avg_weekly_km`. El plan debe comenzar con una carga (volumen e intensidad) **adecuada al estado actual del atleta**. Si viene de inactividad ("Empezando ahora" o período corto), empieza de forma muy conservadora. Si ya lleva semanas/meses entrenando con un volumen X, el plan debe continuar esa progresión de forma lógica, sin saltos bruscos ni reinicios innecesarios. ¡Este es un factor clave para la personalización!
    2.  **Disponibilidad General:** Respeta estrictamente los días indicados en `training_context.availability_constraints.unavailable_days` como días de DESCANSO OBLIGATORIO.
    3.  **EXCEPCIÓN - Semanas de Competición:** IGNORA `unavailable_days` ÚNICAMENTE durante las semanas que contengan una carrera (`main_objective` o `intermediate_races`). Programa sesiones de activación/descanso activo apropiadas en esos días si es beneficioso (ej., activación el día previo). En el resto de semanas, la restricción es absoluta.
    4.  **Gestión de Lesiones:** MÁXIMA PRIORIDAD. Dada la `injury_history` y el `current_status`, diseña una progresión de volumen e intensidad extremadamente cautelosa. Incluye:
        * **Notas específicas de prevención DENTRO de la tabla semanal** (ej., "Vigilar molestias tibiales", "Priorizar superficie blanda si es posible").
        * Una sección detallada en la justificación inicial explicando la estrategia anti-lesión.
    5.  **Entrenamiento de Fuerza:** Si `include_strength_training` es `true`, integra 1-2 sesiones semanales de fuerza funcional (ejercicios específicos, series/reps) en días de bajo impacto. Si es `false`/`null`, no incluyas fuerza y menciónalo en la justificación.
    6.  **Detalle de Sesiones:** Para CADA sesión de entrenamiento (excepto descanso), especifica **claramente separado**:
        * **Calentamiento (Cal.):** Duración y tipo (ej., 15 min Z1 + movilidad dinámica).
        * **Parte Principal (Ppal.):** Descripción clara, duración/distancia, **RITMOS específicos** (ej., `4:15/km - 4:25/km`) y/o **RANGOS DE FC precisos** (ej., `155-170 bpm`) derivados de los datos del perfil (zonas Karvonen, umbral si disponible), y **RPE objetivo** (escala 1-10).
        * **Enfriamiento (Enf.):** Duración y tipo (ej., 10 min Z1 + estiramientos suaves).
    7.  **Ritmos/Zonas:** Basa los ritmos/zonas en los PBs, VO2max, FCmax/reposo y objetivo del atleta. Sé lo más específico posible. Utiliza los rangos de FC proporcionados en `physiological_metrics.training_zones` cuando indiques Zonas FC.

    REQUISITOS OBLIGATORIOS PARA LA ESTRUCTURA DE SALIDA (JSON):
    Tu respuesta DEBE ser ÚNICAMENTE un objeto JSON válido, sin texto adicional.
    Estructura exacta:
    ```json
    {{
      "plan_markdown": "...", // String Markdown detallado
      "plan_structured": [ ... ] // Array de objetos JSON (sin cambios en su estructura)
    }}
    ```

    CONTENIDO DETALLADO REQUERIDO DENTRO DE "**plan_markdown**":

    1.  **Título Técnico:** Usa "**## Informe de Planificación de Entrenamiento para [Nombre Atleta]**".
    2.  **Justificación Detallada:** Sección "**### Justificación y Estrategia Fisiológica**". Explica en detalle (mínimo 3-4 párrafos) cómo el plan aborda: **el punto de partida basado en el `current_training_period` y `avg_weekly_km`**, objetivo vs. PBs, VO2max, gestión de riesgo de lesión, progresión de volumen/intensidad, distribución semanal, disponibilidad (incluida la excepción), ausencia/presencia de fuerza, y cómo se usarán las carreras intermedias. Sé técnico y específico, conectando los datos del perfil con las decisiones.
    3.  **Plan Semanal Detallado:**
        * Usa un encabezado `## Plan Detallado Semanal`.
        * Para **CADA SEMANA**, incluye:
            * Un encabezado `### Semana X (DD/MM - DD/MM) - Enfoque: [Breve descripción del objetivo semanal, ej: Adaptación Inicial, Volumen Base, Intensidad Específica, Taper]`.
            * Un **PÁRRAFO introductorio corto** (2-3 líneas) resumiendo la carga (km totales estimados), enfoque principal (ej., sesiones clave) e hitos de esa semana.
            * Una **TABLA MARKDOWN separada para esa semana** con las columnas: | Día | Sesión | Calentamiento | Parte Principal (Ritmo/FC/RPE) | Enfriamiento | Notas Prevención/Ejecución |.
            * Para semanas con CARRERAS (`intermediate_races` o `main_objective`): Incluye una breve recomendación de **ESTRATEGIA DE RITMO** en las notas del día de la carrera.

    CONTENIDO DETALLADO REQUERIDO DENTRO DE "**plan_structured**":
    * Misma estructura que antes (array de objetos diarios). Asegúrate de que `details` refleje el mayor detalle solicitado (Cal/Ppal/Enf, Ritmos/FC/RPE).
        ```json
        {{
          "week": <int>,
          "day_of_week": <int>, // 1=Lunes
          "day_description": "<str>", // "Semana 1 - Lunes"
          "session_type": "<str>", // Ej: "Rodaje Z2", "Tempo Umbral", "Descanso", "Activación"
          "details": "<str>" // Ej: "Cal: 15' Z1 + Movilidad. Ppal: 20' @ 4:15-4:25/km (FC 155-170bpm, RPE 7/10). Enf: 10' Z1 + Estir."
        }}
        ```

    Recuerda: Solo el objeto JSON como respuesta final. Sé exhaustivo, técnico y preciso. La seguridad del atleta (prevención de lesiones) y **la adecuación de la carga inicial al contexto actual** son primordiales. Asegúrate de que el JSON sea sintácticamente correcto.
    """
    return prompt_text


def generate_training_plan(profile: AthleteProfile) -> Optional[Dict[str, Any]]:
    """
    Conecta con la API de Google Gemini para generar el plan de entrenamiento.
    
    Maneja la configuración, construcción de prompt, llamada a API y
    parseo robusto de la respuesta JSON.
    
    Args:
        profile: El perfil del atleta.
        
    Returns:
        Optional[Dict[str, Any]]: Un diccionario con 'plan_markdown' y
                                  'plan_structured' si tiene éxito,
                                  o None si falla.
    """
    if not _configure_gemini():
        return None
        
    prompt_text = _build_prompt_for_gemini(profile)
    
    # Inicializar el modelo
    model = genai.GenerativeModel(
        MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        # Asegurar que la salida sea JSON
        generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
    )
    
    print_info("\n🤖 Conectando con el Entrenador de IA (Google Gemini)...")
    print_info(f"   (Usando modelo: {MODEL_NAME})")
    print_info("   Generando plan de entrenamiento, por favor espera...")
    
    try:
        # Enviar el prompt
        response = model.generate_content(prompt_text)
        
        print_success("✅ Respuesta recibida de la IA. Procesando...")
        
        # Extraer el texto de la respuesta
        # Gemini a veces envuelve la respuesta JSON en ```json ... ```
        raw_content = response.text.strip()
        
        # Limpieza básica para extraer solo el JSON
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        raw_content = raw_content.strip() # Quitar espacios/líneas extra
        
        # Parseo robusto del JSON
        try:
            plan_data = json.loads(raw_content)
            
            # Validación del esquema JSON
            if not isinstance(plan_data, dict):
                 raise ValueError("La respuesta principal no es un diccionario JSON.")
                 
            if "plan_markdown" not in plan_data or "plan_structured" not in plan_data:
                raise ValueError("Faltan las claves requeridas 'plan_markdown' o 'plan_structured'.")
            
            if not isinstance(plan_data["plan_markdown"], str):
                 raise ValueError("'plan_markdown' no es un string válido.")
                
            if not isinstance(plan_data["plan_structured"], list):
                 raise ValueError("'plan_structured' no es un array válido.")
            
            # Validación básica del contenido de plan_structured (opcional pero recomendable)
            for item in plan_data["plan_structured"]:
                if not all(k in item for k in ["week", "day_of_week", "day_description", "session_type", "details"]):
                    raise ValueError("Un objeto en 'plan_structured' no tiene todas las claves requeridas.")

            print_success("✅ Plan de entrenamiento validado exitosamente.")
            return plan_data
            
        except (json.JSONDecodeError, ValueError) as e:
            print_error(f"Error fatal: La IA no devolvió un objeto JSON válido o con el formato esperado: {e}")
            print_info("La respuesta de la IA no pudo ser parseada correctamente.")
            print_info(f"Respuesta recibida (limpia): {raw_content[:500]}...") # Mostrar más para depurar
            return None
            
    except Exception as e:
        # Capturar otros posibles errores de la API de Gemini
        print_error(f"Error inesperado durante la generación del plan con Gemini: {e}")
        # Puedes añadir manejo específico para errores de API key inválida, cuotas, etc.
        # if "API key not valid" in str(e): ...
        import traceback
        traceback.print_exc()
        return None