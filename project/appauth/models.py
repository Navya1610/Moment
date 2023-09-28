from django.db import models
from appadmin.models import CustomUser
from django.utils import timezone



# Create your models here.




class UserDetails(models.Model):
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,unique=True)
    email = models.CharField(max_length=30, default='default@example.com')
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    area  = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    img = models.ImageField(default = None,blank = True,null = True)
    
    def __str__(self):
        return self.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    
    
    
class Brands(models.Model):
    brand_name = models.CharField(max_length=50)
    
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    
    
    
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_brand = models.ForeignKey(Brands,on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_price = models.IntegerField()
    product_details = models.TextField(max_length=2000,blank=True)
    product_image = models.ImageField(upload_to = 'product_image/',default = None,blank = True,null = True)
    offer_price = models.IntegerField(blank=True,null=True)
    product_status = models.BooleanField(default=True)


    
class Colour(models.Model):
    colour_name = models.CharField(max_length=50,null=True)
    
    
class Variants(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    colour = models.ForeignKey(Colour,on_delete=models.CASCADE,null=True)
    variant_details = models.TextField(max_length=2000,blank=True)
    variant_stock = models.PositiveBigIntegerField(default=0)
    img1 = models.ImageField(upload_to='product_image/',blank=True,default=None,null=True)
    variant_status = models.BooleanField(default=True)
     
     
     
     
