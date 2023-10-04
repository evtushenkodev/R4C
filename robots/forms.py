from django import forms

from robots.models import Robot
from robots.validators import validate_model_version, validate_creation_date


class RobotCreateForm(forms.Form):
    model = forms.CharField(max_length=2, validators=[validate_model_version])
    version = forms.CharField(max_length=2, validators=[validate_model_version])
    created = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"],
        validators=[validate_creation_date],
    )

    def save_robot(self):
        """
        Create and save a new robot based on the form data.

        This method retrieves cleaned data from the form, generates the robot serial,
        and saves the robot to the database.
        """
        model = self.cleaned_data["model"]
        version = self.cleaned_data["version"]
        created = self.cleaned_data["created"]
        serial = self.generate_serial(model, version)
        robot = Robot(serial=serial, model=model, version=version, created=created)
        robot.save()

    @classmethod
    def generate_serial(cls, model, version):
        """
        Generate a robot serial based on model and version.

        Args:
            model (str): The robot's model.
            version (str): The robot's version.

        Returns:
            str: The generated robot serial.
        """
        return f"{model}-{version}"
