from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from userapp.views import index
from django.views.decorators.cache import never_cache,cache_control
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse
from appadmin.models import CustomUser
from django.contrib.auth.hashers import make_password

from django.utils import timezone,datetime_safe
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.template.loader import render_to_string





# Create 



def signup(request):
    if request.method=="POST":
        print('hiiiiiii')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST['password']
        password1=request.POST['password1']
        
        
        if password!=password1:
            messages.warning(request,"Password is Not ")
            return redirect(signup)
        if password==password1:
            if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(phone_number=phone_number).exists():
                
                messages.success(request,'Already exist')
                return redirect(handlelogin)
            
            print(password1)
            otp = ''.join(random.choices('0123456789', k=6))
            user = CustomUser.objects.create_user(first_name=first_name,email=email, password=password1, phone_number=phone_number, otp=otp, is_active=False) 
            print('data entered without verification')  
            send_mail('Email Verification', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email], fail_silently=False)
            request.session['otp_created_at'] = timezone.now().isoformat()
            
            print('email send')
            print(otp,"ttttttttttttttttt")
            return redirect(verify_otp)
        
        
    return render(request,"authtemplate/signup.html")
   
   
    
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@never_cache
def handlelogin(request):
    print("request hitttttttttttttt")
    if request.method=="POST":
        email=request.POST.get('email')
        userpassword=request.POST.get('password')
        user=authenticate(email=email,password=userpassword)
        print("user is", user)
        
        if user is not None:
             login(request,user)
             messages.success(request,"Login Success")
             return redirect(index)
        else:
            print("not fond")
            messages.error(request,"Invalid Credentials")
            
    return render(request,"authtemplate/login.html")
   
           
@never_cache
def handlelogout (request):
    logout(request)
    messages.info(request,"Logout Success")
    return render(request,"authtemplate/login.html")


@never_cache
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        try:
            user = CustomUser.objects.get( otp=otp)
            otp_created_at_str = request.session.get('otp_created_at')
            print(otp_created_at_str,"yyyyyyyyyyyyy")
            if otp_created_at_str is None:
                return redirect('verifyotp')
            otp_created_at = datetime_safe.datetime.fromisoformat(otp_created_at_str)
            current_time = timezone.now()
            
            if (current_time - otp_created_at).total_seconds() > 300:
                error_message = 'OTP has expired. Please request a new OTP.'
                return render(request, 'authtemplate/otppage.html', {'error_message': error_message})
            user.is_active = True
            user.save()

            customers = CustomUser.objects.all()


            request.session.pop('otp_created_at')
            return redirect('handlelogin')
        except CustomUser.DoesNotExist:
            return redirect('verifyotp')
    
    return render(request,'authtemplate/otppage.html')




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact = email)
            
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            
            message = render_to_string('authtemplate/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                
            }) 
            to_mail = email
            
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()
            
            messages.success(request,"Password resent mail has been send to your email address")
            return redirect('handlelogin')
        else:
            messages.error(request,'Account doest not exist')
    return render(request, "authtemplate/forgot_password.html")






def resetpassword_validate(request, uidb64, token):
    print("888888888888888888")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, "This link has been expired")
        return redirect('handlelogin')
    
    
    
    
    
def resetPassword(request):
    print("Reset7777777777777777")
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['password1']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            messages.success(request, "Password Reset Success")
            return redirect('handlelogin')
            
        else:
            messages.error(request, 'password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'authtemplate/reset_password.html')
    
    