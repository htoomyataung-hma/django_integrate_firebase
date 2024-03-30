from django.db import models

class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=10)
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    order_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_progress = models.IntegerField(default=0)
    driver = models.ForeignKey('Driver', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_orders')
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_order = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Driver(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_progress', 'In Progress'),
    )
    driver_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    driver_progress = models.IntegerField(default=0)
    driver_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    order = models.ForeignKey('Order', null=True, blank=True, on_delete=models.SET_NULL, related_name='current_order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)