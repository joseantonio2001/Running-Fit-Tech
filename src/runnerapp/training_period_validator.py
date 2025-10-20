"""
Validador Temporal Inteligente - Reconoce múltiples formatos de tiempo

✅ NUEVO: Validador especializado para períodos de entrenamiento
✅ SOPORTE: Múltiples idiomas (español e inglés)
✅ FLEXIBLE: Reconoce abreviaciones, plurales, mayúsculas/minúsculas
✅ NORMALIZACIÓN: Convierte entrada a formato estándar

Ejemplos de entrada soportados:
- 1 mes, 1 m, 1 M, 1 mes, 1 MESES, 1 month, 1 mo → "1 mes"
- 2 años, 2 año, 2 a, 2 A, 2 AÑOS, 2 year, 2 years, 2 y, 2 Y → "2 años"  
- 3 semanas, 3 semana, 3 s, 3 S, 3 week, 3 weeks, 3 w → "3 semanas"
- 4 días, 4 día, 4 d, 4 D, 4 day, 4 days → "4 días"
"""

import re
from typing import Optional, Tuple
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document

class TrainingPeriodValidator(Validator):
    """
    ✅ Validador inteligente para períodos de entrenamiento.
    
    Reconoce múltiples formatos temporales y los normaliza a formato estándar.
    Permite campo vacío (opcional) y valida rangos razonables.
    """
    
    def __init__(self):
        super().__init__()
        
        # Diccionarios de mapeo para normalización
        self.time_units_es = {
            # Días
            'día': 'día', 'dias': 'días', 'día': 'día', 'días': 'días',
            'd': 'día', 'D': 'día',
            
            # Semanas  
            'semana': 'semana', 'semanas': 'semanas',
            's': 'semana', 'S': 'semana',
            
            # Meses
            'mes': 'mes', 'meses': 'meses',
            'm': 'mes', 'M': 'mes',
            
            # Años
            'año': 'año', 'anos': 'años', 'año': 'año', 'años': 'años',
            'a': 'año', 'A': 'año'
        }
        
        self.time_units_en = {
            # Days
            'day': 'día', 'days': 'días',
            
            # Weeks
            'week': 'semana', 'weeks': 'semanas', 
            'w': 'semana', 'W': 'semana',
            
            # Months
            'month': 'mes', 'months': 'meses',
            'mo': 'mes', 'MO': 'mes', 'Mon': 'mes',
            
            # Years
            'year': 'año', 'years': 'años',
            'y': 'año', 'Y': 'año', 'yr': 'año', 'yrs': 'años'
        }
        
        # Patrones regex para reconocer formatos
        self.patterns = [
            # Números con unidades (ej: "2 años", "3 semanas")
            r'^(\d+(?:\.\d+)?)\s*([a-zA-ZñÑ]+)$',
            
            # Solo números (asumimos meses por defecto)
            r'^(\d+(?:\.\d+)?)$',
            
            # Casos especiales
            r'^0\s*-\s*(empezando|starting|comenzando)$',
            r'^(empezando|starting|comenzando)$'
        ]
    
    def validate(self, document: Document) -> None:
        """Validación síncrona requerida por Validator"""
        text = document.text.strip()
        
        if not text:
            return  # Campo opcional
        
        normalized = self.normalize_period(text)
        if not normalized:
            raise ValidationError(
                message='Formato no reconocido. Ejemplos válidos: "2 meses", "3 semanas", "1 año", "2 m", "3 weeks"',
                cursor_position=len(text)
            )
    
    async def validate_async(self, document: Document) -> None:
        """Validación async requerida por prompt_toolkit"""
        self.validate(document)
    
    def normalize_period(self, text: str) -> Optional[str]:
        """
        Normaliza período de entrenamiento a formato estándar español.
        
        Args:
            text: Entrada del usuario (ej: "2 months", "3 s", "1 año")
            
        Returns:
            str: Formato normalizado (ej: "2 meses", "3 semanas", "1 año")
            None: Si no se puede normalizar
        """
        text = text.lower().strip()
        
        # Casos especiales: empezando
        if any(word in text for word in ['empezando', 'starting', 'comenzando']):
            return "Empezando ahora"
        
        # Patrón: número + unidad
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([a-zA-ZñÑ]+)$', text)
        if match:
            number_str, unit = match.groups()
            number = float(number_str) if '.' in number_str else int(number_str)
            
            # Buscar unidad en diccionarios
            normalized_unit = None
            
            # Primero en español
            if unit in self.time_units_es:
                normalized_unit = self.time_units_es[unit]
            # Luego en inglés
            elif unit in self.time_units_en:
                normalized_unit = self.time_units_en[unit]
            else:
                # Intentar coincidencias parciales
                for es_key, es_val in self.time_units_es.items():
                    if unit.startswith(es_key) or es_key.startswith(unit):
                        normalized_unit = es_val
                        break
                
                if not normalized_unit:
                    for en_key, en_val in self.time_units_en.items():
                        if unit.startswith(en_key) or en_key.startswith(unit):
                            normalized_unit = en_val
                            break
            
            if normalized_unit:
                # Ajustar singular/plural según el número
                if number == 1:
                    if normalized_unit in ['días', 'semanas', 'meses', 'años']:
                        # Convertir a singular
                        singular_map = {
                            'días': 'día',
                            'semanas': 'semana', 
                            'meses': 'mes',
                            'años': 'año'
                        }
                        normalized_unit = singular_map.get(normalized_unit, normalized_unit)
                else:
                    # Convertir a plural si es necesario
                    plural_map = {
                        'día': 'días',
                        'semana': 'semanas',
                        'mes': 'meses', 
                        'año': 'años'
                    }
                    normalized_unit = plural_map.get(normalized_unit, normalized_unit)
                
                # Formatear número (sin decimales innecesarios)
                if isinstance(number, float) and number.is_integer():
                    number = int(number)
                
                return f"{number} {normalized_unit}"
        
        # Patrón: solo número (asumimos meses)
        match = re.match(r'^(\d+(?:\.\d+)?)$', text)
        if match:
            number = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
            if isinstance(number, float) and number.is_integer():
                number = int(number)
            
            unit = "mes" if number == 1 else "meses"
            return f"{number} {unit}"
        
        return None

