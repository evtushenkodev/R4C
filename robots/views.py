import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from robots.forms import RobotCreateForm


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):
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
