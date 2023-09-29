from django.shortcuts import render,redirect,get_object_or_404
from appauth.models import Product,Variants,UserDetails
from .models import Cart,CartItem,CheckOut,CheckOutItem,Orders,OrderedProducts
from django.contrib import messages
import razorpay
from project import settings
from cart.models import Orders
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order, PaymentStatus
from .models import UserCoupon, Coupon
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse
from decimal import Decimal
import json
from decimal import Decimal
from django.urls import reverse
from django.http import HttpResponseRedirect
import uuid
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required



RAZORPAY_KEY_ID = 'rzp_test_lc7mOufDT5YP3x'
RAZORPAY_KEY_SECRET = '3FqFEd2qxQICvlqYiKaaByBU'


# Create your views here.
@login_required(login_url='handlelogin')
@never_cache
def add_cart(request, product_id, variant_id):
    if request.method == 'POST':
        print("add cartttttttttttttttttttttttttttt")
        product = get_object_or_404(Product, id = product_id)
        variant = get_object_or_404(Variants, id = variant_id)
        cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id= cart_id)  #get the cart using the cart id present in the session
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = cart_id
        )
    cart.save()

    
    
    try:
        cart_item = CartItem.objects.get(product=product,variant=variant, cart=cart)
        if cart_item.variant.variant_stock > cart_item.quantity:
            
            cart_item.quantity += 1 
            # Check if there is an offer price and update the product price
            if product.offer_price is not None:
                cart_item.product_price = product.offer_price
            else:
                    cart_item.product_price = product.product_price  # Set product_price to default if no offer price
            cart_item.save()
    
    
    
    except CartItem.DoesNotExist:
        if variant.variant_stock > 0:
            cart_item = CartItem.objects.create(
                product = product,
                variant = variant,
                quantity = 1,
                cart = cart,
                user = request.user,
            )

            # Check if there is an offer price and set the product price
            if product.offer_price is not None:
                cart_item.product_price = product.offer_price
            else:
                cart_item.product_price = product.product_price  # Set product_price to default if no offer price
            cart_item.save()
        
    return redirect('cart')
        
        



@login_required(login_url='handlelogin')
@never_cache
def cart(request,  total_discount = 0):
    total = 0
    quantity = 0
    
    print("carttttttttttttttttttttt")
    try:
        cart_items = CartItem.objects.filter(user=request.user)
    except:
        pass
    
    try:
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)           
        
        
        
        for cart_item in cart_items:
            product = cart_item.product
            variant = cart_item.variant
            
            # if cart_item.quantity != cart_item.quantity_in_database:
            #     cart_item.quantity_in_database = cart_item.quantity
            
            item_price = product.offer_price if product.offer_price is not None else product.product_price
            cart_item.total_amount = item_price * cart_item.quantity
            cart_item.product.product_price = item_price
            cart_item.save()
            
            if variant:
                cart_item.variant_image = variant.img1
                cart_item.variant_stock = variant.variant_stock
                
            cart_item.total_amount = product.product_price * cart_item.quantity
            cart_item.save()
            
            
                
            total += cart_item.total_amount
            quantity += cart_item.quantity
            
            
        
            if variant and cart_item.quantity >= variant.variant_stock:
                cart_item.at_max = True
            else:
                cart_item.at_max = False
                
        
        total_discount = request.session.get('total_discount',0)
        total_discount = float(total_discount)
        print(total_discount)
        
        if total_discount:
            for cart_item in cart_items:
                print(total_discount)
                cart_item.coupon_amount = total_discount
                cart_item.save()
            total -= total_discount

        
    except Cart.DoesNotExist:
        # cart_items = []
        # total= 0
        # quantity = 0
        # total_discount = 0
        pass
        
        
    print(total_discount,"totalllllllllllllllll")
    
    try:
        cart_item = CartItem.objects.filter(user=request.user)
        if not cart_item:
            total= 0
            quantity = 0
            total_discount = 0
            
            
    except:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        # 'cart_items': cart_items,
        'cart_item':cart_item,
        'total_discount' : total_discount,
        
    }
    
    return render(request, "usertemplate/cart.html",context)







def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print(cart)
    return cart





