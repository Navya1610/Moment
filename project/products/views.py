from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from appauth.models import Product,Category,Brands, Colour, Variants
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, Http404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required




# Create your views here.


@login_required
@never_cache
def mendisplay(request):
    return render(request,'usertemplate/menproducts.html')

@login_required
@never_cache
def womendisplay(request):
    return render(request,"usertemplate/womenproducts.html")


def toggle_product_status(request, product_id):
    try:
        if request.method == 'POST':
            product = Product.objects.get(pk=product_id)
            product.product_status = not product.product_status
            product.save()
            return redirect(productlist)
    except Product.DoesNotExist:
        return render(request,"admintemplate/errorpage.html", status=404)
    except Exception as e:
        return render(request, "errorpage.html",{'error_message' : str(e)}, status=500)



# @never_cache
# def productlist(request):
#     try:
#         print("product")
#         products = Product.objects.all()
#         brand = Brands.objects.all()
#         categories = Category.objects.all()
#         # if request.user.is_superuser:
#         #     products = Product.objects.all()
#         #     brand = Brands.objects.all()
#         #     categories = Category.objects.all()
#         return render(request, "admintemplate/product.html", {'products': products, 'brand': brand, 'categories': categories})

#     except Product.DoesNotExist:
#         return HttpResponse("No products Fount.", status = 404)
    
#     except Exception as e:
#         return HttpResponse(f"An error occourred : {e}", status = 500)

@login_required(login_url='admin_signup')
@never_cache
def productlist(request):
        products = Product.objects.all()
        categories = Category.objects.all()
        product_count = products.count()
        brands = Brands.objects.all()
        variants = Variants.objects.all()
        colors = Colour.objects.all()
        print(brands,"2222222222222222222")
        context = {
            "products" : products,
            "product_count" : product_count,
            "categories" : categories,
            "brands" : brands,
            "variants" : variants,
            'colors' : colors
        }
        return render(request, "admintemplate/product.html",context)


@never_cache
def add_product(request):
    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            product_category_id = request.POST.get('product_category')
            product_brand_id = request.POST.get('product_brand')
            product_details = request.POST.get('product_description')
            product_price = request.POST.get('product_mrp')
            quantity = request.POST.get('product_quantity')
            offer_price = request.POST.get('product_offer_price')
            product_brand_name = Brands.objects.get(id=product_brand_id)
            product_category_name = Category.objects.get(id=product_category_id)       
            product_image = request.FILES.get('product_image')
            # print(product_price,quantity,offer_price,product_brand_name,product_category_name,product_details)
            product = Product(
                product_name=product_name,
                product_category=product_category_name,
                product_brand=product_brand_name,
                product_price=product_price,
                # quantity=quantity,
                product_details=product_details,
                product_image=product_image,
                offer_price=offer_price
            )
            product.save()
            
            
            
            return redirect('productlist')
        
        except(Brands.DoesNotExist, Category.DoesNotExist):
            return HttpResponse("Invalid Category or brand", status=400)
        
        except Exception as e:
            return HttpResponse(f"An error occurerd : {e}", status = 500)
    
    return render(request, "admintemplate/product.html")


# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == 'POST':
#         new_product_name = request.POST.get('product_name')
#         new_product_category_id = request.POST.get('category')
#         new_product_brand_id = request.POST.get('brand')
#         new_product_price = request.POST.get('product_mrp')
#         new_product_description = request.POST.get('product_description')

#         try:
#             edited_category = Category.objects.get(id=new_product_category_id)
#             edited_brand = Brands.objects.get(id=new_product_brand_id)
#         except:
#             pass

#         edit = Product.objects.get(id=product_id)
#         edit.product_name = new_product_name
#         edit.product_brand = edited_brand
#         edit.product_category = edited_category
#         edit.product_price = new_product_price
#         edit.product_details = new_product_description
#         edit.save()
#         return redirect(productlist)

#     context = {
#         'edit': product
#     }
#     return render(request, "admintemplate/product.html", context)
@never_cache
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    print("33333333333333333333333333")

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('brand')  # Use 'brand' instead of 'product_brand'
        category_id = request.POST.get('category')  # Use 'category' instead of 'product_category'
        product_price = request.POST.get('product_mrp')
        offer_price = request.POST.get('offer_price')
        product_stock = request.POST.get('product_stock')
        product_description = request.POST.get('product_description')
        print(brand_id,category_id,product_price,product_stock,product_description,"0000000000000000000")

        # Retrieve the updated 'images' field value
        product_thumbnail = request.FILES.get('product_thumbnail')

        # Update other product details
        product.product_name = product_name
        product.product_brand = get_object_or_404(Brands, id=brand_id)
        product.product_category = get_object_or_404(Category, id=category_id)
        product.product_price = product_price
        product.offer_price = offer_price
        product.quantity = product_stock
        product.product_details = product_description


        # Only update 'images' if a new file was provided
        if product_thumbnail:
            product.images = product_thumbnail

        # Save the updated product
        product.save()

        return redirect('productlist')

    return render(request, 'admintemplate/product.html', {'product': product})



