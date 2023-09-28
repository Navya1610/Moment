from django.shortcuts import render,get_object_or_404, redirect
from appauth.models import Product,Category ,Variants, Colour, UserDetails
from django.views.decorators.cache import never_cache,cache_control
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Orders,OrderedProducts,CartItem,Cart
from django.contrib import messages 
from django.contrib.auth import authenticate
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
@login_required(login_url='handlelogin')
@never_cache
def welcome(request):
    return render(request,"usertemplate/welcome.html")


@never_cache
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url='signup')

def index(request):
    if request.user.is_authenticated:
        print("index")
        products = Product.objects.filter(
            product_status = True,
            variants__isnull = False
            ).annotate(variants_count=Count('variants'))
        products = products.filter(variants_count__gt = 0)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        categories = Category.objects.all()
        min_price = request.GET.get('price_from')
        max_price = request.GET.get('price_to')
        
        
        
        # Filter by price range
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                products = products.filter(product_price__range=(min_price, max_price))
            except ValueError:
                # Handle invalid price inputs here (e.g., non-numeric input)
                pass

        product_count = products.count()
        
    
    
      
        context = {
            'products' : paged_products,
            'categories' : categories,
            'product_count' : product_count
        }
            
        return render(request,"usertemplate/indexuser.html",context)
    else:
        return redirect('signup')


@login_required(login_url='handlelogin')
@never_cache
def search(request):
    if 'search_product' in request.GET:
        search_product = request.GET['search_product']
        if search_product:
            products = Product.objects.order_by('product_status').filter(product_name__icontains=search_product)
    context = {
        'products' : products
    }
    return render(request, "usertemplate/indexuser.html", context)






@login_required(login_url='handlelogin')
@never_cache
def category_products(request, category_id):
    print("5555555555555555555555555555555555")
    category = get_object_or_404(Category, id = category_id)
    products = Product.objects.filter(product_category = category)
    
    context = {
        'category' : category,
        'products' : products,
    }
    
    return render(request, "usertemplate/menproducts.html", context)

@login_required(login_url='handlelogin')
@never_cache
def productview(request, product_id):
    print("22222222222222222222")
    
    product = get_object_or_404(Product, id = product_id)
    
    context = {
        'product' : product
    }
    
    return render(request,"usertemplate/singleproduct.html.html",context)


@login_required(login_url='handlelogin')
@never_cache
def men_products(request):
    
    men_products = Product.objects.filter(
        product_category = 1,
        variants__isnull = False
        ).annotate(variants_count=Count('variants'))
    
    men_products = men_products.filter(variants_count__gt = 0)
    context = {
         'products' : men_products,
     }
    
    return render(request,"usertemplate/menproducts.html",context)




@login_required(login_url='handlelogin')
@never_cache
def women_products(request):
    
    women_products = Product.objects.filter(
        product_category = 2,
        variants__isnull = False
        ).annotate(variants_count=Count('variants'))
    
    women_products = women_products.filter(variants_count__gt = 0)
    context = {
        'products' : women_products,
    }
    
    return render(request,"usertemplate/womenproduct.html", context)




@login_required(login_url='signup')
@never_cache
def product_view(request, product_id):
    
    product = get_object_or_404(Product, id= product_id)
    variants = Variants.objects.filter(product_id = product_id)
    # colors = Colour.objects.filter(id = variants.colour.id)
    colors = Colour.objects.filter(id__in=[variant.colour_id for variant in variants])
    

    
    context = {
        'product' : product,
        "variants":variants,
        "colors":colors,
        
    }
    return render(request,"usertemplate/singleproduct.html",context)





