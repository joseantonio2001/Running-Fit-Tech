"""
Output Generation Module - ACTUALIZADO: Fase 5 (Generación de Plan)

✅ AÑADIDO: Funciones para generar plan en JSON, MD, y PDF profesional
- generate_plan_outputs(): Orquestador principal
- save_plan_json(): Guarda datos estructurados
- save_plan_markdown(): Guarda texto Markdown
- generar_plan_pdf(): Renderiza MD a PDF con WeasyPrint y CSS

✅ MANTENIDO: Generación de Ficha Técnica (PDF y JSON)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import traceback

# --- Dependencias Ficha Técnica (ReportLab) ---
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

from .models import AthleteProfile, TrainingZones
from .calculations import calculate_training_zones, calculate_bmi, format_distance_for_display
from .json_optimizer import optimize_profile_for_ai
from .cli_helpers import print_success, print_error, print_info, print_warning

# --- Configuración Ficha Técnica ---
DEFAULT_OUTPUTS_DIR = Path("outputs")
DEFAULT_PDF_FILENAME = "ficha_tecnica_profesional.pdf"
DEFAULT_JSON_FILENAME = "athlete_profile_ai_optimized.json"

# --- Configuración Plan de Entrenamiento ---
DEFAULT_PLAN_PDF_FILENAME = "plan_entrenamiento.pdf"
DEFAULT_PLAN_JSON_FILENAME = "plan_entrenamiento_structured.json"
DEFAULT_PLAN_MD_FILENAME = "plan_entrenamiento.md"

# Ruta al archivo CSS para el plan PDF
PLAN_CSS_PATH = Path(__file__).parent / "styles" / "plan_style.css"

# BALANCED MINIMALIST COLOR PALETTE
BACKGROUND_BLACK = colors.Color(0.04, 0.04, 0.04)  # Deep black #0A0A0A
BACKGROUND_DARK = colors.Color(0.10, 0.10, 0.10)   # Dark gray #1A1A1A
TEXT_WHITE = colors.Color(0.95, 0.95, 0.95)        # Soft white #F2F2F2
TEXT_LIGHT = colors.Color(0.70, 0.70, 0.70)        # Light gray #B3B3B3
TEXT_MEDIUM = colors.Color(0.58, 0.58, 0.58)       # Medium gray
ACCENT_CHROME = colors.Color(0.72, 0.72, 0.72)     # Chrome/metallic
ACCENT_BRIGHT = colors.Color(0.82, 0.82, 0.82)     # Subtle bright accent
BORDER_SUBTLE = colors.Color(0.25, 0.25, 0.25)     # Subtle border
HEADER_DARKER = colors.Color(0.45, 0.45, 0.45)     # Darker header gray
FOOTER_GRAY = colors.Color(0.40, 0.40, 0.40)       # Footer gray

# Balanced training zones colors
ZONE_COLORS_BALANCED = {
    'Z1': colors.Color(0.12, 0.18, 0.12),  # Subtle green
    'Z2': colors.Color(0.10, 0.16, 0.22),  # Subtle blue
    'Z3': colors.Color(0.22, 0.20, 0.08),  # Subtle yellow
    'Z4': colors.Color(0.24, 0.15, 0.08),  # Subtle orange
    'Z5': colors.Color(0.24, 0.10, 0.10),  # Subtle red
}

# Balanced minimalist table style
BALANCED_MINIMALIST_TABLE_STYLE = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_DARKER),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('BACKGROUND', (0, 1), (-1, -1), BACKGROUND_DARK),
    ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_LIGHT),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('LINEBELOW', (0, 0), (-1, 0), 1, BORDER_SUBTLE),
    ('LINEABOVE', (0, 1), (-1, -1), 0.3, BORDER_SUBTLE),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
])

# Balanced zones table style
def create_balanced_zones_style():
    base_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_DARKER),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_LIGHT),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 0), 1, BORDER_SUBTLE),
        ('LINEABOVE', (0, 1), (-1, -1), 0.3, BORDER_SUBTLE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]
    
    for i, zone in enumerate(['Z1', 'Z2', 'Z3', 'Z4', 'Z5']):
        if zone in ZONE_COLORS_BALANCED:
            base_style.append(('BACKGROUND', (0, i+1), (-1, i+1), ZONE_COLORS_BALANCED[zone]))
    return TableStyle(base_style)

BALANCED_ZONES_STYLE = create_balanced_zones_style()

# Create balanced minimalist styles
def create_balanced_minimalist_styles():
    styles = {}
    
    # Ultra-minimalist title
    styles['doc_title'] = ParagraphStyle(
        'DocumentTitle',
        fontName='Helvetica',
        fontSize=19,
        textColor=TEXT_WHITE,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=5
    )
    
    # Minimalist athlete name
    styles['athlete_name'] = ParagraphStyle(
        'AthleteName',
        fontName='Helvetica',
        fontSize=16,
        textColor=ACCENT_BRIGHT,
        alignment=TA_CENTER,
        spaceAfter=16,
        spaceBefore=0
    )
    
    # Ultra-minimal date
    styles['document_info'] = ParagraphStyle(
        'DocumentInfo',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_MEDIUM,
        alignment=TA_CENTER,
        spaceAfter=25
    )
    
    # Section titles with balanced spacing
    styles['section_title'] = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica',
        fontSize=12,
        textColor=TEXT_WHITE,
        alignment=TA_CENTER,
        spaceAfter=0,
        spaceBefore=15,
        borderWidth=0,
        borderPadding=8,
        backColor=BACKGROUND_DARK,
        leftIndent=0,
        rightIndent=0
    )
    
    # Ultra-minimal descriptions
    styles['section_description'] = ParagraphStyle(
        'SectionDescription',
        fontName='Helvetica',
        fontSize=9,
        textColor=TEXT_LIGHT,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        spaceBefore=8,
        leftIndent=15,
        rightIndent=15
    )
    
    # Subsection titles - balanced
    styles['subsection_title'] = ParagraphStyle(
        'SubsectionTitle',
        fontName='Helvetica',
        fontSize=11,
        textColor=ACCENT_CHROME,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=10,
        leftIndent=5
    )
    
    # Minimal normal text
    styles['normal'] = ParagraphStyle(
        'Normal',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_LIGHT,
        alignment=TA_LEFT,
        spaceAfter=5
    )
    
    # Data text with balanced spacing - MISMO ESTILO QUE VERSIÓN ANTERIOR
    styles['data_text'] = ParagraphStyle(
        'DataText',
        fontName='Helvetica',  # ✅ IGUAL QUE VERSIÓN ANTERIOR
        fontSize=10,
        textColor=TEXT_LIGHT,
        alignment=TA_LEFT,
        spaceAfter=3,
        spaceBefore=1,
        leftIndent=15,
        rightIndent=5
    )
    
    # Race details - balanced
    styles['race_detail'] = ParagraphStyle(
        'RaceDetail',
        fontName='Helvetica',
        fontSize=9,
        textColor=TEXT_LIGHT,
        alignment=TA_LEFT,
        spaceAfter=2,
        spaceBefore=1,
        leftIndent=25,
        rightIndent=5
    )
    
    return styles

PDF_STYLES = create_balanced_minimalist_styles()

# BALANCED SPACING CONSTANTS - Perfect distribution
BALANCED_TITLE_CONTENT_SPACING = 14
BALANCED_CONTENT_BLOCK_SPACING = 14
TABLE_TITLE_SPACING = 6

def generate_outputs(profile: AthleteProfile,
                    output_dir: Optional[str] = None,
                    pdf_filename: Optional[str] = None,
                    json_filename: Optional[str] = None) -> Tuple[bool, str, str]:
    """Generate both PDF and JSON outputs for an athlete profile."""
    if not output_dir:
        output_dir = DEFAULT_OUTPUTS_DIR
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    if profile.name:
        clean_name = "".join(c for c in profile.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_name = clean_name.replace(' ', '_').lower()
        
        if not pdf_filename:
            pdf_filename = f"ficha_tecnica_profesional_{clean_name}.pdf"
        if not json_filename:
            json_filename = f"athlete_profile_{clean_name}_ai.json"
    else:
        pdf_filename = pdf_filename or DEFAULT_PDF_FILENAME
        json_filename = json_filename or DEFAULT_JSON_FILENAME
    
    pdf_path = output_path / pdf_filename
    json_path = output_path / json_filename
    
    try:
        pdf_success = generate_minimalist_final_pdf_output(profile, str(pdf_path))
        if not pdf_success:
            return False, "", ""
        
        json_success = generate_json_output(profile, str(json_path))
        if not json_success:
            return False, "", ""
        
        return True, str(pdf_path), str(json_path)
    
    except Exception as e:
        print(f"Error generating outputs: {e}")
        return False, "", ""

def generate_plan_outputs(
    plan_markdown: str,
    plan_structured: List[Dict[str, Any]],
    profile_name: str,
    output_dir: Optional[str] = None
) -> Tuple[bool, List[str]]:
    """
    Orquesta la generación de todos los artefactos del plan de entrenamiento.
    Genera .json, .md, y .pdf del plan.
    
    Args:
        plan_markdown: String del plan en formato Markdown.
        plan_structured: Lista de objetos del plan estructurado.
        profile_name: Nombre del atleta para nombrar archivos.
        output_dir: Directorio de salida.
        
    Returns:
        Tuple[bool, List[str]]: (Éxito, Lista de rutas de archivos generados)
    """
    if not output_dir:
        output_dir = DEFAULT_OUTPUTS_DIR
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Limpiar nombre para archivos
    clean_name = "".join(c for c in profile_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_name = clean_name.replace(' ', '_').lower()
    
    base_filename = f"plan_{clean_name}"
    
    generated_files = []
    
    try:
        # 1. Guardar Plan JSON
        json_path = save_plan_json(plan_structured, output_path, base_filename)
        if json_path:
            generated_files.append(json_path)
            print_success(f"💾 Plan Estructurado JSON guardado: {json_path}")
        
        # 2. Guardar Plan Markdown
        md_path = save_plan_markdown(plan_markdown, output_path, base_filename)
        if md_path:
            generated_files.append(md_path)
            print_success(f"📝 Plan Markdown guardado: {md_path}")
            
        # 3. Generar Plan PDF
        pdf_path = generar_plan_pdf(plan_markdown, output_path, base_filename)
        if pdf_path:
            generated_files.append(pdf_path)
            print_success(f"📄 Plan Profesional PDF guardado: {pdf_path}")
            
        return True, generated_files
        
    except Exception as e:
        print_error(f"Error generando salidas del plan: {e}")
        import traceback
        traceback.print_exc()
        return False, []
    
def save_plan_json(plan_structured: List[Dict[str, Any]], output_path: Path, base_filename: str) -> Optional[str]:
    """Guarda los datos estructurados del plan en un archivo .json."""
    try:
        filepath = output_path / f"{base_filename}_structured.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(plan_structured, f, ensure_ascii=False, indent=4)
        return str(filepath)
    except Exception as e:
        print_error(f"Error guardando plan JSON: {e}")
        return None

def save_plan_markdown(plan_markdown: str, output_path: Path, base_filename: str) -> Optional[str]:
    """Guarda el string de markdown del plan en un archivo .md."""
    try:
        filepath = output_path / f"{base_filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(plan_markdown)
        return str(filepath)
    except Exception as e:
        print_error(f"Error guardando plan Markdown: {e}")
        return None

def generar_plan_pdf(plan_markdown: str, output_path: Path, base_filename: str) -> Optional[str]:
    """
    Convierte el Markdown del plan a HTML (asegurando soporte para tablas)
    y lo renderiza como un PDF profesional usando WeasyPrint y CSS.
    Ahora importa las dependencias Just-in-Time.
    """
    # --- MOVER IMPORTACIONES AQUÍ DENTRO ---
    try:
        from weasyprint import HTML, CSS
        from markdown_it import MarkdownIt
        from mdit_py_plugins.front_matter import front_matter_plugin
        from mdit_py_plugins.footnote import footnote_plugin
        from mdit_py_plugins.deflist import deflist_plugin
        # from mdit_py_plugins.table import table_plugin # Descomentar si es necesario
    except ImportError:
        print_warning("Generación de Plan PDF omitida (faltan dependencias WeasyPrint/MarkdownIt)")
        print_info("Instale con: pip install weasyprint markdown-it-py mdit-py-plugins")
        return None
    # -----------------------------------------

    try:
        filepath = output_path / f"{base_filename}.pdf"

        # 1. Convertir Markdown a HTML CON SOPORTE PARA TABLAS
        md = (
            MarkdownIt('gfm-like') # Activa tablas y otras extensiones
            # .enable('table')
            # .use(table_plugin) # Usar si es necesario
        )
        html_content = md.render(plan_markdown)

        # Añadir un wrapper HTML básico
        html_full = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Plan de Entrenamiento</title></head>
        <body>{html_content}</body>
        </html>
        """

        # 2. Cargar hoja de estilos CSS
        css_to_use = None
        if PLAN_CSS_PATH.exists():
            try:
                css_to_use = CSS(filename=str(PLAN_CSS_PATH))
                print_info(f"Usando estilos desde: {PLAN_CSS_PATH}")
            except Exception as css_err:
                print_error(f"Error cargando CSS desde {PLAN_CSS_PATH}: {css_err}")
                print_warning("Continuando sin estilos CSS personalizados.")
        else:
             print_warning(f"No se encontró CSS en {PLAN_CSS_PATH}. El PDF tendrá estilos por defecto.")

        # 3. Renderizar PDF
        print_info(f"Renderizando PDF en: {filepath}...")
        html_doc = HTML(string=html_full)
        html_doc.write_pdf(filepath, stylesheets=[css_to_use] if css_to_use else None)
        print_info("PDF renderizado.")

        return str(filepath)

    except Exception as e:
        print_error(f"Error generando plan PDF con WeasyPrint: {e}")
        traceback.print_exc() # Imprime el traceback completo
        return None

