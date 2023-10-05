import io
import json
from datetime import date

from django.core.exceptions import ValidationError
from django.http import JsonResponse, FileResponse, HttpResponseNotFound
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from robots.services import generate_report
from robots.forms import RobotCreateForm


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):
    """
    View for creating a robot.

    Accepts a POST request with JSON data containing the robot details.
    If the data is valid, the robot is saved and a success message is returned.
    If the data is invalid, a JSON response with the form errors is returned.
    If the JSON data is invalid, a JSON response with an error message is returned.
    If any other exception occurs, a JSON response with the error message is returned.
    """

    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body.decode("utf-8"))
            form = RobotCreateForm(request_data)

            if form.is_valid():
                form.save_robot()
                return JsonResponse({"message": "The robot has been created."})
            else:
                return JsonResponse({"errors": form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RobotReportView(View):
    """
    View for generating and downloading the robot manufacturing report.

    Accepts a GET request to generate the report.
    If no robots were manufactured in the past week, a 404 response is returned.
    If the report is generated successfully, it is saved as an Excel file and returned as a file response.
    The filename of the downloaded file includes the current date.
    """

    def get(self, request):
        workbook, report_data = generate_report()
        if not report_data:
            return HttpResponseNotFound(
                {'No robots were manufactured in the past week.'}
            )
        buffer = io.BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        current_date = date.today().strftime('%Y-%m-%d')
        response = FileResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response[
            'Content-Disposition'
        ] = f'attachment; filename=robot_report_{current_date}.xlsx'
        return response
