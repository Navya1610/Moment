from django.urls import path
from accounts import views

urlpatterns = [
    path('payment/',views.order_payment,name="order_payment"),
    path('callback/', views.callback, name="callback"),
    path('ordersuccess/',views.ordersuccess, name="ordersuccess"),
    path('orderfailure/',views.orderfailure, name="orderfailure"),
]