def generate_minimalist_final_pdf_output(profile: AthleteProfile, filepath: str) -> bool:
    """Generate final minimalist PDF with elegant name formatting."""
    try:
        if not profile.training_zones and profile.max_hr and profile.resting_hr:
            profile.training_zones = calculate_training_zones(profile.max_hr, profile.resting_hr)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=25*mm,
            rightMargin=25*mm,
            topMargin=40*mm,  # For clean header
            bottomMargin=25*mm  # Space for page number at bottom
        )
        
        story = []
        
        # ✅ Simplified main header with elegant name formatting
        story.extend(_build_simplified_main_header(profile))
        story.append(Spacer(1, 15))  # Reduced spacing
        
        # All sections with perfectly balanced spacing and ALL FIELDS ALWAYS SHOWN
        story.extend(_build_complete_personal_info_section(profile))
        story.append(Spacer(1, BALANCED_CONTENT_BLOCK_SPACING))
        
        story.extend(_build_complete_physiological_section(profile))
        story.append(Spacer(1, BALANCED_CONTENT_BLOCK_SPACING))
        
        # Training zones section with PAGE BREAK after table
        if profile.training_zones:
            story.extend(_build_balanced_training_zones_section(profile))
            story.append(PageBreak())  # SALTO DE PÁGINA después de zonas
        
        # Continue with remaining sections on new page
        story.extend(_build_complete_training_context_section_with_new_fields(profile))
        story.append(Spacer(1, BALANCED_CONTENT_BLOCK_SPACING))
        
        story.extend(_build_balanced_performance_section(profile))
        story.append(Spacer(1, BALANCED_CONTENT_BLOCK_SPACING))
        
        story.extend(_build_balanced_race_goals_section(profile))
        story.append(Spacer(1, BALANCED_CONTENT_BLOCK_SPACING))
        
        story.extend(_build_balanced_injury_history_section(profile))
        
        # ✅ NO LÍNEA FINAL (como en versión anterior)
        
        # ✅ Build with final minimalist template and correct page numbering
        doc.build(story,
                  onFirstPage=_add_final_minimalist_template,
                  onLaterPages=_add_final_minimalist_template)
        
        return True
    
    except Exception as e:
        print(f"Error generating minimalist final PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def _add_final_minimalist_template(canvas, doc):
    """✅ Add final minimalist page template with clean header and correct page number."""
    # Dark background
    canvas.saveState()
    canvas.setFillColor(BACKGROUND_BLACK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1)
    
    # ✅ FINAL MINIMALIST HEADER
    _draw_final_minimalist_header(canvas, doc)
    
    # ✅ CORRECT PAGE NUMBER POSITION
    _draw_correct_page_number(canvas, doc)
    
    canvas.restoreState()

def _draw_final_minimalist_header(canvas, doc):
    """✅ Draw final minimalist header: branding left, copyright right."""
    # Header positioning
    page_width = A4[0]
    page_height = A4[1]
    header_y = page_height - 20*mm
    
    # ✅ LEFT: Branding
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(ACCENT_CHROME)
    canvas.drawString(25*mm, header_y, "RUNNING FIT-TECH")
    
    # ✅ RIGHT: Copyright con año correcto
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TEXT_MEDIUM)
    generation_date = datetime.now()
    copyright_text = f"© {generation_date.year} PREMIUM"
    copyright_width = canvas.stringWidth(copyright_text, 'Helvetica', 8)
    canvas.drawString(page_width - 25*mm - copyright_width, header_y, copyright_text)
    
    # ✅ SUBTLE SEPARATOR LINE
    canvas.setStrokeColor(BORDER_SUBTLE)
    canvas.setLineWidth(0.5)
    canvas.line(25*mm, header_y - 4, page_width - 25*mm, header_y - 4)

