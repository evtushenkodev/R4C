from django.db import models

from orders.utils import ORDER_STATUS
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    status = models.CharField(choices=ORDER_STATUS, default='CREATED', max_length=64,)
