import pdb

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Driver, Customer
from .serializers import OrderSerializer, CustomerSerializer, DriverSerializer
import firebase_admin
from firebase_admin import db, credentials

cred = credentials.Certificate('G:\Side-Project\order-80576-firebase-adminsdk-yjbu0-65c5af888e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://order-80576-default-rtdb.asia-southeast1.firebasedatabase.app'
})


class CustomerAPI(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, customer_id):
    #     name = request.data.get('name')
    #     address = request.data.get('address')
    #     phone_no = request.data.get('phone_no')
    #     customer = Customer.objects.filter(customer_id=customer_id).first()
    #     if customer is None:
    #         response_data = {"response": "Customer does not exists"}
    #         return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    #     customer.name = name
    #     customer.address = address
    #     customer.phone_no = phone_no
    #     customer.save()
    #     response_data = {"response": "Customer Updated"}
    #     return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, customer_id):
        try:
            customer = Customer.objects.get(pk=customer_id)
            name = request.data.get('name')
            address = request.data.get('address')
            phone_no = request.data.get('phone_no')
            customer.name = name
            customer.address = address
            customer.phone_no = phone_no
            customer.save()
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response({"response": "Customer Deleted"}, status=status.HTTP_200_OK)


class Order_Tracker_API(APIView):
    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()  # Save the new order
            driver = self.find_next_available_driver()  # Find the next available driver
            if driver:
                # Assign the driver and update order status
                order.driver = driver
                order.status_order = 'in_progress'
                order.save()
                driver.driver_status = 'in_progress'
                driver.save()
                return Response({'message': 'Order created and matched with driver successfully'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No available driver found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, order_id):
    #     try:
    #         order = Order.objects.get(pk=order_id)
    #     except Order.DoesNotExist:
    #         return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     serializer = OrderSerializer(order, data=request.data)
    #     if serializer.is_valid():
    #         # Check if the order status is completed
    #         if serializer.validated_data.get('status_order') == 'completed' and serializer.validated_data.get(
    #                 'order_progress') == 100:
    #             # Update the corresponding driver's status
    #             driver = order.driver
    #             if driver:
    #                 driver.driver_status = 'available'
    #                 driver.driver_progress = 0
    #                 driver.save()
    #         elif serializer.validated_data.get('status_order') == 'canceled' and serializer.validated_data.get(
    #                 'order_progress') == 0:
    #             driver = order.driver
    #             if driver:
    #                 driver.driver_status = 'available'
    #                 driver.driver_progress = 0
    #                 driver.save()
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            status_order = validated_data.get('status_order')
            order_progress = validated_data.get('order_progress')

            # Check if the order status is completed or canceled
            if status_order in ['completed', 'canceled']:
                if status_order == 'completed' and order_progress == 100:
                    # Update the corresponding driver's status to available and progress to 0
                    driver = order.driver
                    if driver:
                        driver.driver_status = 'available'
                        driver.driver_progress = 0
                        driver.save()
                elif status_order == 'canceled' and order_progress == 0:
                    driver = order.driver
                    if driver:
                        driver.driver_status = 'available'
                        driver.driver_progress = 0
                        driver.save()

            # Save the order and update Firebase
            serializer.save()
            firebase_ref = db.reference(f'order/update/{order_id}')
            firebase_ref.set({
                'order_progress': order_progress,
                'status_order': status_order
            })

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def find_next_available_driver(self):
        # Implement logic to find the next available driver
        # For example:
        available_drivers = Driver.objects.filter(driver_status='available')
        if available_drivers.exists():
            return available_drivers.first()
        else:
            return None


class DriverAPI(APIView):
    def get(self, request):
        driver = Driver.objects.all()
        serializer = DriverSerializer(driver, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, driver_id):
    #     name = request.data.get('name')
    #     driver_progress = request.data.get('driver_progress')
    #     driver_status = request.data.get('driver_status')
    #     order = request.data.get('order')
    #     customer = request.data.get('customer')
    #     driver = Driver.objects.filter(driver_id=driver_id).first()
    #     if driver is None:
    #         response_data = {"response": "Driver does not exists"}
    #         return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    #     driver.name = name
    #     driver.driver_progress = driver_progress
    #     driver.driver_status = driver_status
    #     driver.order = order
    #     driver.customer = customer
    #     driver.save()
    #     firebase_ref = db.reference(f'driver/update/{driver_id}/progress')
    #     firebase_ref.set(driver_progress)
    #     response_data = {"response": "Driver Updated"}
    #     return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, driver_id):
        name = request.data.get('name')
        driver_progress = request.data.get('driver_progress')
        driver_status = request.data.get('driver_status')
        order_id = request.data.get('order')  # Assuming order ID is provided in request data
        customer_id = request.data.get('customer')  # Assuming customer ID is provided in request data

        # Retrieve Driver instance
        driver = Driver.objects.filter(driver_id=driver_id).first()
        if driver is None:
            response_data = {"response": "Driver does not exist"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Update driver fields
        driver.name = name
        driver.driver_progress = driver_progress
        driver.driver_status = driver_status

        # Assign Order instance to driver if order ID is provided
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                driver.order = order
            except Order.DoesNotExist:
                return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Assign Customer instance to driver if customer ID is provided
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id)
                driver.customer = customer
            except Customer.DoesNotExist:
                return Response({"error": "Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Save driver object
        driver.save()

        # Update driver progress in Firebase
        # firebase_ref = db.reference(f'driver/update/{driver_id}/progress')
        # firebase_ref.set(driver_progress)

        firebase_ref = db.reference(f'driver/update/{driver_id}')
        firebase_ref.set({
            'name': name,
            'driver_progress': driver_progress,
            'driver_status': driver_status
        })

        response_data = {"response": "Driver Updated"}
        return Response(response_data, status=status.HTTP_200_OK)