def _draw_correct_page_number(canvas, doc):
    """✅ Draw page number at bottom center with correct orientation."""
    # Page positioning
    page_width = A4[0]
    page_num = canvas.getPageNumber()
    
    # ✅ CORRECT POSITION: Bottom center of page
    page_number_y = 15*mm  # At the bottom, above bottom margin
    
    # Draw page number with correct orientation (no rotation)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TEXT_MEDIUM)
    page_text = str(page_num)
    text_width = canvas.stringWidth(page_text, 'Helvetica', 8)
    
    # ✅ CENTER HORIZONTALLY at bottom of page
    canvas.drawString((page_width - text_width) / 2, page_number_y, page_text)

def _format_name_with_elegant_spacing(name: str) -> str:
    """✅ Format name with elegant spacing: letters separated by spaces, words by dots."""
    if not name:
        return ""
    
    # Split name into words
    words = name.strip().split()
    
    # Process each word: add spaces between letters
    formatted_words = []
    for word in words:
        # Convert to uppercase and add spaces between letters
        spaced_word = " ".join(word.upper())
        formatted_words.append(spaced_word)
    
    # Join words with centered dot separator
    return " · ".join(formatted_words)

def _build_simplified_main_header(profile: AthleteProfile) -> list:
    """Build simplified main header with elegant name formatting."""
    content = []
    
    # Ultra-minimal title
    title = Paragraph("FICHA TÉCNICA DEPORTIVA", PDF_STYLES['doc_title'])
    content.append(title)
    
    # ✅ Name with elegant letter spacing and word separation
    if profile.name:
        name_formatted = _format_name_with_elegant_spacing(profile.name)
        name = Paragraph(name_formatted, PDF_STYLES['athlete_name'])
        content.append(name)
    
    # ✅ Ultra-minimal date with dots con MES EN ESPAÑOL
    generation_date = datetime.now()
    months_spanish = {
        'January': 'ENERO', 'February': 'FEBRERO', 'March': 'MARZO',
        'April': 'ABRIL', 'May': 'MAYO', 'June': 'JUNIO',
        'July': 'JULIO', 'August': 'AGOSTO', 'September': 'SEPTIEMBRE',
        'October': 'OCTUBRE', 'November': 'NOVIEMBRE', 'December': 'DICIEMBRE'
    }
    
    month_english = generation_date.strftime('%B')
    month_spanish = months_spanish.get(month_english, month_english.upper())
    formatted_date = f"{generation_date.day} · {month_spanish} · {generation_date.year}"
    date = Paragraph(formatted_date, PDF_STYLES['document_info'])
    content.append(date)
    
    return content

