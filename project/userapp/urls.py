from django.urls import path
from .import views

urlpatterns = [
    path('',views.welcome,name="welcome"),
    path('home/',views.index,name="index"),
    path('product/',views.productview,name="productview"),
    path('category/<int:category_id>/',views.category_products,name="category_products"),
    # path('product/<int:product_id>/',views.productview,name="productview"),
    path('products/men',views.men_products,name="men_products"),
    path('products/women',views.women_products,name="women_products"),
    path('single-product/<int:product_id>/',views.product_view,name="product_view"),
    path('invoice/<int:order_id>/',views.invoice,name="invoice"),
    path('profile/',views.user_profile,name="user_profile"),
    path('add_address/',views.add_address,name="add_address"),
    path('address_view/',views.address_view,name="address_view"),
    path('edit_address/<int:user_details_id>/',views.edit_address,name="edit_address"),
    path('my_orders/',views.my_orders,name="my_orders"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name="cancel_order"),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password-page', views.reset_password_page, name='reset_password_page'),
    path('delete_address/',views.delete_address,name="delete_address"),
    path('order-view-user/<int:order_id>/',views.order_view,name="order_view"),
    path('return-product/<int:item_id>/',views.return_product,name="return_product"),
    path('search/',views.search,name="search"),
    path('upload_img/',views.upload_img,name="upload_img"),
    
]

