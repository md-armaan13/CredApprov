from django.core.exceptions import ValidationError

def validate_not_empty_or_single_space(value):
    if value == "" or value == " ":
        raise ValidationError("Phone number cannot be an empty string or a single space.")