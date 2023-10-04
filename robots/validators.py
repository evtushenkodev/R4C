import re
from datetime import datetime

from django.core.exceptions import ValidationError


def validate_model_version(value):
    """
    Validate model and version.

    Args:
        value (str): The value to be validated.

    Returns:
        str: The validated value.

    Raises:
        ValidationError: If the value is not a combination of digits or English letters.
    """
    pattern = r"^[a-zA-Z0-9]*$"
    if re.match(pattern, value):
        return value
    raise ValidationError(
        "Invalid model or version name. It should consist of digits or English letters."
    )


def validate_creation_date(value):
    """
    Validate date and time.

    Args:
        value (str): The value to be validated.

    Raises:
        ValidationError: If the value is not in the 'YYYY-MM-DD HH:MM:SS' format or if it's later than the current time.
    """

    current_time = datetime.now().replace(tzinfo=None)
    if value.replace(tzinfo=None) >= current_time:
        raise ValidationError("Creation date cannot be later than the current time.")
