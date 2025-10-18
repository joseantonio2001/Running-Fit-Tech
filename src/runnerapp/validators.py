"""
Validadores Personalizados para prompt-toolkit

Este módulo implementa validadores específicos para la CLI interactiva,
proporcionando validación en tiempo real de las entradas del usuario
usando las capacidades avanzadas de prompt-toolkit.

Cada validador hereda de prompt_toolkit.validation.Validator y implementa
la lógica específica para diferentes tipos de datos de la aplicación.
"""

import re
from datetime import datetime, date
from typing import Optional
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.document import Document

from .calculations import (
    parse_time_input, 
    validate_heart_rates, 
    validate_physical_metrics,
    validate_race_date
)


class AgeValidator(Validator):
    """Valida entrada de edad."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            age = int(text)
            if age < 10 or age > 100:
                raise ValidationError(
                    message='La edad debe estar entre 10 y 100 años',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número válido',
                cursor_position=len(text)
            )


class WeightValidator(Validator):
    """Valida entrada de peso."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            weight = float(text.replace(',', '.'))  # Permitir coma decimal
            if weight < 30 or weight > 200:
                raise ValidationError(
                    message='El peso debe estar entre 30 y 200 kg',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número válido (ej: 67.5)',
                cursor_position=len(text)
            )


class HeightValidator(Validator):
    """Valida entrada de altura."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            height = int(text)
            if height < 100 or height > 250:
                raise ValidationError(
                    message='La altura debe estar entre 100 y 250 cm',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número entero (ej: 180)',
                cursor_position=len(text)
            )


class HeartRateValidator(Validator):
    """Valida frecuencia cardíaca con rangos realistas."""
    
    def __init__(self, min_hr: int = 30, max_hr: int = 220, field_name: str = "FC"):
        self.min_hr = min_hr
        self.max_hr = max_hr
        self.field_name = field_name
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            hr = int(text)
            if hr < self.min_hr or hr > self.max_hr:
                raise ValidationError(
                    message=f'{self.field_name} debe estar entre {self.min_hr} y {self.max_hr} ppm',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número entero (ej: 184)',
                cursor_position=len(text)
            )


class VO2MaxValidator(Validator):
    """Valida entrada de VO2 máximo."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            vo2 = float(text.replace(',', '.'))
            if vo2 < 20 or vo2 > 90:
                raise ValidationError(
                    message='VO2máx debe estar entre 20 y 90 ml/kg/min',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número válido (ej: 60.5)',
                cursor_position=len(text)
            )


class WeeklyKmValidator(Validator):
    """Valida volumen semanal de entrenamiento."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            km = float(text.replace(',', '.'))
            if km < 0 or km > 300:
                raise ValidationError(
                    message='Volumen semanal debe estar entre 0 y 300 km',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número válido (ej: 50.0)',
                cursor_position=len(text)
            )


class TrainingDaysValidator(Validator):
    """Valida días de entrenamiento por semana."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        # Patrones válidos: "4", "4-5", "3-4"
        single_pattern = r'^\d+$'
        range_pattern = r'^\d+-\d+$'
        
        if re.match(single_pattern, text):
            days = int(text)
            if days < 1 or days > 7:
                raise ValidationError(
                    message='Días de entrenamiento debe estar entre 1 y 7',
                    cursor_position=len(text)
                )
        elif re.match(range_pattern, text):
            start, end = map(int, text.split('-'))
            if start < 1 or end > 7 or start > end:
                raise ValidationError(
                    message='Rango inválido. Use formato: 4-5 (entre 1 y 7)',
                    cursor_position=len(text)
                )
        else:
            raise ValidationError(
                message='Use formato: 4 o 4-5',
                cursor_position=len(text)
            )


class TimeValidator(Validator):
    """Valida tiempo deportivo en formato HH:MM:SS o HH:MM."""
    
    def __init__(self, allow_empty: bool = True):
        self.allow_empty = allow_empty
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text and self.allow_empty:
            return  # Campo vacío permitido
        
        if not text and not self.allow_empty:
            raise ValidationError(
                message='Este campo es obligatorio',
                cursor_position=0
            )
        
        # Intentar parsear el tiempo
        parsed_time = parse_time_input(text)
        if parsed_time is None:
            raise ValidationError(
                message='Formato inválido. Use: HH:MM o HH:MM:SS (ej: 18:30 o 1:25:30)',
                cursor_position=len(text)
            )


