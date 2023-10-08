from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse

from R4C import settings
from orders.models import Order

from robots.models import Robot


@receiver(post_save, sender=Robot)
def update_robot_availability(sender, instance, created, **kwargs):
    """
    Custom signal receiver to notify customers when a robot becomes available.

    Args:
        sender: The sender of the signal.
        instance: The instance of the Robot model that triggered the signal.
        created: A boolean indicating whether the instance was just created.
        kwargs: Additional keyword arguments.

    Returns:
        JsonResponse: A JSON response indicating the result of the notification process.
    """
    if created:
        orders_with_robot = Order.objects.filter(
            robot_serial=instance.serial, status='ROBOT_IS_OUT_OF_STOCK'
        )

        for order in orders_with_robot:
            notify_customer_about_robot_availability(order)


def notify_customer_about_robot_availability(order):
    subject = 'Robot in stock'
    model, version = order.robot_serial.split('-')
    message = f"""
            Добрый день!
            Недавно вы интересовались нашим роботом модели {model}, версии {version}. 
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
            """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email]
    order.status = 'READY'
    order.save()

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)