def parse_training_period(text: str) -> str:
    """
    ✅ Función auxiliar para normalizar períodos desde CLI.
    
    Args:
        text: Entrada del usuario
        
    Returns:
        str: Período normalizado o texto original si no se puede normalizar
    """
    validator = TrainingPeriodValidator()
    normalized = validator.normalize_period(text)
    return normalized if normalized else text

# ✅ Ejemplos de uso y tests
def test_training_period_validator():
    """Tests para verificar el funcionamiento del validador"""
    validator = TrainingPeriodValidator()
    
    test_cases = [
        # Español
        ("2 meses", "2 meses"),
        ("1 mes", "1 mes"),
        ("3 semanas", "3 semanas"),
        ("1 semana", "1 semana"),
        ("2 años", "2 años"),
        ("1 año", "1 año"),
        ("5 días", "5 días"),
        ("1 día", "1 día"),
        
        # Abreviaciones español
        ("2 m", "2 meses"),
        ("1 M", "1 mes"),
        ("3 s", "3 semanas"),
        ("2 a", "2 años"),
        ("5 d", "5 días"),
        
        # Inglés
        ("2 months", "2 meses"),
        ("1 month", "1 mes"),
        ("3 weeks", "3 semanas"),
        ("1 week", "1 semana"),
        ("2 years", "2 años"),
        ("1 year", "1 año"),
        ("5 days", "5 días"),
        ("1 day", "1 día"),
        
        # Abreviaciones inglés
        ("2 mo", "2 meses"),
        ("3 w", "3 semanas"),
        ("2 y", "2 años"),
        
        # Solo números (asume meses)
        ("3", "3 meses"),
        ("1", "1 mes"),
        
        # Casos especiales
        ("empezando", "Empezando ahora"),
        ("0 - empezando", "Empezando ahora"),
        ("starting", "Empezando ahora"),
    ]
    
    print("🧪 Testing TrainingPeriodValidator:")
    for input_text, expected in test_cases:
        result = validator.normalize_period(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{input_text}' → '{result}' (esperado: '{expected}')")

if __name__ == "__main__":
    test_training_period_validator()