from django.db import models
from appadmin.models import CustomUser
from appauth.models import Product,Variants,Category, UserDetails
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.utils import timezone



# Create your models here.



class Coupon(models.Model):


    
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    min_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    

    def is_valid(self):
        current_time = timezone.now()
        return self.is_active and self.start_date <= current_time and self.end_date >= current_time


    
    def __str__(self):
        return self.code






class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_coupon_applied = models.BooleanField(default=False)
    
    def _str_(self):
        return self.cart_id  
    
    def total(self):
        cart_items = self.cartitem_set.all()
        total = sum(cart_item.product.product_price * cart_item.quantity for cart_item in cart_items)
        return total



    
        
    
class CheckOut(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=30, default='default@example.com')
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
   
class CartItem(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    coupon_amount = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    
    
    
class CheckOutItem(models.Model):
    checkout = models.ForeignKey(CheckOut, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
 
    
    
    
   
    
    
    
    
class Orders(models.Model):
    STATUS =(

        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled','Cancelled'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        
    )
    
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=200, unique=True)
    order_total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    order_created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.CharField(max_length=100, null=True)
    # quantity = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=250, null=True)

    billing_address = models.ForeignKey(CheckOut, related_name='billing_orders', on_delete=models.SET_NULL,null=True)
    shipping_address = models.ForeignKey(CheckOut, related_name='shipping_orders', on_delete=models.SET_NULL, null=True)
    products_ordered = models.ManyToManyField(Product, through='OrderedProducts')
    order_cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.first_name}"
    
    
    
    @property
    def total_revenue(self):
        ordered_products = self.orderedproducts_set.all()
        total = sum(product.subtotal for product in ordered_products)
        return total
    
    

    
    
class OrderedProducts(models.Model):
    PRODUCT_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        
    )
    product_status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='Pending')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    unit_amount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"
        
    def calculate_subtotal(self):
        return self.quantity * self.product.product_price






class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
    
    
    


    
    




class UserCoupon(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank=True)
    is_applied = models.BooleanField(default=True)
    
    def __str__(self):
        if self.coupon_applied:
            return self.coupon_applied.code
        return "No Coupon Applied"
    
    
    
    

