from django.urls import path
from products import views

urlpatterns = [
    path('',views.mendisplay,name="mendisplay"),
    path('women/',views.womendisplay,name="womendisplay"),
    path('product/status/<int:product_id>/',views.toggle_product_status,name="toggle_product_status"),
    path('product/', views.productlist, name="productlist"),
    path('product/add/', views.add_product, name="add_product"),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    # path('product/variant/<int:product_id>/', views.product_variant, name="product_variant"),
    # path('variant/add/',views.add_variant,name="add_variant"),
    # path('product/edit/variant/<int:variant_id>/',views.edit_variant,name="edit_variant"),
    path('color/',views.colorlist,name="colorlist"),
    path('add-color/',views.add_colour,name="add_colour"),
    path('variantlist/<int:product_id>/',views.variantlist,name="variantlist"),
    path('add-variant/<int:product_id>/',views.add_variant,name="variant_add"),
    path('add_variantdemo/<int:id>/',views.add_variantdemo,name="add_variantdemo"),
    path('variantlist/',views.variantlist,name="variantlist")
    
    
]
