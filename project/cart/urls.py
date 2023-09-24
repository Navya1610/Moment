from django.urls import path
from cart import views



urlpatterns = [
    path('',views.cart,name="cart"),
    path('add_cart/<int:product_id>/<int:variant_id>/',views.add_cart,name="add_cart"),
    path('_cart_id/',views._cart_id,name="_cart_id"),
    path('update_quantity/<int:cart_item_id>/<str:action>/',views.update_cart_item_quantity,name="update_cart_item_quantity"),
    path('remove_item/<int:cart_item_id>/',views.remove_cart_item,name="remove_cart_item"),
    path('checkout/',views.checkout,name="checkout"),
    path('order_confirmation/<int:order_id>/',views.order_confirmation,name="order_confirmation"),
    # path('invoice/',views.invoice,name="invoice"),
    path('apply-coupon/',views.apply_coupon,name="apply_coupon"),
    path('payment_select/<int:checkout_id>/',views.payment_select,name="payment_select"),
    
    
]
