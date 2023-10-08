from django import forms

from customers.models import Customer
from orders.models import Order
from robots.models import Robot
from robots.validators import validate_model_version


class OrderCreateForm(forms.Form):
    """
    A custom form for creating robot orders.

    This form allows customers to place orders for robots by providing their email address, the robot's model,
    and the robot's version.

    Attributes:
        customer_email (EmailField): The customer's email address.
        robot_model (CharField): The model of the robot.
        robot_version (CharField): The version of the robot.

    Methods:
        save_custom_order(): Validates the form data and creates a new order for the customer if a robot
        with the specified model and version is available in the stock.

        generate_robot_serial(model, version): Generates a unique robot serial based on the model and version.
    """

    customer_email = forms.EmailField(max_length=255, label='Customer Email')
    robot_model = forms.CharField(max_length=2, validators=[validate_model_version], label='Robot Model')
    robot_version = forms.CharField(max_length=2, validators=[validate_model_version], label='Robot Version')

    def save_robot_order(self):
        """
        Create a new robot order for the customer.

        This method validates the form data and creates a new order for the customer if a robot with the specified
        model and version is available in the stock. It also updates the robot's status to 'READY' if the robot is
        available, or 'NO_ROBOT_IN_STOCK' if it's not.

        Returns:
            None
        """

        customer_email = self.cleaned_data['customer_email']
        robot_model = self.cleaned_data['robot_model']
        robot_version = self.cleaned_data['robot_version']
        robot_serial = self.generate_robot_serial(robot_model, robot_version)
        customer, created = Customer.objects.get_or_create(email=customer_email)
        robot = Robot.objects.filter(serial=robot_serial, ordered=False).first()

        if robot:
            robot.ordered = True
            robot.save()
            order_status = 'READY'
        else:
            order_status = 'ROBOT_IS_OUT_OF_STOCK'

        order = Order(customer=customer, robot_serial=robot_serial, status=order_status)
        order.save()

    @staticmethod
    def generate_robot_serial(model, version):
        """
        Generate a robot serial based on model and version.

        Args:
            model (str): The robot's model.
            version (str): The robot's version.

        Returns:
            str: The generated robot serial.
        """
        return f"{model}-{version}"
