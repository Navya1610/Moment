
from django.urls import path
from appadmin import views

urlpatterns = [
    # path('',views.admins,name="admins"),
    # path('admin-log',views.admin_log,name="admin_log"),
    
    path('', views.admin_signup, name="admin_signup"),
    path('index/', views.index_admin, name="index_admin"),
    path('logout',views.admin_logout,name="admin_logout"),
    path('user-details/',views.user_details,name="user_details"),
    path('user-block/<int:user_id>/',views.user_block,name="user_block"),
    path('user-unblock/<int:user_id>/',views.user_unblock,name="user_unblock"),
    path('brands/', views.brandslist, name="brandslist"),
    path('category/', views.categorylist, name="categorylist"),
    path('category/add/',views.add_category,name="add_category"),
    path('brands/add/',views.add_brand,name="add_brand"),
    path('category/edit/<int:category_id>',views.edit_category,name="edit_category"),
    path('brand/edit/<int:brand_id/',views.edit_brand,name="edit_brand"),
    path('orderlist/',views.orderlist,name="orderlist"),
    path('cancel_order/<int:order_id>/',views.canncel_order,name="canncel_order"),
    path('dashboard/',views.dashboard, name="dashboard"),
    # path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('coupon-list',views.coupon_list,name="coupon_list"),
    path('add-coupon/',views.add_coupon,name="add_coupon"),
    path('edit-coupon/<int:coupon_id>/',views.edit_coupon,name="edit_coupon"),
    path('manage-productstatus/<int:order_id>/<int:item_id>/',views.manage_productstatus,name="manage_productstatus"),
    path('order-view/<int:order_id>/',views.orderview,name="orderview"),
    path('sales/',views.saleslist,name="saleslist"),
    path('manage-orderstatus<int:order_id>/',views.manage_orderstatus,name="manage_orderstatus"),
    
]
