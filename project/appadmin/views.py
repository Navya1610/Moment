from logging.config import IDENTIFIER
from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from appauth.models import Category,Brands
from appadmin.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache,cache_control
import re
from cart.models import Orders,OrderedProducts,Order,Coupon
from django.db.models import Sum

from datetime import datetime, timedelta




# Create your views here.


def admin_signup(request):
    print("hy")
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(index_admin)
    if request.method == 'POST':
        email = request.POST.get('ad_email')
        print(email)
        password = request.POST.get('ad_password')
        print(password)
        try:
            user=CustomUser.objects.get(email=email)
            if user.is_active == False:
                user.is_active = True
                user.save()
        except:
            messages.info(request, 'Invalid Credentials')
        user = authenticate(email=email,password=password)
        print(user)
        if user and user.is_superuser:
            
            login(request,user)
            return redirect(index_admin)
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect(admin_signup)
    else:
        return render(request, "admintemplate/signup.html")
    
    
    
# @never_cache 
# def admins(request):
#     if request.user.is_superuser:
#         return redirect(index_admin)
#     return redirect(admin_log)



# @never_cache
# def admin_log(request):
#     # if request.user.is_superuser:
#     #     return redirect(index_admin)
#     return render(request,"admintemplate/signup.html")

    
  
  
  
@login_required(login_url='admin_signup')
@never_cache
@cache_control(no_cache = True, must_revalidate = True, no_store = True) 
def index_admin(request):
    
    print("hello")
    return render(request,"admintemplate/index.html")




@never_cache
def admin_logout(request):
    request.session.flush()
    messages.info(request,"Logout Sucessful")
    return redirect(admin_signup)


@login_required(login_url='admin_signup')
@never_cache
def user_details(request):
    print("user")
    data = CustomUser.objects.all()
    
    
    return render(request,"admintemplate/user_details.html",{"data":data})

@never_cache
def user_block(request,user_id):
    if request.method == "POST":
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.save()
        print(user,'user blocked')
        return redirect(user_details)
    
@never_cache   
def user_unblock(request,user_id):
    if request.method == "POST":
        user= CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save()
        print(user)
        return redirect(user_details)


@login_required(login_url='admin_signup')
@never_cache
def categorylist(request):
    categories = Category.objects.all()
    print("category")
    if request.user.is_superuser:
        categories = Category.objects.all()
    return render(request,"admintemplate/category.html",{'categories':categories})




@login_required(login_url='admin_signup')
@never_cache
def brandslist(request):
    print("brandlist")
    brand = Brands.objects.all()
    if request.user.is_superuser:
        brand = Brands.objects.all()
    # else:
    #     return redirect(admin_log)
    return render(request,"admintemplate/brands.html",{'brand':brand})

@never_cache
def add_category(request):
    print("add category")
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        
        pattern = r'^[a-zA-Z]+$'
        
        if not re.match(pattern, category_name):
            error_message = "Category name invalid"
            return render(request,"admintemplate/category.html",{'error_message': error_message})
        
        
        category = Category(category_name=category_name)
        category.save()
        return redirect('categorylist')
    return render(request,"admintemplate/category.html")


@never_cache
def add_brand(request):
    print("add brand")
    if request.method =='POST':
        brand_name = request.POST.get('brand_name')
        brand = Brands(brand_name=brand_name)
        brand.save()
        return redirect('brandslist')
 
 
 

@never_cache
def edit_category(request, category_id):
    print("edit category")
    if request.method == 'POST':
        edited_category_name = request.POST.get('category_name')
        category = Category.objects.get(id=category_id)
        category.category_name = edited_category_name
        category.save()
        return redirect('categorylist')
    
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admintemplate/category.html', context)
        
        
        

@never_cache
def edit_brand(request, brand_id):
    print("edit brand")
    if request.method == 'POST':
        edited_brand_name = request.POST.get('brand_name')
        brand = Brands.objects.get(id=brand_id)
        brand.brand_name = edited_brand_name
        brand.save()
        return redirect('brandslist')

    brand = Brands.objects.all()
    context = {
        'brand': brand
    }
    return render(request, "admintemplate/brand.html", context)


@login_required(login_url='admin_signup')
@never_cache
def orderlist(request):
    orders = Orders.objects.all()
    status = Orders.STATUS
    
    context = {
        'orders' : orders,
        'status' : status,
    }
    return render(request, "admintemplate/orders.html", context)




@never_cache
def manage_productstatus(request,order_id, item_id):
    
    order = get_object_or_404(Orders, id=order_id)
    item = get_object_or_404(OrderedProducts, id=item_id)
    orders = OrderedProducts.objects.all()
    statuses = OrderedProducts.PRODUCT_STATUS
    print('statuse',statuses)
    if request.method == "POST":
        print("mmmmmmmmmmmmmmmmmmm")
        product_status = request.POST.get('status')
        print(product_status,"yyyyyyyyyyyyyyyyyy")
        item.product_status = product_status
        item.save()
        messages.success(request, 'Order status updated successfully.')
        
        
        order = item.order
        if order.orderedproducts_set.filter(product_status ='Delivered').count() == order.orderedproducts_set.count():
            order.order_status = 'Delivered'
        elif order.orderedproducts_set.filter(product_status ='Returned').count() == order.orderedproducts_set.count():
            order.order_status = 'Returned'
        else:
            order.order_status = 'Pending'
        order.save()
        
        
        return redirect('orderlist')  # Redirect after successful update
        
    context = {
        'item' : item,
        'order' : order,
        'orders' : orders,
        'statuses' : statuses,
    }
    return render(request, "admintemplate/orderview.html", context)