@login_required(login_url='handlelogin')
@never_cache
def invoice(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    order_items = OrderedProducts.objects.filter(order_id = order_id)
    print(order_items,"jjjjjjjjjjjjjjjjjjjjjjj")
    
    
    
    total = 0
    unit_total = 0
    discount = 0
    subtotal = 0
    
    
    for item in order_items:
        if item.discount_amount:
            discount = item.discount_amount
            total = item.subtotal
            if item.product.offer_price:
                unit_total = item.product.offer_price * item.quantity
            else:
                unit_total = item.product.product_price * item.quantity
            subtotal += unit_total
            
            
        elif item.product.offer_price:
            item.subtotal = item.product.offer_price * item.quantity
            total += item.subtotal
            unit_total = item.product.offer_price * item.quantity
            subtotal += unit_total
            
            
        else:
            item.subtotal = item.product.product_price * item.quantity
            total += item.subtotal
            unit_total = item.product.product_price * item.quantity
            subtotal += unit_total
            
        
        

    context = {
        'order': order,
        'order_items': order_items,
        'total': total,
        'unit_total' : unit_total,
        'discount' : discount,
        'subtotal' : subtotal
    
    }

    return render(request, "usertemplate/invoice.html", context)





@login_required(login_url='handlelogin')
@never_cache
def user_profile(request):
    user_details = UserDetails.objects.filter(user = request.user)
    return render(request, "usertemplate/profile.html", {'user_details':user_details})


def upload_img(request):
    user = request.user
    print("hhhhhhhhhhhhhhh")
    if request.method == 'POST':
        print("helloo")
        image = request.FILES.get('img')
        user_details, created = UserDetails.objects.get_or_create(user=user)
        user_details.img = image
        user_details.save()
        # img_url = user_details.img.url
        # return render(request, "usertemplate/profile.html", {'img_url' : img_url})
    return redirect('user_profile')


@csrf_exempt
def add_address(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        postcode = request.POST.get('postcode')
        area = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        
        user_details = UserDetails(
            user = user,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone,
            email = email,
            address_line_1 = address_line_1,
            address_line_2 = address_line2,
            postcode = postcode,
            area = area,
            state = state,
            country = country,
            
        )
        
        user_details.save()
        
        return redirect('user_profile')
        
    




@login_required(login_url='handlelogin')
@never_cache
def address_view(request):
    user_details = UserDetails.objects.get(user=request.user)
    return render(request, "usertemplate/address_view.html", {'user_details': user_details})


def edit_address(request):
    print("8888888888")
    # user = request.user
    address_id = request.POST.get('user_details.id')
    print(address_id,"88888888888")
    # address = get_object_or_404(UserDetails, user = user , id = address_id)
    # if address_id:
    #     try:
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        
        
        try:
            user_details = UserDetails.objects.get(pk = address_id)
            user_details.first_name = first_name
            user_details.last_name = last_name
            user_details.email = email
            user_details.phone_number = phone
            user_details.address_line_1 = address_line1
            user_details.address_line_2 = address_line2
            user_details.area = city
            user_details.state = state
            user_details.country = country
            user_details.postcode = postcode
            user_details.save()
            
        except UserDetails.DoesNotExist:
            print("address not found")    
    
        
                
    return redirect(user_profile)
    






def my_orders(request):
    orders = Orders.objects.filter(user=request.user).order_by('-id')
    return render(request, "usertemplate/my_orders.html",{'orders' : orders})




def cancel_order(request, order_id):
    order = get_object_or_404(Orders, id = order_id)
    
    if order.order_status == 'Pending':
        order.order_status = 'Cancelled'
        order.save()
        
    return redirect('my_orders')




def order_view(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    
    context = {
        'order' : order,
        'order_items' : order.orderedproducts_set.all(),
    }
    return render(request, "usertemplate/order_view.html", context)






def reset_password_page(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        return render(request,"usertemplate/user_reset_pass.html")




def reset_password(request):
    if request.user.is_authenticated and not request.user.is_superuser :
        if request.method == "POST":
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('new_password')
            user = authenticate(email = request.user.email, password = old_pass)
            if user is not None:
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Your password has been changed successfully.')
            else:
                messages.error(request, "Password Mismatch.")
        return render(request,"usertemplate/user_reset_pass.html")
    else:
        return render(request,"usertemplate/user_reset_pass.html")
    
    
    
    
def delete_address(request):
    user = request.user
    address_id = request.POST.get('address_id')

    if address_id:
        try:
            address_id = int(address_id)
            profile_address = get_object_or_404(UserDetails, id=address_id, user=user)
            profile_address.delete()
        except (ValueError, UserDetails.DoesNotExist):
            pass

    return redirect('user_profile')




def return_product(request,item_id):
    user = request.user
    try:
        order_product = OrderedProducts.objects.get(id = item_id)
        if order_product.product_status == "Delivered":
            order_product.product_status = "Returned"
            order_product.save()
            
    except OrderedProducts.DoesNotExist:
        messages.error(request, 'Product does not exist.')
        
    return redirect('user_profile')
        