class DateValidator(Validator):
    """Valida fecha en formato YYYY-MM-DD."""
    
    def __init__(self, must_be_future: bool = True, allow_empty: bool = True):
        self.must_be_future = must_be_future
        self.allow_empty = allow_empty
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text and self.allow_empty:
            return  # Campo vacío permitido
        
        if not text and not self.allow_empty:
            raise ValidationError(
                message='Este campo es obligatorio',
                cursor_position=0
            )
        
        # Validar formato de fecha
        try:
            input_date = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                message='Formato inválido. Use: YYYY-MM-DD (ej: 2024-12-25)',
                cursor_position=len(text)
            )
        
        # Validar que sea futura si es requerido
        if self.must_be_future and input_date <= date.today():
            raise ValidationError(
                message='La fecha debe ser futura',
                cursor_position=len(text)
            )


class DistanceValidator(Validator):
    """Valida distancia de carrera."""
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            distance = float(text.replace(',', '.'))
            if distance <= 0 or distance > 200:
                raise ValidationError(
                    message='Distancia debe estar entre 0.1 y 200 km',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número válido (ej: 21.097)',
                cursor_position=len(text)
            )


class TerrainValidator(Validator):
    """Valida tipo de terreno de carrera."""
    
    VALID_TERRAINS = [
        'llano', 'montañoso', 'mixto', 'trail', 'pista', 
        'urbano', 'carretera', 'montaña'
    ]
    
    def validate(self, document: Document) -> None:
        text = document.text.strip().lower()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        if text not in self.VALID_TERRAINS:
            valid_options = ', '.join(self.VALID_TERRAINS)
            raise ValidationError(
                message=f'Tipo de terreno debe ser uno de: {valid_options}',
                cursor_position=len(document.text)
            )


class NonEmptyValidator(Validator):
    """Validador genérico para campos obligatorios no vacíos."""
    
    def __init__(self, message: str = "Este campo es obligatorio"):
        self.message = message
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            raise ValidationError(
                message=self.message,
                cursor_position=0
            )


class YesNoValidator(Validator):
    """Valida respuestas Sí/No con múltiples formatos aceptados."""
    
    YES_VALUES = ['sí', 'si', 's', 'yes', 'y', '1', 'true', 'verdadero']
    NO_VALUES = ['no', 'n', '0', 'false', 'falso']
    
    def validate(self, document: Document) -> None:
        text = document.text.strip().lower()
        
        if not text:
            return  # Campo vacío es válido (se interpretará como No)
        
        if text not in self.YES_VALUES and text not in self.NO_VALUES:
            raise ValidationError(
                message='Responda con: Sí/S/Yes o No/N',
                cursor_position=len(document.text)
            )


class OptionalIntegerValidator(Validator):
    """Validador para números enteros opcionales."""
    
    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None):
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        
        if not text:
            return  # Campo vacío es válido (opcional)
        
        try:
            value = int(text)
            
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(
                    message=f'El valor debe ser mayor o igual a {self.min_value}',
                    cursor_position=len(text)
                )
            
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(
                    message=f'El valor debe ser menor o igual a {self.max_value}',
                    cursor_position=len(text)
                )
                
        except ValueError:
            raise ValidationError(
                message='Por favor, ingrese un número entero válido',
                cursor_position=len(text)
            )


# Instancias pre-configuradas para uso común
age_validator = AgeValidator()
weight_validator = WeightValidator()
height_validator = HeightValidator()
max_hr_validator = HeartRateValidator(120, 220, "FCmáx")
resting_hr_validator = HeartRateValidator(30, 100, "FCrep")
vo2_max_validator = VO2MaxValidator()
weekly_km_validator = WeeklyKmValidator()
training_days_validator = TrainingDaysValidator()
time_validator = TimeValidator()
date_validator = DateValidator()
distance_validator = DistanceValidator()
terrain_validator = TerrainValidator()
yes_no_validator = YesNoValidator()
name_validator = NonEmptyValidator("El nombre es obligatorio")
