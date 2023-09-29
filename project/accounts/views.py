from django.shortcuts import render,redirect,get_object_or_404
from project import settings
from cart.models import Orders,CartItem
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order, PaymentStatus



RAZORPAY_KEY_ID = 'rzp_test_lc7mOufDT5YP3x'
RAZORPAY_KEY_SECRET = '3FqFEd2qxQICvlqYiKaaByBU'



# Create your views here.

def order_payment(request):
    print("ppppppppppppppppppppppppp")
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        print(first_name)
        amount = request.POST.get("total")
        print(amount)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET_))
        
        razorpay_order = client.order.create(
            {"amount" : int(amount) * 100, "currency" : "INR", "payment_capture": "1"}
        )    
                        
        order = Orders.objects.create(
            user = request.user,
            order_number = razorpay_order["id"],
            billing_address = None,
            shipping_address = None,
        )
        order.save()
        return render(
            request,"usertemplate/payment.html",
              {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": 'rzp_test_lc7mOufDT5YP3x',
                "order": order,
            },
        )
    return render(request,"usertemplate/payment.html")






@csrf_exempt
def callback(request):
    print("calllllllllllllllllll")
    def verify_signature(response_data):
        print("verifyyyyyyyyyyyy")
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        print(client)
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        print(payment_id,"888888888888")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        print(provider_order_id)
        signature_id = request.POST.get("razorpay_signature", "")
        print(signature_id,"55555555555555")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        print(signature_id,"zzzzzzzzzzzzz")
        
        if verify_signature(request.POST):
            print("sucesssssssssssss")
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect('ordersuccess')
        else:
            order.status = PaymentStatus.FAILURE
            print("ffffffffffffffff")
            order.save()
            return redirect('orderfailure')
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return redirect('orderfailure')
       





def ordersuccess(request):
    cart_item = CartItem.objects.filter(user=request.user)
    for cart in cart_item:
        cart.delete()
    return render(request,"usertemplate/confirmation.html")

def orderfailure(request):
    orders = Orders.objects.all().order_by('id').first()
    orders.delete()
    
    return render(request,"errorpage.html")
    