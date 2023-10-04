import json
from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Robot


class RobotCreateViewTest(TestCase):
    def test_valid_robot_creation(self):
        # Create valid JSON data for a robot
        robot_data = {
            "model": "R2",
            "version": "D2",
            "created": "2023-10-04 23:59:59"
        }

        # Send a POST request to the view
        response = self.client.post(reverse("create_robot"), json.dumps(robot_data), content_type="application/json")

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Check that a new robot is created in the database
        self.assertEqual(Robot.objects.count(), 1)

    def test_invalid_robot_creation(self):
        # Create invalid JSON data for a robot
        invalid_robot_data = {
            "model": "Invalid Model",  # Invalid model
            "version": "D2",
            "created": "2023-10-04 23:59:59"
        }

        # Send a POST request to the view
        response = self.client.post(reverse("create_robot"), json.dumps(invalid_robot_data),
                                    content_type="application/json")

        # Check that the response has a status code of 400 (invalid data)
        self.assertEqual(response.status_code, 400)

        # Check that no new robot is created in the database
        self.assertEqual(Robot.objects.count(), 0)

    def test_future_creation_date(self):
        # Create JSON data with a future date
        future_robot_data = {
            "model": "R2",
            "version": "D2",
            "created": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        }

        # Send a POST request to the view
        response = self.client.post(reverse("create_robot"), json.dumps(future_robot_data),
                                    content_type="application/json")

        # Check that the response has a status code of 400 (future date is not allowed)
        self.assertEqual(response.status_code, 400)

        # Check that no new robot is created in the database
        self.assertEqual(Robot.objects.count(), 0)
