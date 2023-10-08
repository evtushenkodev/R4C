from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'robot_serial')


admin.site.register(Order, OrderAdmin)
