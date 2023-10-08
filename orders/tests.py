from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
import json

from orders.models import Order
from robots.models import Robot
from customers.models import Customer
from .signals import update_robot_availability

ORDER_DATA = {
    "customer_email": "customer@example.com",
    "robot_model": "R2",
    "robot_version": "D2"
}


class OrderCreateViewTest(TestCase):
    def test_valid_order_creation(self):
        # Send a POST request to the view
        response = self.client.post(reverse("create_order"), json.dumps(ORDER_DATA), content_type="application/json")

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check that a new order is created in the database
        self.assertEqual(Order.objects.count(), 1)

    def test_invalid_order_creation(self):
        # Create invalid JSON data for an order
        invalid_order_data = {
            "customer_email": "invalid_email",  # Invalid email
            "robot_model": "R2",
            "robot_version": "D2"
        }

        # Send a POST request to the view
        response = self.client.post(reverse("create_order"), json.dumps(invalid_order_data),
                                    content_type="application/json")

        # Check that the response has a status code of 400 (invalid data)
        self.assertEqual(response.status_code, 400)

        # Check that no new order is created in the database
        self.assertEqual(Order.objects.count(), 0)

    def test_order_creation_with_existing_robot(self):
        # Create a robot in the database
        robot = Robot.objects.create(serial="R2-D2", model="R2", version="D2", created=timezone.now())

        # Send a POST request to the view
        response = self.client.post(reverse("create_order"), json.dumps(ORDER_DATA), content_type="application/json")

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check that a new order is created in the database
        self.assertEqual(Order.objects.count(), 1)

        # Check that the robot is marked as ordered
        robot.refresh_from_db()
        self.assertTrue(robot.ordered)

    def test_order_creation_with_non_existing_robot(self):
        # Send a POST request to the view
        response = self.client.post(reverse("create_order"), json.dumps(ORDER_DATA), content_type="application/json")

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check that a new order is created in the database
        self.assertEqual(Order.objects.count(), 1)

        # Check that no new robot is created in the database
        self.assertEqual(Robot.objects.count(), 0)


class RobotAvailabilitySignalTest(TestCase):
    def test_signal_handler(self):
        customer = Customer.objects.create(email='test@example.com')
        robot = Robot.objects.create(
            serial='M1-V2',
            model='M1',
            version='V2',
            created=timezone.now(),
            ordered=False
        )
        order = Order.objects.create(
            customer=customer,
            robot_serial=robot.serial,
            status='ROBOT_IS_OUT_OF_STOCK'
        )
        update_robot_availability(sender=Robot, instance=robot, created=True)
        order.refresh_from_db()
        self.assertEqual(order.status, 'READY')
