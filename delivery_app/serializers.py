from rest_framework import serializers
from .models import Order, Customer, Driver


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'address', 'phone_no']


class OrderSerializer(serializers.ModelSerializer):
    # customer_id = serializers.SerializerMethodField(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer',
                                                     write_only=True)
    driver = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'customer_id', 'order_progress', 'status_order', 'driver']

    def get_customer(self, obj):
        if obj.customer_id:
            customer_id = {
                'customer_id': obj.customer_id.customer_id,
                'name': obj.customer.name,
                'address': obj.customer.address,
                'phone_no': obj.customer.phone_no,
            }
            return customer_id
        else:
            return None

    def get_driver(self, obj):
        if obj.driver:
            driver = {
                'driver': obj.driver.driver_id,
                'name': obj.driver.name,
                'customer': obj.customer.name,
                'driver_progress': obj.driver.driver_progress,
                'driver_status': obj.driver.driver_status,
                # 'order': obj.driver.order.items if obj.driver.order else None,
                # 'customer': obj.driver.customer.name if obj.driver.customer else None
            }
            return driver
        else:
            return None


class DriverSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField(read_only=True)
    customer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Driver
        fields = ['driver_id', 'name', 'driver_progress', 'driver_status', 'order', 'customer']

    def get_order(self, obj):
        if obj.order:
            order = {
                'order_id': obj.order.order_id,
                'customer': obj.order.customer.name if obj.order.customer else None,
                'status_order': obj.order.status_order if obj.order.status_order else None,
            }
            return order
        else:
            return None

    def get_customer(self, obj):
        if obj.order:
            return obj.order.customer.name if obj.order.customer else None
        else:
            return None