@login_required(login_url='admin_signup')
@never_cache
def colorlist(request):
    print("colourlist 00000000000000000000000000000000000")
    color = Colour.objects.all()
    return render(request,"admintemplate/colour.html",{'colour' : color})


@never_cache
def add_colour(request):
    print("add colorrrrrrrrrrrrrrrrrrrrrrrr")
    if request.method == 'POST':
        if request.POST['color']:
            color = request.POST.get('color')
            if Colour.objects.filter(colour_name = color).exists():
                messages.error(request,"Already exists")
                return redirect(colorlist)
            else:
                c = Colour()
                c.colour_name = color
                c.save()
                messages.success(request,"Added new colour")
                return redirect(colorlist)
        else:
            messages.error(request,"Required field")
            return redirect(colorlist)
        
        
        
# def variantlist(request,product_id):
#     product = Product.objects.get(pk = product_id)
#     variants = Variants.objects.filter(product_id=product)
#     color = Colour.objects.all()
#     context = {
#         'product' : product,
#         'variants' : variants,
#         'color' : color,
#     }
#     return render(request,"admintemplate/variant.html", context)

  
        
# def add_variant(request):
#     if request.method == 'POST':
#         product_color_id = request.POST.get('product_color')
#         variant_details = request.POST.get('varient_details')
#         variant_stock = int(request.POST.get('varient_stock'))
#         variant_status = bool(request.POST.get('varient_status'))
#         img1 = request.FILES.get('img1')
#         img2 = request.FILES.get('img2')
#         img3 = request.FILES.get('img3')
#         product_id = int(request.POST.get('product_id'))
#         product_color_name = Colour.objects.get(id=product_color_id)
        
        
#         try:
#             product = Product.objects.get(pk = product_id)
            
#         except Product.DoesNotExist:
#             return redirect('variantlist', product_id=product_id)
        
        
#         variant = Variants.objects.create(
#             colour = product_color_name,
#             variant_details = variant_details,
#             variant_stock = variant_stock,
#             variant_status = variant_status,
#             img1 = img1,
#             img2 = img2,
#             img3 = img3,
#             product = product,
#         )
        
#         return redirect('variantlist', product_id=product_id)
    
#     return render(request,"admintemplate/variant.html")



@never_cache       
def add_variant(request,product_id):
    if request.method == 'POST':
        product_color_id = request.POST.get('product_color')
        variant_details = request.POST.get('varient_details')
        variant_stock = request.POST.get('varient_stock')
        variant_status = request.POST.get('varient_status')
        # img1 = request.FILES.get('img1')
        # img2 = request.FILES.get('img2')
        # img3 = request.FILES.get('img3')
        product_id = int(request.POST.get('product_id'))
        product_color_name = Colour.objects.get(id=product_color_id)
        
        
        try:
            product = Product.objects.get(pk = product_id)
            
        except Product.DoesNotExist:
            return redirect('variantlist', product_id=product_id)
        
        
        variant = Variants.objects.create(
            colour = product_color_name,
            variant_details = variant_details,
            variant_stock = variant_stock,
            variant_status = variant_status,
            # img1 = img1,
            # img2 = img2,
            # img3 = img3,
            product = product,
        )
        
        return redirect('variantlist', product_id=product_id)
    
    return render(request,"admintemplate/variant.html")


@never_cache
def add_variantdemo(request,id):
    product = get_object_or_404(Product, id = id)
    print(id)
    if request.method == 'POST':
       product_color_id = request.POST.get('variant_color')
       details = request.POST.get('variant_description')
       stock = request.POST.get('variant_quantity')
       img = request.FILES.get('variant_image')
       product_color_name = Colour.objects.get(id = product_color_id)
       product_name = Product.objects.get(id = id)
       
       
       product = Variants(
       product = product_name,
       colour = product_color_name,
       variant_details = details,
       variant_stock = stock,
       img1 = img,
       )
       product.save()
       
       return redirect('productlist')
       
       
        
    return render(request,"admintemplate/product.html")

@login_required(login_url='admin_signup')
@never_cache
def variantlist(request):
    # product = get_object_or_404(Product, id=id)
    variants = Variants.objects.all()
    return render(request, "admintemplate/variant.html",{'variants' : variants})