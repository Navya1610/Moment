from django.urls import path
from appauth import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('otp/',views.verify_otp,name="verify_otp"),
    path('forgot-password/',views.forgot_password,name="forgot_password"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name="resetpassword_validate"),
    path('resetPassword/',views.resetPassword,name="resetPassword"),
]
