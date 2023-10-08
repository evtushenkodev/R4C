import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from orders.forms import OrderCreateForm


@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateView(View):
    """
    A custom view for creating robot orders.

    This view allows customers to place orders for robots by providing their email address, the robot's model,
    and the robot's version in a JSON payload.

    Methods:
        post(request, *args, **kwargs): Handles the POST request to create a new robot order.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            form = OrderCreateForm(data)
            if not form.is_valid():
                return JsonResponse({'errors': form.errors}, status=400)
            form.save_robot_order()
            return JsonResponse({'message': 'Order successfully created.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)