def _build_complete_personal_info_section(profile: AthleteProfile) -> list:
    """Build personal information with ALL FIELDS ALWAYS SHOWN."""
    content = []
    
    section_title = Paragraph("INFORMACIÓN PERSONAL", PDF_STYLES['section_title'])
    content.append(section_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    
    # ✅ EDAD - Siempre mostrado con Helvetica-Bold para nombre del campo
    age_value = f"{profile.age} años" if profile.age else "No proporcionado"
    age_text = Paragraph(f"<b>EDAD</b> · {age_value}", PDF_STYLES['data_text'])
    content.append(age_text)
    
    # ✅ GÉNERO - Siempre mostrado con Helvetica-Bold para nombre del campo
    gender_value = profile.gender if profile.gender else "No proporcionado"
    gender_text = Paragraph(f"<b>GÉNERO</b> · {gender_value}", PDF_STYLES['data_text'])
    content.append(gender_text)
    
    # ✅ ALTURA - Siempre mostrado con Helvetica-Bold para nombre del campo
    height_value = f"{profile.height_cm} cm" if profile.height_cm else "No proporcionado"
    height_text = Paragraph(f"<b>ALTURA</b> · {height_value}", PDF_STYLES['data_text'])
    content.append(height_text)
    
    # ✅ PESO - Siempre mostrado con Helvetica-Bold para nombre del campo
    weight_value = f"{profile.weight_kg} kg" if profile.weight_kg else "No proporcionado"
    weight_text = Paragraph(f"<b>PESO</b> · {weight_value}", PDF_STYLES['data_text'])
    content.append(weight_text)
    
    # ✅ BMI - Siempre mostrado (campo separado) con Helvetica-Bold para nombre del campo
    if profile.weight_kg and profile.height_cm:
        bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
        bmi_value = f"{bmi:.1f}" if bmi else "No calculable"
    else:
        bmi_value = "No calculable"
    bmi_text = Paragraph(f"<b>BMI</b> · {bmi_value}", PDF_STYLES['data_text'])
    content.append(bmi_text)
    
    return content

def _build_complete_physiological_section(profile: AthleteProfile) -> list:
    """Build physiological metrics with ALL FIELDS ALWAYS SHOWN."""
    content = []
    
    section_title = Paragraph("MÉTRICAS FISIOLÓGICAS", PDF_STYLES['section_title'])
    content.append(section_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    
    # ✅ RECUPERADA: Descripción fisiológica original
    description = Paragraph(
        "Parámetros fisiológicos que definen el perfil de resistencia cardiovascular y el potencial de rendimiento aeróbico del atleta.",
        PDF_STYLES['section_description']
    )
    content.append(description)
    
    # ✅ FC MÁXIMA - Siempre mostrado con Helvetica-Bold para nombre del campo
    max_hr_value = f"{profile.max_hr} bpm" if profile.max_hr else "No proporcionado"
    hr_max_text = Paragraph(f"<b>FC MÁXIMA</b> · {max_hr_value}", PDF_STYLES['data_text'])
    content.append(hr_max_text)
    
    # ✅ FC REPOSO - Siempre mostrado con Helvetica-Bold para nombre del campo
    rest_hr_value = f"{profile.resting_hr} bpm" if profile.resting_hr else "No proporcionado"
    hr_rest_text = Paragraph(f"<b>FC REPOSO</b> · {rest_hr_value}", PDF_STYLES['data_text'])
    content.append(hr_rest_text)
    
    # ✅ VO2 MÁXIMO - Siempre mostrado con Helvetica-Bold para nombre del campo
    vo2_value = f"{profile.vo2_max} ml/kg/min" if profile.vo2_max else "No proporcionado"
    vo2_text = Paragraph(f"<b>VO2 MÁXIMO</b> · {vo2_value}", PDF_STYLES['data_text'])
    content.append(vo2_text)
    
    # ✅ UMBRAL LACTATO - Siempre mostrado (CORREGIDO: lactate_threshold_bpm)
    lactate_value = f"{profile.lactate_threshold_bpm} bpm" if profile.lactate_threshold_bpm else "No proporcionado"
    lactate_text = Paragraph(f"<b>UMBRAL LACTATO</b> · {lactate_value}", PDF_STYLES['data_text'])
    content.append(lactate_text)
    
    # ✅ VFC (HRV) - Siempre mostrado con Helvetica-Bold para nombre del campo
    hrv_value = f"{profile.hrv_ms} ms" if profile.hrv_ms else "No proporcionado"
    hrv_text = Paragraph(f"<b>VFC (HRV)</b> · {hrv_value}", PDF_STYLES['data_text'])
    content.append(hrv_text)
    
    return content

def _build_complete_training_context_section_with_new_fields(profile: AthleteProfile) -> list:
    """
    ✅ Build training context CON NUEVOS CAMPOS TÉCNICOS - SIN "INCLUIR FUERZA".
    
    Mantiene EXACTAMENTE la misma estética de la versión anterior,
    añadiendo los 3 nuevos campos y eliminando "INCLUIR FUERZA" del PDF.
    """
    content = []
    
    section_title = Paragraph("CONTEXTO DE ENTRENAMIENTO", PDF_STYLES['section_title'])
    content.append(section_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    
    # ✅ NUEVO CAMPO 2: PERÍODO ACTUAL
    period_value = profile.current_training_period if profile.current_training_period else "No proporcionado"
    period_text = Paragraph(f"<b>PERÍODO ACTUAL</b> · {period_value}", PDF_STYLES['data_text'])
    content.append(period_text)

    # ✅ VOLUMEN SEMANAL - Siempre mostrado con Helvetica-Bold para nombre del campo
    volume_value = f"{profile.avg_weekly_km} km/semana" if profile.avg_weekly_km else "No proporcionado"
    volume_text = Paragraph(f"<b>VOLUMEN SEMANAL</b> · {volume_value}", PDF_STYLES['data_text'])
    content.append(volume_text)
    
    # ✅ DÍAS ENTRENAMIENTO - Siempre mostrado con Helvetica-Bold para nombre del campo
    days_value = f"{profile.training_days_per_week} días/semana" if profile.training_days_per_week else "No proporcionado"
    days_text = Paragraph(f"<b>DÍAS ENTRENAMIENTO</b> · {days_value}", PDF_STYLES['data_text'])
    content.append(days_text)
    
    # ✅ NUEVO CAMPO 1: EXPERIENCIA DEPORTIVA
    experience_value = f"{profile.running_experience_years} años" if profile.running_experience_years else "No proporcionado"
    experience_text = Paragraph(f"<b>EXPERIENCIA DEPORTIVA</b> · {experience_value}", PDF_STYLES['data_text'])
    content.append(experience_text)
    
    # ✅ HISTORIAL FUERZA - Siempre mostrado con Helvetica-Bold para nombre del campo
    if profile.strength_training_history is not None:
        history_value = "SÍ" if profile.strength_training_history else "NO"
    else:
        history_value = "No proporcionado"
    strength_text = Paragraph(f"<b>HISTORIAL FUERZA</b> · {history_value}", PDF_STYLES['data_text'])
    content.append(strength_text)
    
    # ✅ ELIMINADO: "INCLUIR FUERZA" del PDF (como solicitado)
    # Solo se mantiene en el JSON para la IA
    
    return content

def _build_balanced_training_zones_section(profile: AthleteProfile) -> list:
    """Build training zones with balanced spacing (Page break will be added after this)."""
    content = []
    
    zones_title = Paragraph("ZONAS DE ENTRENAMIENTO · KARVONEN", PDF_STYLES['section_title'])
    content.append(zones_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    content.append(Spacer(1, TABLE_TITLE_SPACING))
    
    zones_data = [['ZONA', 'DESCRIPCIÓN', 'RANGO FC', 'PROPÓSITO']]
    
    zones_info = [
        ('Z1', 'Recuperación Activa', getattr(profile.training_zones, 'zone1_hr', 'N/A'), 'Regeneración y base aeróbica'),
        ('Z2', 'Aeróbico Base', getattr(profile.training_zones, 'zone2_hr', 'N/A'), 'Resistencia fundamental'),
        ('Z3', 'Aeróbico Tempo', getattr(profile.training_zones, 'zone3_hr', 'N/A'), 'Desarrollo aeróbico'),
        ('Z4', 'Umbral Anaeróbico', getattr(profile.training_zones, 'zone4_hr', 'N/A'), 'Potencia aeróbica máxima'),
        ('Z5', 'Capacidad Máxima', getattr(profile.training_zones, 'zone5_hr', 'N/A'), 'VO2máx y velocidad')
    ]
    
    for zone_name, zone_desc, hr_range, purpose in zones_info:
        if hr_range and hr_range != 'N/A':
            zones_data.append([zone_name, zone_desc, hr_range, purpose])
    
    if len(zones_data) > 1:
        zones_table = Table(zones_data, colWidths=[20*mm, 38*mm, 32*mm, 80*mm])
        zones_table.setStyle(BALANCED_ZONES_STYLE)
        content.append(zones_table)
    
    return content

def _build_balanced_performance_section(profile: AthleteProfile) -> list:
    """Build performance data with balanced spacing."""
    content = []
    
    section_title = Paragraph("RENDIMIENTO COMPETITIVO", PDF_STYLES['section_title'])
    content.append(section_title)
    
    if profile.personal_bests:
        content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
        content.append(Spacer(1, TABLE_TITLE_SPACING))
        
        data = [['DISTANCIA', 'MARCA PERSONAL', 'RITMO MEDIO']]
        
        distance_names = {
            '5k': '5K',
            '10k': '10K',
            'half_marathon': 'MEDIA MARATÓN',
            'marathon': 'MARATÓN'
        }
        
        distance_km = {
            '5k': 5.0,
            '10k': 10.0,
            'half_marathon': 21.097,
            'marathon': 42.195
        }
        
        for key, name in distance_names.items():
            if profile.personal_bests.get(key):
                time = profile.personal_bests[key]
                pace = _calculate_pace(time, distance_km[key])
                data.append([name, time, pace])
        
        if len(data) > 1:
            table = Table(data, colWidths=[52*mm, 38*mm, 35*mm])
            table.setStyle(BALANCED_MINIMALIST_TABLE_STYLE)
            content.append(table)
    
    return content

def _build_balanced_race_goals_section(profile: AthleteProfile) -> list:
    """Build race goals with balanced spacing."""
    content = []
    
    section_title = Paragraph("OBJETIVOS COMPETITIVOS", PDF_STYLES['section_title'])
    content.append(section_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    
    if profile.main_objective:
        objective_title = Paragraph("OBJETIVO PRINCIPAL", PDF_STYLES['subsection_title'])
        content.append(objective_title)
        
        race_info = f"<b>CARRERA</b> · {profile.main_objective.name.upper()}"
        race_para = Paragraph(race_info, PDF_STYLES['data_text'])
        content.append(race_para)
        
        date_info = f"<b>FECHA</b> · {profile.main_objective.date}"
        date_para = Paragraph(date_info, PDF_STYLES['data_text'])
        content.append(date_para)
        
        distance_info = f"<b>DISTANCIA</b> · {format_distance_for_display(profile.main_objective.distance_km)}"
        distance_para = Paragraph(distance_info, PDF_STYLES['data_text'])
        content.append(distance_para)
        
        terrain_info = f"<b>TERRENO</b> · {profile.main_objective.terrain.upper()}"
        terrain_para = Paragraph(terrain_info, PDF_STYLES['data_text'])
        content.append(terrain_para)
        
        if profile.main_objective.goal_time:
            time_info = f"<b>TIEMPO OBJETIVO</b> · {profile.main_objective.goal_time}"
            time_para = Paragraph(time_info, PDF_STYLES['data_text'])
            content.append(time_para)
    
    if profile.intermediate_races:
        content.append(Spacer(1, 12))
        intermediate_title = Paragraph("CARRERAS PREPARATORIAS", PDF_STYLES['subsection_title'])
        content.append(intermediate_title)
        
        for i, race in enumerate(profile.intermediate_races, 1):
            race_header = f"{i} · {(race.name or f'CARRERA PREPARATORIA {i}').upper()}"
            header_para = Paragraph(race_header, PDF_STYLES['data_text'])
            content.append(header_para)
            
            if race.date:
                date_detail = f"Fecha · {race.date}"
                date_para = Paragraph(date_detail, PDF_STYLES['race_detail'])
                content.append(date_para)
            
            if race.distance_km:
                distance_detail = f"Distancia · {format_distance_for_display(race.distance_km)}"
                distance_para = Paragraph(distance_detail, PDF_STYLES['race_detail'])
                content.append(distance_para)
            
            goal_detail = f"Objetivo · {race.goal_time or 'Preparación específica'}"
            goal_para = Paragraph(goal_detail, PDF_STYLES['race_detail'])
            content.append(goal_para)
            
            terrain_detail = f"Terreno · {(race.terrain or 'Estándar').upper()}"
            terrain_para = Paragraph(terrain_detail, PDF_STYLES['race_detail'])
            content.append(terrain_para)
            
            if i < len(profile.intermediate_races):
                content.append(Spacer(1, 6))
    
    return content

def _build_balanced_injury_history_section(profile: AthleteProfile) -> list:
    """Build injury history with balanced spacing."""
    content = []
    
    section_title = Paragraph("HISTORIAL MÉDICO", PDF_STYLES['section_title'])
    content.append(section_title)
    content.append(Spacer(1, BALANCED_TITLE_CONTENT_SPACING))
    
    if profile.injuries:
        for i, injury in enumerate(profile.injuries):
            injury_text = f"LESIÓN · {(injury.type or 'NO ESPECIFICADA').upper()}"
            injury_para = Paragraph(injury_text, PDF_STYLES['data_text'])
            content.append(injury_para)
            
            date_text = f"FECHA · {injury.date_approx or 'Sin fecha registrada'}"
            date_para = Paragraph(date_text, PDF_STYLES['data_text'])
            content.append(date_para)
            
            recovery_text = f"RECUPERACIÓN · {injury.recovery_desc or 'Sin información detallada'}"
            recovery_para = Paragraph(recovery_text, PDF_STYLES['data_text'])
            content.append(recovery_para)
            
            # ✅ NUEVO CAMPO - Estado actual
            status_text = f"ESTADO ACTUAL · {(injury.current_status or 'No especificado').upper()}"
            status_para = Paragraph(status_text, PDF_STYLES['data_text'])
            content.append(status_para)
            
            if i < len(profile.injuries) - 1:
                content.append(Spacer(1, 8))
    else:
        no_injuries = Paragraph(
            "SIN LESIONES REGISTRADAS · PERFIL DE BAJO RIESGO",
            PDF_STYLES['normal']
        )
        content.append(no_injuries)
    
    return content

def _calculate_pace(time_str: str, distance_km: float) -> str:
    """Calculate pace from time and distance."""
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        else:
            return "N/A"
        
        pace_seconds = total_seconds / distance_km
        pace_minutes = int(pace_seconds // 60)
        pace_seconds = int(pace_seconds % 60)
        
        return f"{pace_minutes:02d}:{pace_seconds:02d}/km"
    except:
        return "N/A"

def generate_json_output(profile: AthleteProfile, filepath: str) -> bool:
    """Generate AI-optimized JSON output."""
    try:
        ai_optimized_data = optimize_profile_for_ai(profile)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(ai_optimized_data, f, ensure_ascii=False, indent=4, sort_keys=False)
        
        return True
    
    except Exception as e:
        print(f"Error generating JSON: {e}")
        return False

def validate_profile_completeness(profile: AthleteProfile) -> Tuple[bool, list]:
    """Validate profile completeness."""
    missing_fields = []
    
    if not profile.name:
        missing_fields.append("Nombre del atleta")
    
    if not profile.age:
        missing_fields.append("Edad")
    
    if not profile.gender:
        missing_fields.append("Género")
    
    has_physiological = bool(profile.max_hr and profile.resting_hr)
    has_performance = bool(profile.personal_bests and any(profile.personal_bests.values()))
    has_objectives = bool(profile.main_objective)
    
    if not (has_physiological or has_performance or has_objectives):
        missing_fields.append("Al menos una sección significativa")
    
    return len(missing_fields) == 0, missing_fields

def main():
    """Test function for final minimalist output generation with elegant name formatting."""
    from .persistence import load_profile
    from .cli_helpers import print_success, print_error, print_info
    
    try:
        profile = load_profile()
        
        if not profile.name:
            print_error("No se encontró un perfil válido")
            sys.exit(1)
        
        is_valid, missing_fields = validate_profile_completeness(profile)
        
        if not is_valid:
            print_error("El perfil no está completo:")
            for field in missing_fields:
                print_error(f"  - {field}")
            print_info("Completar el perfil antes de generar outputs")
            sys.exit(1)
        
        print_info(f"Generando FICHA TÉCNICA FINAL CON NUEVOS CAMPOS para: {profile.name}")
        success, pdf_path, json_path = generate_outputs(profile)
        
        if success:
            print_success(f"🏆 PDF FINAL generado: {pdf_path}")
            print_success(f"✅ JSON generado: {json_path}")
            print_info("\n✨ NUEVOS CAMPOS AÑADIDOS:")
            print_info("  📊 EXPERIENCIA DEPORTIVA: En PDF y JSON")
            print_info("  ⏱️  PERÍODO ACTUAL: En PDF y JSON")  
            print_info("  🏆 NIVEL COMPETITIVO: En PDF y JSON")
            print_info("  🚫 INCLUIR FUERZA: Solo en JSON (eliminado del PDF)")
        else:
            print_error("❌ Error al generar las salidas")
    
    except Exception as e:
        print_error(f"Error: {e}")

if __name__ == "__main__":
    main()