def update_cart_item_quantity(request, cart_item_id, action):
    try:
        cart_item =CartItem.objects.get(id = cart_item_id)
        
        if action == 'increase':
            cart_item.quantity += 1
            print(cart_item.variant.variant_stock,"aaaaaaaaaaaaaaaaa")
            if cart_item.variant and cart_item.variant.variant_stock > 0:
                cart_item.variant.variant_stock -= 1
                cart_item.variant.save()
                print(cart_item.variant.variant_stock,"bbbbbbbbbbbbbbbbbbb")
        elif action == 'decrease':
            if cart_item.quantity > 1 :
                cart_item.quantity -= 1
                
                if cart_item.variant:
                    cart_item.variant.variant_stock += 1
                    cart_item.variant.save()                
        else:
            pass
        
        cart_item.save()
        # messages.success(request, 'Quantity updated Successfully')
        
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart')





def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.variant:
        cart_item.variant.variant_stock += cart_item.quantity
        cart_item.variant.save()
    cart_item.delete()
    return redirect(cart)




@login_required(login_url='handlelogin')
@never_cache
def checkout(request):
    print("cheooooooooooooooooooooo")
    
    total = 0
    quantity = 0
    total_discount = 0
    grand_total = 0
    cart_items = None
    
    try:
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        cart_items = CartItem.objects.filter(user=request.user)
        
        for cart_item in cart_items:
            product = cart_item.product
            variant = cart_item.variant
            coupon_amount = cart_item.coupon_amount
            
            print(coupon_amount,"couponnnnnnnnnnnn")
            print(cart_item.quantity,"858585858585454545656565252525")
            if variant:
                cart_item.variant_image = variant.img1
                cart_item.variant_stock = variant.variant_stock
                
            item_price = product.offer_price if product.offer_price is not None else product.product_price
            # cart_item.product.product_price = item_price
                
            grand_total += item_price * cart_item.quantity
            total += grand_total
            print(total,"rrrrrrrrrrrrrrrrr")
            print(grand_total)
            print(item_price)
            
            if coupon_amount is not None:
                total_discount += coupon_amount
                
                print(total_discount,"discounttttttttttttt")
                
            quantity += cart_item.quantity
            
            try:
                if coupon_amount:
                    total -= coupon_amount
            except:
                pass
            
            print(quantity)
            
            if variant and cart_item.quantity >= variant.variant_stock:
                cart_item.at_max = True
            else:
                cart_item.at_max = False
                
        print(total)
        
        
    except Cart.DoesNotExist:
        cart_items = []
        total= 0
        quantity = 0
        total_discount = 0
        
        
    user_details = UserDetails.objects.filter(user=request.user)
    
    if request.method == 'POST':
        print("iffffffffffffffffffffff")
        selected_address_id = request.POST.get('selected_address')
        print(selected_address_id)
        if selected_address_id:
            try:
                
                selected_address = UserDetails.objects.get(id=selected_address_id)
                UserDetails.objects.filter(user=request.user)
                checkout_data = {
                    'user' : request.user,
                    'first_name' : selected_address.first_name,
                    'last_name' : selected_address.last_name,
                    'phone_number' : selected_address.phone_number,
                    'address_line_1' : selected_address.address_line_1,
                    'address_line_2' : selected_address.address_line_2,
                    'postcode' : selected_address.postcode,
                    'area' : selected_address.area,
                    'state' : selected_address.state,
                    'country' : selected_address.country,
                    'email' : selected_address.email,
                }
                
                checkout = CheckOut(**checkout_data)  # Create a new CheckOut instance using the data from checkout_data
                checkout.save()
                
                print(checkout_data,"bbbbbbbbbbbbbbbbbbbbbbbut")
                
                print(selected_address)
                
            except:
                pass
            print(checkout.id)
            
        return redirect('payment_select', checkout_id = checkout.id)
                
            
            
        
    context = {
        'user_details' : user_details,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'total_discount' : total_discount,
        'grand_total' : grand_total
        
        
    }
     
    return render(request, "usertemplate/checkout.html", context)



