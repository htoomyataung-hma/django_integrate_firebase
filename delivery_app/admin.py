from django.contrib import admin
from .models import Customer, Order, Driver

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Driver)
# Register your models here.
