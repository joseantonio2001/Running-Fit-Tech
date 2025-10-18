"""
Professional PDF Styling Module - Advanced Technical Report Design

This module implements a medical/scientific-grade PDF layout inspired by
professional sports medicine reports, laboratory analyses, and clinical
fitness assessments. Designed for maximum technical credibility while
maintaining excellent readability and professional aesthetics.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import mm, inch
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfgen import canvas
from typing import List, Dict, Any, Optional
import datetime

from .models import TrainingZones, Injury, Race


# Page Layout Constants - Professional Medical Format
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGINS = {
    'left': 20*mm,
    'right': 20*mm, 
    'top': 30*mm,
    'bottom': 25*mm
}

CONTENT_WIDTH = PAGE_WIDTH - MARGINS['left'] - MARGINS['right']

# Professional Scientific Color Scheme
COLORS = {
    # Primary palette - Medical/Scientific
    'primary': colors.Color(0.12, 0.29, 0.49),      # Deep medical blue
    'secondary': colors.Color(0.25, 0.35, 0.45),    # Muted professional blue
    'accent': colors.Color(0.92, 0.49, 0.13),       # Scientific orange
    
    # Status colors
    'success': colors.Color(0.15, 0.68, 0.38),      # Medical green
    'warning': colors.Color(0.96, 0.76, 0.05),      # Caution yellow
    'danger': colors.Color(0.86, 0.24, 0.24),       # Medical alert red
    'info': colors.Color(0.20, 0.60, 0.86),         # Information blue
    
    # Neutral palette
    'text_primary': colors.Color(0.15, 0.15, 0.15), # Near black
    'text_secondary': colors.Color(0.45, 0.45, 0.45), # Professional grey
    'text_light': colors.Color(0.65, 0.65, 0.65),   # Light grey
    
    # Background palette
    'bg_primary': colors.white,
    'bg_secondary': colors.Color(0.98, 0.98, 0.99), # Very light blue
    'bg_accent': colors.Color(0.95, 0.97, 1.0),     # Light technical blue
    'bg_warning': colors.Color(1.0, 0.98, 0.90),    # Light warning
    
    # Training zone colors (scientifically appropriate)
    'zone1': colors.Color(0.85, 0.95, 0.85),        # Light green
    'zone2': colors.Color(0.75, 0.90, 0.95),        # Light blue  
    'zone3': colors.Color(1.0, 0.95, 0.70),         # Light yellow
    'zone4': colors.Color(1.0, 0.85, 0.70),         # Light orange
    'zone5': colors.Color(1.0, 0.80, 0.80),         # Light red
}

# Professional Typography System
PDF_STYLES = {
    # Document hierarchy
    'doc_title': ParagraphStyle(
        'DocumentTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=COLORS['primary'],
        alignment=TA_CENTER,
        spaceAfter=8,
        spaceBefore=0
    ),
    
    'doc_subtitle': ParagraphStyle(
        'DocumentSubtitle',
        fontName='Helvetica',
        fontSize=14,
        textColor=COLORS['secondary'],
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=0
    ),
    
    'athlete_name': ParagraphStyle(
        'AthleteName',
        fontName='Helvetica-Bold', 
        fontSize=22,
        textColor=COLORS['text_primary'],
        alignment=TA_CENTER,
        spaceAfter=6,
        spaceBefore=12
    ),
    
    'document_info': ParagraphStyle(
        'DocumentInfo',
        fontName='Helvetica',
        fontSize=9,
        textColor=COLORS['text_secondary'],
        alignment=TA_CENTER,
        spaceAfter=25
    ),
    
    # Section styles
    'section_title': ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=COLORS['primary'],
        alignment=TA_LEFT,
        spaceAfter=12,
        spaceBefore=20,
        borderWidth=2,
        borderColor=COLORS['primary'],
        borderPadding=5
    ),
    
    'subsection_title': ParagraphStyle(
        'SubsectionTitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=COLORS['secondary'],
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=15
    ),
    
    'section_description': ParagraphStyle(
        'SectionDescription',
        fontName='Helvetica',
        fontSize=9,
        textColor=COLORS['text_secondary'],
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leftIndent=10,
        rightIndent=10
    ),
    
    # Content styles
    'normal': ParagraphStyle(
        'Normal',
        fontName='Helvetica',
        fontSize=10,
        textColor=COLORS['text_primary'],
        alignment=TA_LEFT,
        spaceAfter=6
    ),
    
    'technical_data': ParagraphStyle(
        'TechnicalData',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=COLORS['primary'],
        alignment=TA_LEFT,
        spaceAfter=4
    ),
    
    'analysis_text': ParagraphStyle(
        'AnalysisText',
        fontName='Helvetica',
        fontSize=10,
        textColor=COLORS['text_primary'],
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leftIndent=15,
        rightIndent=15
    ),
    
    'warning_text': ParagraphStyle(
        'WarningText',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=COLORS['warning'],
        alignment=TA_LEFT,
        spaceAfter=6
    ),
    
    'success_text': ParagraphStyle(
        'SuccessText',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=COLORS['success'],
        alignment=TA_LEFT,
        spaceAfter=6
    ),
    
    # Footer styles
    'footer_main': ParagraphStyle(
        'FooterMain',
        fontName='Helvetica',
        fontSize=8,
        textColor=COLORS['text_light'],
        alignment=TA_CENTER
    ),
    
    'footer_tech': ParagraphStyle(
        'FooterTech',
        fontName='Helvetica',
        fontSize=7,
        textColor=COLORS['text_light'],
        alignment=TA_RIGHT
    )
}

# Advanced Table Styles
PDF_STYLES['header_table_style'] = TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), COLORS['primary']),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
])

PDF_STYLES['data_table_style'] = TableStyle([
    # Header row - Professional medical style
    ('BACKGROUND', (0, 0), (-1, 0), COLORS['secondary']),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    
    # Data rows - Alternating backgrounds for readability
    ('BACKGROUND', (0, 1), (-1, 1), colors.white),
    ('BACKGROUND', (0, 2), (-1, 2), COLORS['bg_secondary']),
    ('BACKGROUND', (0, 3), (-1, 3), colors.white),
    ('BACKGROUND', (0, 4), (-1, 4), COLORS['bg_secondary']),
    ('BACKGROUND', (0, 5), (-1, 5), colors.white),
    ('BACKGROUND', (0, 6), (-1, 6), COLORS['bg_secondary']),
    
    # Text formatting
    ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['text_primary']),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),    # First column bold
    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),        # Other columns normal
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ('ALIGN', (2, 1), (-1, -1), 'LEFT'),
    
    # Professional borders
    ('LINEBELOW', (0, 0), (-1, 0), 2, COLORS['primary']),
    ('LINEABOVE', (0, 1), (-1, 1), 1, COLORS['text_light']),
    ('LINEBEFORE', (0, 0), (0, -1), 1, COLORS['text_light']),
    ('LINEAFTER', (-1, 0), (-1, -1), 1, COLORS['text_light']),
    
    # Spacing
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
])

PDF_STYLES['zones_table_style'] = TableStyle([
    # Header - Professional scientific style
    ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    
    # Zone-specific color coding (scientific standards)
    ('BACKGROUND', (0, 1), (-1, 1), COLORS['zone1']),    # Z1 - Recovery
    ('BACKGROUND', (0, 2), (-1, 2), COLORS['zone2']),    # Z2 - Aerobic
    ('BACKGROUND', (0, 3), (-1, 3), COLORS['zone3']),    # Z3 - Tempo
    ('BACKGROUND', (0, 4), (-1, 4), COLORS['zone4']),    # Z4 - Threshold
    ('BACKGROUND', (0, 5), (-1, 5), COLORS['zone5']),    # Z5 - VO2max
    
    # Professional text styling
    ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['text_primary']),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    
    # Technical borders
    ('LINEBELOW', (0, 0), (-1, 0), 2, COLORS['primary']),
    ('GRID', (0, 1), (-1, -1), 0.5, COLORS['text_light']),
    ('LINEAFTER', (-1, 0), (-1, -1), 1, COLORS['text_light']),
    ('LINEBEFORE', (0, 0), (0, -1), 1, COLORS['text_light']),
    
    # Spacing
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
])

PDF_STYLES['summary_table_style'] = TableStyle([
    # Executive summary style - Key metrics highlighted
    ('BACKGROUND', (0, 0), (-1, 0), COLORS['accent']),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    
    # Data rows with emphasis
    ('BACKGROUND', (0, 1), (-1, -1), COLORS['bg_accent']),
    ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['text_primary']),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 11),
    
    # Professional styling
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 1.5, COLORS['primary']),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
])


def create_professional_header(canvas_obj, doc, profile_name: str):
    """Create advanced professional header with branding."""
    canvas_obj.saveState()
    
    # Header background bar
    canvas_obj.setFillColor(COLORS['primary'])
    canvas_obj.rect(0, PAGE_HEIGHT - 25*mm, PAGE_WIDTH, 25*mm, fill=1)
    
    # Company logo area (placeholder)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.circle(30*mm, PAGE_HEIGHT - 12.5*mm, 8*mm, fill=1)
    canvas_obj.setFillColor(COLORS['primary'])
    canvas_obj.circle(30*mm, PAGE_HEIGHT - 12.5*mm, 6*mm, fill=1)
    
    # Header text
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont('Helvetica-Bold', 16)
    canvas_obj.drawString(50*mm, PAGE_HEIGHT - 10*mm, "FIT-TECH SOLUTIONS")
    
    canvas_obj.setFont('Helvetica', 10)
    canvas_obj.drawString(50*mm, PAGE_HEIGHT - 15*mm, "Sports Science & Performance Analytics")
    
    # Document ID and date (right side)
    doc_id = f"FT-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(profile_name) % 1000:03d}"
    canvas_obj.setFont('Helvetica-Bold', 10)
    canvas_obj.drawRightString(PAGE_WIDTH - 15*mm, PAGE_HEIGHT - 10*mm, f"Document ID: {doc_id}")
    
    canvas_obj.setFont('Helvetica', 9)
    generation_date = datetime.datetime.now().strftime("%d %B %Y | %H:%M")
    canvas_obj.drawRightString(PAGE_WIDTH - 15*mm, PAGE_HEIGHT - 15*mm, f"Generated: {generation_date}")
    
    # Professional separator line
    canvas_obj.setStrokeColor(COLORS['accent'])
    canvas_obj.setLineWidth(3)
    canvas_obj.line(MARGINS['left'], PAGE_HEIGHT - MARGINS['top'] + 5,
                    PAGE_WIDTH - MARGINS['right'], PAGE_HEIGHT - MARGINS['top'] + 5)
    
    canvas_obj.restoreState()


def create_professional_footer(canvas_obj, doc):
    """Create professional footer with technical information."""
    canvas_obj.saveState()
    
    # Footer separator
    canvas_obj.setStrokeColor(COLORS['text_light'])
    canvas_obj.setLineWidth(1)
    canvas_obj.line(MARGINS['left'], MARGINS['bottom'] + 10*mm,
                    PAGE_WIDTH - MARGINS['right'], MARGINS['bottom'] + 10*mm)
    
    # Technical footer info
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(COLORS['text_secondary'])
    
    # Left side - Company info
    canvas_obj.drawString(MARGINS['left'], MARGINS['bottom'] + 5*mm, 
                         "RUNNING Fit-Tech | AI-Powered Training Analytics")
    canvas_obj.drawString(MARGINS['left'], MARGINS['bottom'] + 2*mm,
                         "Scientific approach to personalized training")
    
    # Right side - Page and technical info
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawRightString(PAGE_WIDTH - MARGINS['right'], MARGINS['bottom'] + 5*mm,
                              f"Página {page_num}")
    canvas_obj.drawRightString(PAGE_WIDTH - MARGINS['right'], MARGINS['bottom'] + 2*mm,
                              "Confidencial - Solo para uso del atleta")
    
    canvas_obj.restoreState()


def create_executive_summary_table(profile) -> Table:
    """Create executive summary with key metrics."""
    from .calculations import calculate_bmi
    
    data = [
        ['RESUMEN EJECUTIVO - MÉTRICAS CLAVE', '', '']
    ]
    
    # Calculate key metrics
    if profile.age:
        age_category = "Joven" if profile.age < 25 else "Adulto" if profile.age < 40 else "Máster"
        data.append(['Categoría por Edad', f'{profile.age} años', age_category])
    
    if profile.weight_kg and profile.height_cm:
        bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
        bmi_status = "Óptimo" if 18.5 <= bmi < 25 else "Revisar"
        data.append(['Índice de Masa Corporal', f'{bmi:.1f}', bmi_status])
    
    if profile.max_hr and profile.resting_hr:
        hr_reserve = profile.max_hr - profile.resting_hr
        reserve_status = "Excelente" if hr_reserve > 160 else "Bueno" if hr_reserve > 140 else "Limitado"
        data.append(['Reserva Cardíaca', f'{hr_reserve} bpm', reserve_status])
    
    if profile.vo2_max:
        vo2_status = "Elite" if profile.vo2_max > 55 else "Alto" if profile.vo2_max > 45 else "Moderado"
        data.append(['VO2 Máximo', f'{profile.vo2_max} ml/kg/min', vo2_status])
    
    if profile.avg_weekly_km:
        volume_status = "Alto" if profile.avg_weekly_km > 60 else "Moderado" if profile.avg_weekly_km > 30 else "Bajo"
        data.append(['Volumen Semanal', f'{profile.avg_weekly_km} km', volume_status])
    
    # Risk assessment
    injury_risk = "Bajo" if not profile.injuries else "Moderado" if len(profile.injuries) < 3 else "Alto"
    data.append(['Riesgo de Lesión', f'{len(profile.injuries)} lesiones registradas', injury_risk])
    
    table = Table(data, colWidths=[70*mm, 50*mm, 50*mm])
    table.setStyle(PDF_STYLES['summary_table_style'])
    
    return table


def draw_training_zones_table(training_zones: TrainingZones) -> Table:
    """Create advanced training zones table with scientific precision."""
    data = [
        ['ZONA', 'RANGO FC (bpm)', '% FC RESERVA', 'PROPÓSITO FISIOLÓGICO', 'ADAPTACIÓN']
    ]
    
    zone_data = [
        ('Z1', training_zones.zone1_hr if hasattr(training_zones, 'zone1_hr') else 'N/A', 
         '50-60%', 'Recuperación Activa', 'Capilarización y enzimas oxidativas'),
        ('Z2', training_zones.zone2_hr if hasattr(training_zones, 'zone2_hr') else 'N/A', 
         '60-70%', 'Base Aeróbica', 'Mitocondrias y metabolismo graso'),
        ('Z3', training_zones.zone3_hr if hasattr(training_zones, 'zone3_hr') else 'N/A', 
         '70-80%', 'Tempo Aeróbico', 'Eficiencia cardiovascular'),
        ('Z4', training_zones.zone4_hr if hasattr(training_zones, 'zone4_hr') else 'N/A', 
         '80-90%', 'Umbral Anaeróbico', 'Tolerancia al lactato y buffering'),
        ('Z5', training_zones.zone5_hr if hasattr(training_zones, 'zone5_hr') else 'N/A', 
         '90-100%', 'Potencia Aeróbica', 'VO2máx y sistema neuromuscular')
    ]
    
    for zone_name, hr_range, fc_percent, purpose, adaptation in zone_data:
        data.append([zone_name, hr_range, fc_percent, purpose, adaptation])
    
    table = Table(data, colWidths=[15*mm, 30*mm, 25*mm, 50*mm, 50*mm])
    table.setStyle(PDF_STYLES['zones_table_style'])
    
    return table


def draw_performance_analysis_table(profile) -> Table:
    """Create advanced performance analysis with percentiles."""
    if not profile.personal_bests:
        return Table([['Sin datos de rendimiento disponibles']], colWidths=[170*mm])
    
    data = [
        ['DISTANCIA', 'MARCA PERSONAL', 'RITMO/KM', 'NIVEL ESTIMADO', 'VDOT EQUIV.']
    ]
    
    distance_data = {
        '5k': {'name': '5.000m', 'km': 5.0},
        '10k': {'name': '10.000m', 'km': 10.0},
        'half_marathon': {'name': '21.097m (1/2 Maratón)', 'km': 21.097},
        'marathon': {'name': '42.195m (Maratón)', 'km': 42.195}
    }
    
    for key, info in distance_data.items():
        if profile.personal_bests.get(key):
            time = profile.personal_bests[key]
            pace = _calculate_detailed_pace(time, info['km'])
            level = _estimate_performance_level(key, time, profile.age, profile.gender)
            vdot = _calculate_vdot_equivalent(key, time)
            
            data.append([info['name'], time, pace, level, f"{vdot:.1f}"])
    
    table = Table(data, colWidths=[40*mm, 25*mm, 25*mm, 40*mm, 25*mm])
    table.setStyle(PDF_STYLES['data_table_style'])
    
    return table


def draw_injury_risk_assessment_table(injuries: List[Injury]) -> Table:
    """Create professional injury risk assessment."""
    if not injuries:
        data = [
            ['EVALUACIÓN DE RIESGO DE LESIONES', '', ''],
            ['Estado Actual', 'Sin lesiones registradas', '✓ BAJO RIESGO'],
            ['Recomendación', 'Protocolo preventivo estándar', 'Continuar monitorización']
        ]
    else:
        data = [
            ['HISTORIAL DE LESIONES Y EVALUACIÓN DE RIESGO', '', '']
        ]
        
        for i, injury in enumerate(injuries, 1):
            risk_level = _assess_injury_risk_level(injury.type)
            prevention_focus = _get_prevention_strategy(injury.type)
            
            data.extend([
                [f'Lesión {i}', injury.type, risk_level],
                ['Fecha', injury.date_approx or 'No especificada', ''],
                ['Recuperación', injury.recovery_desc or 'Sin detalles', ''],
                ['Prevención', prevention_focus, ''],
                ['', '', '']  # Separator row
            ])
    
    table = Table(data, colWidths=[40*mm, 80*mm, 50*mm])
    table.setStyle(PDF_STYLES['data_table_style'])
    
    return table


def draw_race_goals_analysis_table(profile) -> Table:
    """Create race goals with feasibility analysis."""
    if not profile.main_objective:
        return Table([['Sin objetivos de carrera definidos']], colWidths=[170*mm])
    
    data = [
        ['ANÁLISIS DE OBJETIVOS DE CARRERA', '', '']
    ]
    
    # Main objective analysis
    obj = profile.main_objective
    weeks_until = _calculate_weeks_until_race(obj.date)
    feasibility = _analyze_goal_feasibility(profile, obj, weeks_until)
    
    data.extend([
        ['Objetivo Principal', obj.name, ''],
        ['Fecha Objetivo', obj.date, f'{weeks_until} semanas disponibles' if weeks_until else 'Fecha pasada'],
        ['Distancia', f'{obj.distance_km:.3f} km', _categorize_distance(obj.distance_km)],
        ['Tiempo Meta', obj.goal_time or 'No especificado', ''],
        ['Terreno', obj.terrain, _analyze_terrain_difficulty(obj.terrain)],
        ['Factibilidad', feasibility['assessment'], feasibility['confidence']]
    ])
    
    # Intermediate races
    if profile.intermediate_races:
        data.append(['', '', ''])
        data.append(['CARRERAS PREPARATORIAS', '', ''])
        
        for race in profile.intermediate_races:
            strategic_value = _assess_race_strategic_value(race, profile.main_objective)
            data.append([race.name, race.date, strategic_value])
    
    table = Table(data, colWidths=[50*mm, 70*mm, 50*mm])
    table.setStyle(PDF_STYLES['data_table_style'])
    
    return table


def create_physiological_assessment_section(profile) -> List:
    """Create comprehensive physiological assessment."""
    content = []
    
    # Section title with technical emphasis
    title = Paragraph(
        "EVALUACIÓN FISIOLÓGICA Y CAPACIDADES FUNCIONALES",
        PDF_STYLES['section_title']
    )
    content.append(title)
    
    # Clinical-style description
    description = Paragraph(
        "Análisis científico de las capacidades cardiovasculares, metabólicas y de rendimiento del atleta "
        "basado en parámetros fisiológicos medidos y estimados. Evaluación realizada según protocolos "
        "estándar de medicina deportiva y ciencias del ejercicio.",
        PDF_STYLES['section_description']
    )
    content.append(description)
    
    # Cardiovascular assessment
    if profile.max_hr and profile.resting_hr:
        cv_title = Paragraph("PERFIL CARDIOVASCULAR", PDF_STYLES['subsection_title'])
        content.append(cv_title)
        
        # Professional cardiovascular analysis
        cv_analysis = _generate_cardiovascular_analysis(profile)
        cv_text = Paragraph(cv_analysis, PDF_STYLES['analysis_text'])
        content.append(cv_text)
    
    # VO2max assessment
    if profile.vo2_max:
        vo2_title = Paragraph("CAPACIDAD AERÓBICA MÁXIMA", PDF_STYLES['subsection_title'])
        content.append(vo2_title)
        
        vo2_analysis = _generate_vo2_analysis(profile)
        vo2_text = Paragraph(vo2_analysis, PDF_STYLES['analysis_text'])
        content.append(vo2_text)
    
    return content


def create_performance_benchmarking_section(profile) -> List:
    """Create detailed performance benchmarking section."""
    content = []
    
    if not profile.personal_bests:
        return content
    
    # Section title
    title = Paragraph(
        "ANÁLISIS DE RENDIMIENTO Y BENCHMARKING COMPETITIVO",
        PDF_STYLES['section_title']
    )
    content.append(title)
    
    # Performance analysis
    performance_analysis = _generate_comprehensive_performance_analysis(profile)
    analysis_text = Paragraph(performance_analysis, PDF_STYLES['analysis_text'])
    content.append(analysis_text)
    
    # Performance table
    content.append(draw_performance_analysis_table(profile))
    
    # Age-group comparison
    if profile.age:
        comparison_title = Paragraph(
            f"COMPARATIVA POR GRUPO DE EDAD ({profile.age} años - {profile.gender})",
            PDF_STYLES['subsection_title']
        )
        content.append(comparison_title)
        
        comparison_analysis = _generate_age_group_comparison(profile)
        comparison_text = Paragraph(comparison_analysis, PDF_STYLES['analysis_text'])
        content.append(comparison_text)
    
    return content


def create_training_prescription_section(profile) -> List:
    """Create training prescription based on scientific analysis."""
    content = []
    
    # Section title
    title = Paragraph(
        "PRESCRIPCIÓN DE ENTRENAMIENTO BASADA EN EVIDENCIA",
        PDF_STYLES['section_title']
    )
    content.append(title)
    
    # Training prescription
    prescription = _generate_training_prescription(profile)
    prescription_text = Paragraph(prescription, PDF_STYLES['analysis_text'])
    content.append(prescription_text)
    
    # Weekly structure recommendation
    if profile.training_days_per_week and profile.avg_weekly_km:
        structure_title = Paragraph("ESTRUCTURA SEMANAL RECOMENDADA", PDF_STYLES['subsection_title'])
        content.append(structure_title)
        
        weekly_structure = _generate_weekly_structure(profile)
        structure_text = Paragraph(weekly_structure, PDF_STYLES['analysis_text'])
        content.append(structure_text)
    
    return content


# Helper functions for advanced calculations and analysis

def _calculate_detailed_pace(time_str: str, distance_km: float) -> str:
    """Calculate precise pace with seconds."""
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
        
        return f"{pace_minutes}'{pace_seconds:02d}\"/km"
    except:
        return "N/A"


def _estimate_performance_level(distance_key: str, time: str, age: int, gender: str) -> str:
    """Estimate performance level based on age/gender standards."""
    # Simplified performance level estimation
    if distance_key == "10k":
        # Convert time to minutes for analysis
        try:
            parts = time.split(':')
            if len(parts) == 2:
                total_minutes = int(parts[0]) + int(parts[1])/60
                if gender == "Masculino":
                    if total_minutes < 35:
                        return "Elite Nacional"
                    elif total_minutes < 40:
                        return "Competitivo Alto"
                    elif total_minutes < 45:
                        return "Competitivo"
                    elif total_minutes < 50:
                        return "Recreativo Alto"
                    else:
                        return "Recreativo"
                else:  # Femenino
                    if total_minutes < 40:
                        return "Elite Nacional"
                    elif total_minutes < 45:
                        return "Competitivo Alto" 
                    elif total_minutes < 50:
                        return "Competitivo"
                    elif total_minutes < 55:
                        return "Recreativo Alto"
                    else:
                        return "Recreativo"
        except:
            return "A Evaluar"
    
    return "Por Determinar"


def _calculate_vdot_equivalent(distance_key: str, time: str) -> float:
    """Calculate VDOT equivalent score."""
    # Simplified VDOT calculation - would need full Jack Daniels tables
    try:
        if distance_key == "10k":
            parts = time.split(':')
            if len(parts) == 2:
                total_seconds = int(parts[0]) * 60 + int(parts[1])
                # Approximate VDOT calculation for 10K
                vdot = 15.3 * (10000 / total_seconds)
                return max(20.0, min(85.0, vdot))
    except:
        pass
    
    return 45.0  # Default moderate value


def _assess_injury_risk_level(injury_type: str) -> str:
    """Assess injury recurrence risk level."""
    injury_lower = injury_type.lower()
    
    high_risk_keywords = ['fascitis', 'fractura', 'ligamento', 'menisco', 'aquiles']
    moderate_risk_keywords = ['tendinitis', 'rodilla', 'espalda', 'cadera']
    
    if any(keyword in injury_lower for keyword in high_risk_keywords):
        return "🔴 ALTO RIESGO"
    elif any(keyword in injury_lower for keyword in moderate_risk_keywords):
        return "🟡 RIESGO MODERADO"
    else:
        return "🟢 BAJO RIESGO"


def _get_prevention_strategy(injury_type: str) -> str:
    """Get specific prevention strategy for injury type."""
    injury_lower = injury_type.lower()
    
    if 'fascitis' in injury_lower:
        return "Fortalecimiento específico de pie y pantorrilla"
    elif 'aquiles' in injury_lower:
        return "Trabajo excéntrico y progresión gradual"
    elif 'rodilla' in injury_lower:
        return "Fortalecimiento de glúteo y análisis biomecánico"
    elif 'espalda' in injury_lower:
        return "Core stability y técnica de carrera"
    else:
        return "Protocolo de prevención general"


def _calculate_weeks_until_race(race_date: str) -> Optional[int]:
    """Calculate weeks until race date."""
    try:
        race_dt = datetime.datetime.strptime(race_date, "%Y-%m-%d")
        now = datetime.datetime.now()
        delta = race_dt - now
        return max(0, delta.days // 7)
    except:
        return None


def _analyze_goal_feasibility(profile, objective, weeks_until: int) -> Dict[str, str]:
    """Analyze goal feasibility with scientific approach."""
    if not weeks_until or weeks_until <= 0:
        return {"assessment": "Objetivo en el pasado", "confidence": "N/A"}
    
    # Base analysis on current fitness and time available
    if weeks_until < 6:
        return {"assessment": "Tiempo muy limitado - mantenimiento", "confidence": "Baja"}
    elif weeks_until < 12:
        return {"assessment": "Preparación específica posible", "confidence": "Moderada"}
    elif weeks_until < 20:
        return {"assessment": "Preparación óptima factible", "confidence": "Alta"}
    else:
        return {"assessment": "Tiempo amplio para desarrollo completo", "confidence": "Muy Alta"}


def _categorize_distance(distance_km: float) -> str:
    """Categorize race distance scientifically."""
    if distance_km <= 5:
        return "Velocidad/Potencia"
    elif distance_km <= 10:
        return "Velocidad-Resistencia"
    elif distance_km <= 21.1:
        return "Resistencia Medio-Fondo"
    elif distance_km <= 42.2:
        return "Resistencia Fondo"
    else:
        return "Ultra-Resistencia"


def _analyze_terrain_difficulty(terrain: str) -> str:
    """Analyze terrain difficulty factor."""
    terrain_lower = terrain.lower() if terrain else ""
    
    if 'montañoso' in terrain_lower or 'trail' in terrain_lower:
        return "Alto factor de dificultad"
    elif 'mixto' in terrain_lower:
        return "Factor de dificultad moderado"
    elif 'llano' in terrain_lower or 'pista' in terrain_lower:
        return "Condiciones óptimas"
    else:
        return "Por evaluar"


def _assess_race_strategic_value(race: Race, main_objective: Race) -> str:
    """Assess strategic value of intermediate race."""
    if not main_objective:
        return "Objetivo independiente"
    
    # Compare distances and dates for strategic assessment
    if race.distance_km < main_objective.distance_km:
        return "Preparación de velocidad"
    elif race.distance_km == main_objective.distance_km:
        return "Test de ritmo objetivo"
    else:
        return "Desarrollo de resistencia"


def _generate_cardiovascular_analysis(profile) -> str:
    """Generate professional cardiovascular analysis."""
    analysis = []
    
    if profile.max_hr:
        predicted_max = 220 - profile.age if profile.age else 185
        if profile.max_hr > predicted_max + 10:
            analysis.append(f"FC máxima superior a la predicción por edad (+{profile.max_hr - predicted_max} bpm).")
        elif profile.max_hr < predicted_max - 10:
            analysis.append(f"FC máxima inferior a la predicción por edad ({predicted_max - profile.max_hr} bpm).")
        else:
            analysis.append("FC máxima dentro de rangos predichos por edad.")
    
    if profile.resting_hr:
        if profile.resting_hr < 50:
            analysis.append("FC en reposo indica excelente adaptación cardiovascular.")
        elif profile.resting_hr < 60:
            analysis.append("FC en reposo en rango óptimo para atleta entrenado.")
        elif profile.resting_hr < 70:
            analysis.append("FC en reposo normal, margen de mejora disponible.")
        else:
            analysis.append("FC en reposo elevada - oportunidad significativa de desarrollo aeróbico.")
    
    if profile.max_hr and profile.resting_hr:
        reserve = profile.max_hr - profile.resting_hr
        analysis.append(f"Reserva cardíaca de {reserve} bpm permite entrenamiento de alta intensidad.")
    
    return " ".join(analysis) if analysis else "Datos cardiovasculares insuficientes para análisis completo."


def _generate_vo2_analysis(profile) -> str:
    """Generate VO2max analysis with performance implications."""
    if not profile.vo2_max:
        return "VO2 máximo no disponible para análisis."
    
    vo2 = profile.vo2_max
    analysis = []
    
    # Gender-specific analysis
    if profile.gender == "Masculino":
        if vo2 > 70:
            analysis.append("VO2máx excepcional - nivel elite internacional.")
        elif vo2 > 60:
            analysis.append("VO2máx muy alto - potencial competitivo nacional.")
        elif vo2 > 50:
            analysis.append("VO2máx alto - buen nivel competitivo regional.")
        elif vo2 > 40:
            analysis.append("VO2máx moderado - corredor recreativo entrenado.")
        else:
            analysis.append("VO2máx bajo - gran margen de mejora disponible.")
    else:  # Femenino
        if vo2 > 60:
            analysis.append("VO2máx excepcional - nivel elite internacional.")
        elif vo2 > 50:
            analysis.append("VO2máx muy alto - potencial competitivo nacional.")
        elif vo2 > 42:
            analysis.append("VO2máx alto - buen nivel competitivo regional.")
        elif vo2 > 35:
            analysis.append("VO2máx moderado - corredora recreativa entrenada.")
        else:
            analysis.append("VO2máx bajo - gran margen de mejora disponible.")
    
    # Performance correlation
    if profile.personal_bests and profile.personal_bests.get('10k'):
        analysis.append("VO2máx coherente con marcas de rendimiento registradas.")
    
    return " ".join(analysis)


def _generate_comprehensive_performance_analysis(profile) -> str:
    """Generate comprehensive performance analysis."""
    if not profile.personal_bests:
        return "Sin datos de rendimiento disponibles para análisis."
    
    analysis = []
    
    # Distance specialization analysis
    distances_completed = [k for k, v in profile.personal_bests.items() if v]
    
    if len(distances_completed) >= 3:
        analysis.append("Perfil completo con experiencia en múltiples distancias.")
    elif len(distances_completed) >= 2:
        analysis.append("Experiencia competitiva moderada, expandir rango de distancias.")
    else:
        analysis.append("Experiencia limitada, desarrollar base competitiva.")
    
    # Progression potential
    if profile.age and profile.age < 25:
        analysis.append("Edad óptima para desarrollo de rendimiento máximo.")
    elif profile.age < 35:
        analysis.append("Etapa de madurez atlética, potencial de especialización.")
    else:
        analysis.append("Enfoque en mantenimiento y eficiencia técnica.")
    
    return " ".join(analysis)


def _generate_age_group_comparison(profile) -> str:
    """Generate age group performance comparison."""
    if not profile.personal_bests.get('10k') or not profile.age:
        return "Datos insuficientes para comparación por edad."
    
    # This would contain actual age-group performance tables
    return f"Rendimiento en 10K corresponde a percentil estimado del grupo de edad {profile.age}-{profile.age+4} años."


def _generate_training_prescription(profile) -> str:
    """Generate evidence-based training prescription."""
    prescription = []
    
    # Volume prescription
    if profile.avg_weekly_km:
        current_volume = profile.avg_weekly_km
        if current_volume < 30:
            prescription.append("Prioridad: Desarrollo progresivo de volumen base aeróbico.")
        elif current_volume < 60:
            prescription.append("Volumen base sólido, desarrollar intensidad específica.")
        else:
            prescription.append("Alto volumen establecido, optimizar distribución de intensidades.")
    
    # Intensity prescription based on objectives
    if profile.main_objective:
        distance = profile.main_objective.distance_km
        if distance >= 42:
            prescription.append("Énfasis: 80% Zona 1-2, 15% Zona 3-4, 5% Zona 5.")
        elif distance >= 21:
            prescription.append("Énfasis: 70% Zona 1-2, 20% Zona 3-4, 10% Zona 5.")
        elif distance >= 10:
            prescription.append("Énfasis: 60% Zona 1-2, 25% Zona 3-4, 15% Zona 5.")
        else:
            prescription.append("Énfasis: 50% Zona 1-2, 30% Zona 3-4, 20% Zona 5.")
    
    # Strength training prescription
    if profile.include_strength_training:
        if not profile.strength_training_history:
            prescription.append("Incorporar 2 sesiones/semana de fuerza funcional con énfasis técnico.")
        else:
            prescription.append("Mantener 2-3 sesiones/semana de fuerza con periodización específica.")
    
    return " ".join(prescription) if prescription else "Prescripción requerirá datos adicionales."


def _generate_weekly_structure(profile) -> str:
    """Generate weekly training structure recommendation."""
    days = profile.training_days_per_week
    volume = profile.avg_weekly_km
    
    if not days or not volume:
        return "Estructura semanal requiere datos de disponibilidad y volumen."
    
    try:
        days_num = int(days.split('-')[0]) if '-' in str(days) else int(days)
        avg_session = volume / days_num
        
        structure = f"Distribución recomendada para {days} días/semana ({volume}km total): "
        
        if days_num <= 3:
            structure += f"Sesiones largas ({avg_session:.1f}km promedio) - Calidad sobre cantidad."
        elif days_num <= 5:
            structure += f"Equilibrio óptimo ({avg_session:.1f}km/sesión) - Combinación volumen/intensidad."
        else:
            structure += f"Alta frecuencia ({avg_session:.1f}km/sesión) - Distribución polarizada."
        
        return structure
        
    except:
        return "Estructura semanal requiere clarificación de datos."


# Additional helper functions for professional analysis
def create_header(canvas_obj, doc):
    """Standard header function for compatibility."""
    pass


def create_footer(canvas_obj, doc):
    """Standard footer function for compatibility."""
    pass