@never_cache
def manage_orderstatus(request, order_id):
    orders = get_object_or_404(Orders, id=order_id)
    if request.method =="POST":
        order_status = request.POST.get('status')
        orders.order_status = order_status
        orders.save()
        
    
        return redirect(orderlist)
    
    context ={
        'orders' : orders
    }
    
    return render(request, "admintemplate/orders.html", context)




@never_cache
def orderview(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    orders = OrderedProducts.objects.all()
    statuses = OrderedProducts.PRODUCT_STATUS
    
    
    context = {
        'order' : order,
        'order_items' : order.orderedproducts_set.all(),
        'orders' : orders,
        'statuses' : statuses,
    }
    return render(request, "admintemplate/orderview.html", context)



@never_cache
def canncel_order(request, order_id):
    order = get_object_or_404(Orders, id = order_id)
    
    if request.method == 'POST':
        order.order_status = 'Cancelled'
        order.save()
        
        return redirect(orderlist)
    
    return redirect(orderlist)


@never_cache
@login_required(login_url='admin_signup')
def dashboard(request):
    print("uuuuuuuuuuuuuuuuuuuuuuuuu")

    # Get current date
    current_date = datetime.now()

    # Calculate the start date for the week and month
    week_start_date = current_date - timedelta(days=current_date.weekday())
    
    # Calculate the end date for the week
    week_end_date = week_start_date + timedelta(days=6)
    
    # Calculate the start date for the month
    month_start_date = current_date.replace(day=1)
    
    # Calculate the end date for the month
    next_month = month_start_date.replace(day=28) + timedelta(days=4)  # Move to end of the month
    month_end_date = next_month - timedelta(days=next_month.day)

    # Get total sales for the current year
    current_year = current_date.year
    yearly_sales = Orders.objects.filter(
        order_created_date__year=current_year
    ).aggregate(total=Sum('order_total_amount'))['total'] or 0

    # Get total sales for the current month
    monthly_sales = Orders.objects.filter(
        order_created_date__gte=month_start_date,
        order_created_date__lte=month_end_date
    ).aggregate(total=Sum('order_total_amount'))['total'] or 0

    # Get total sales for the current week
    weekly_sales = Orders.objects.filter(
        order_created_date__gte=week_start_date,
        order_created_date__lte=week_end_date
    ).aggregate(total=Sum('order_total_amount'))['total'] or 0

    # Get total sales for all time
    total_sales = Orders.objects.aggregate(total=Sum('order_total_amount'))['total'] or 0

    status_order_totals = Orders.objects.values('order_status').annotate(total=Sum('order_total_amount'))

    context = {
        'status_order_totals': status_order_totals,
        'yearly_sales': yearly_sales,
        'monthly_sales': monthly_sales,
        'weekly_sales': weekly_sales,
        'total_sales': total_sales,
    }

    return render(request, "admintemplate/index.html", context)








# @login_required
# def dashboard(request):
#     print("uuuuuuuuuuuuuuuuuuuuuuuuu")
#     # orders = Orders.objects.all()
#     # order_dates = [order.order_created_date for order in orders]
#     # total_revenue = sum(order.total_revenue for order in orders)
#     # context = {
#     #     'order_dates' : order_dates,
#     #     'total_revenue' : total_revenue,
#     # }
    
#     status_order_totals = Orders.objects.values('order_status').annotate(total = Sum('order_total_amount'))
#     print(status_order_totals)
#     context = {
#         'status_order_totals' : status_order_totals,
#     }
#     return render(request,"admintemplate/index.html", context)


@login_required(login_url='admin_signup')
@never_cache
def saleslist(request):
    sales_report = Orders.objects.all()
    
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    clear_filter = request.GET.get('clearFilter')
    
    
    if clear_filter:
        start_date= None
        end_date = None
    
    elif start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        sales_report = sales_report.filter(order_created_date__range =(start_date,end_date))
        

    context = {
        'sales_report': sales_report,
    }
    return render(request, "admintemplate/sales.html", context)








@login_required(login_url='admin_signup')
@never_cache
def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons' : coupons
    }
    return render(request, "admintemplate/coupon.html", context)




@never_cache
def add_coupon(request):
    if request.method == 'POST':
        
        coupon_code = request.POST.get('coupon_code')
        coupon_description = request.POST.get('coupon_description')
        coupon_discount = request.POST.get('discount')
        min_amount = request.POST.get('min_amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        coupon_is_active = request.POST.get('is_active')
        
        coupon = Coupon(
            code = coupon_code,
            description = coupon_description,
            discount = coupon_discount,
            start_date = start_date,
            end_date = end_date,
            min_amount = min_amount,
            is_active = bool(coupon_is_active)
        )
        coupon.save()
        return redirect('coupon_list')
    return redirect(request, "admintemplate/coupon.html")

@never_cache
def edit_coupon(request, coupon_id):
        if request.method == 'POST':
            edit_coupon_code = request.POST.get('coupon_code')
            edit_coupon_description = request.POST.get('coupon_description')
            edit_coupon_discount = request.POST.get('discount')
            edit_coupon_start_date = request.POST.get('start_date')
            edit_end_date = request.POST.get('end_date')
            edit_min_amount = request.POST.get('min_amount')
            edit_coupon_is_active = request.POST.get('is_active')
            
            coupon = Coupon.objects.get(id=coupon_id)
            
            coupon.code = edit_coupon_code
            coupon.description = edit_coupon_description
            coupon.discount = edit_coupon_discount
            coupon.start_date = edit_coupon_start_date
            coupon.end_date = edit_end_date
            coupon.min_amount = edit_min_amount
            coupon.is_active = bool(edit_coupon_is_active)
            
            coupon.save()
            
            return redirect('coupon_list')
        
        return render(request, "admintemplate/coupon.html")

