from django.urls import path
from .views import Order_Tracker_API, CustomerAPI, DriverAPI

urlpatterns = [
    path('customer/list/', CustomerAPI.as_view()),
    path('customer/create/', CustomerAPI.as_view()),
    path('customer/update/<int:customer_id>', CustomerAPI.as_view()),
    path('customer/delete/<int:customer_id>', CustomerAPI.as_view()),
    path('order/list/', Order_Tracker_API.as_view()),
    path('order/create/', Order_Tracker_API.as_view()),
    path('order/update/<int:order_id>', Order_Tracker_API.as_view()),
    # path('fulfill-order/create/<int:order_id>', FulfillOrder.as_view()),
    path('driver/list/', DriverAPI.as_view()),
    path('driver/create/', DriverAPI.as_view()),
    path('driver/update/<int:driver_id>', DriverAPI.as_view()),
    # Add other URL patterns as needed
]
