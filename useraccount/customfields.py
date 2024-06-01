from typing import Any
from django.db import models
from django.core.exceptions import ValidationError

# C0FFEE -> 12648430
def hex_to_int(value):
    if value is None:
        return None
    return int(value, 16)

# 12648430 -> C0FFEE
def int_to_hex(value):
    hex_val = format(value, 'X')
    # Pad with 0's, if needed
    hex_val = '0'*(6-len(hex_val)) + hex_val
    return hex_val


class RGBcolorField(models.CharField):
    description = 'A field for holding RGB color values'
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        self._validators = []
        self.validators.append(self.validate_all_values_hex)
        super().__init__(*args, **kwargs)
    
    def validate_all_values_hex(self, value):
        try:
            hex_to_int(value)
        except:
            raise ValidationError(f'{value} is not a hex value.')
        
    def db_type(self, connection: Any) -> str:
        return 'UNSIGNED INTEGER(3)'
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return int_to_hex(value)
    
    def get_prep_value(self, value: Any) -> Any:
        return hex_to_int(value)