@login_required(login_url='handlelogin')
@never_cache
def payment_select(request, checkout_id, unit_amount = 0):
    
    try:
        checkout = CheckOut.objects.get(id=checkout_id)
        first_name = checkout.first_name
    except:
        print("first try block")
        pass
    
    user = request.user
    # try:
    # cart = Cart.objects.get(cart_id = _cart_id(request))
    # cart_items = CartItem.objects.filter(cart=cart, is_active = True)
    cart_items = CartItem.objects.filter(user=request.user)
    
    grand_total = 0
    discount_amount = 0

    for cart_item in cart_items:
        
        grand_total += cart_item.total_amount
        
        if cart_item.coupon_amount is not None:
            discount_amount += cart_item.coupon_amount
            
    total = grand_total - discount_amount
    
        
    print(total)
        
            
    # except:
    #      print("2 try block")
    
    
    
    # try:
        
    if request.method == 'POST':
        print("post METHOD")
        payment_mode = request.POST.get('payment_mode')
        if payment_mode == 'cod':
            order_number = str(uuid.uuid4().int)
            print("codddddddddddddddddddddddd")
            print(total,checkout,payment_mode,"55555555555555555555555")
            payment_mode = 'Cash on Delivery'
            print(user,total,checkout,payment_mode,"55555555555555555555555")
            orders = Orders.objects.create(
                user = user,
                order_number = order_number,
                order_total_amount = total,
                billing_address = checkout,
                shipping_address = checkout,
                payment_mode = payment_mode,
            )
            
            for cart in cart_items:
                if cart.product.offer_price:
                    unit_amount = cart.product.offer_price * cart.quantity
                else:
                    unit_amount = cart.product.product_price * cart.quantity
                orderedproducts = OrderedProducts.objects.create(
                    order = orders,
                    product = cart.product,
                    quantity = cart.quantity,
                    subtotal = total,
                    unit_amount = unit_amount,
                    discount_amount = None if cart_item.coupon_amount is None else cart_item.coupon_amount,
                )

            cart_items.delete()
            
            
        elif payment_mode == 'razorpay':
            order_number = str(uuid.uuid4().int)
            print("razzzzzzzzzzzzzzzzz")
            
            payment_mode = 'Razorpay'
            
        
            
            amount = total
            name = first_name
            
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

            razorpay_order = client.order.create(
                {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )
            print(razorpay_order)
            order = Order.objects.create(
                name=name, amount=amount,
                provider_order_id =razorpay_order["id"],
                
            )
            order.save()
            
            
            orders = Orders.objects.create(
                user = user,
                order_number = order_number,
                order_total_amount = total,
                billing_address = checkout,
                shipping_address = checkout,
                payment_mode = payment_mode
        )
            orders.save() 
            
            for cart in cart_items:
                if cart.product.offer_price:
                    unit_amount = cart.product.offer_price * cart.quantity
                else:
                    unit_amount = cart.product.product_price * cart.quantity
                orderedproducts = OrderedProducts.objects.create(
                    order = orders,
                    product = cart.product,
                    quantity = cart.quantity,
                    subtotal = total,
                    unit_amount = unit_amount,
                    discount_amount = None if cart_item.coupon_amount is None else cart_item.coupon_amount,
                    
                ) 
            

            return render(
                request,"usertemplate/payment.html",
                {
                    "callback_url": "http://" + "127.0.0.1:8000" + "/accounts/callback/",
                    "razorpay_key": 'rzp_test_lc7mOufDT5YP3x',
                    "order": order,
                },
            )
            
            
        print(orders.id,"addddddddddddddddddddddd")
        
        
        return redirect('order_confirmation', order_id = orders.id)
    
    # except :
    #     print('error ocuured')
        
        
        
    return render(request, "usertemplate/payment_select.html",{'checkout_id':checkout_id})
    
    
    
    
@never_cache       
def order_confirmation(request, order_id):
    print(order_id,"ttttttttttttttttttttttttttttt")
    order = get_object_or_404(Orders, pk=order_id)
    ordered_products = order.orderedproducts_set.all()
    
    
    print
    context = {
        'orders' : order,
        'ordered_products' : ordered_products,
    }
    return render(request, "usertemplate/order_confirmation.html", context)

@login_required(login_url='handlelogin')
@never_cache
def invoice(request,order_id):
    order = Orders.objects.get(id=order_id)
    return render(request, "usertemplate/invoice.html")



def apply_coupon(request):
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        print(coupon_code)
        
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            user = request.user
            if UserCoupon.objects.filter(user=user, coupon_applied=coupon).exists():
                print("Coupon has already been applied by this user.")
                
            else:
                if coupon.is_valid():
                    total_discount = float(coupon.discount)
                    request.session['total_discount'] = total_discount
                    print("Coupon applied successfully!")
                    
                    
                    UserCoupon.objects.create(user=user, coupon_applied=coupon)
                        
                else:
                    print("Coupon is not valid.")
                
        except Coupon.DoesNotExist:
            print("Invalid Coupon Code.")
            
    return redirect('cart')


