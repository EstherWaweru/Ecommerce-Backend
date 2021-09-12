from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.contrib import messages
from products.models import Brand, Category, Item, ItemVariation, ProductUtil, SubCategory, Variation
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
# Create your views here.
@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        print("********************",request.POST)
        print("!!!!!!!!!!!!!!!!!!!",request.FILES)
        category_name = request.POST.get('category_name')
        category_image = request.POST.get('category_image')
        print(request.FILES.get("category_image"))
        message=""
        if category_name:
            #check if category name exist
            if not Category.objects.filter(name=category_name):
                try:
                    Category.objects.create(name=category_name,image=category_image)
                    messages.success(request,"Category created succesfuly")
                    message = "Category created succesfuly"
                except:
                    messages.error(request,"Something went wrong")
                    message = "Something went wrong"
            else:
                messages.error("Category already exists!")
                message = "Category already exists!"
        return JsonResponse(message,safe = False)
    else:
       return render(request,'products/categories.html')

        


def edit_category(request):
    if request.method == 'POST':
        
        category_id = request.POST.get('category_id')
        try:
            category = Category.objects.get(id = category_id)
            data = {'name':category.name,'image':category.image.url}
            print(data)
            return JsonResponse(data, safe = False)
        except:
            return render(request,'products/categories.html')
def get_all_categories(request):
    categories = Category.objects.all()
    context={'categories':categories}
    return render(request,'products/category.html',context)
def category_view_ajax(request):
    if request.method=='POST':
        category_id=request.POST.get("category_id")
        category=Category.objects.get(id=category_id)
        sub_categories=category.sub_categories.all()
        data={'category':category.name,'sub_categories':list(sub_categories.values('name','id'))}
        return JsonResponse(data)
    else:
        return render(request,'products/category.html')
def delete_category_ajax(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        try:
            Category.objects.filter(id = category_id).delete()
            messages.success(request,"Category created succesfuly")
            return JsonResponse(json.dumps({'status':200}))
        except:
             messages.error(request,"Operation not succesful")
             return render(request,'products/categories.html')
            
def edit_category_ajax(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.POST.get('category_image')
        category_id = request.POST.get('category_id')
        #check if category exist
        category = Category.objects.get(id = category_id)
        data ={}
        # if category.name != category_name:
        #     if Category.object.get(name = category_name):
        #         messages.error(request,'Category Exists!')
        #         return render(request,'products/categories.html')
        try:
            Category.objects.filter(id = category_id).update(name = category_name,image = category_image)
            data = {'status':200,'detail':'Success'}
            return JsonResponse(json.dumps(data))
        except:
            messages.error(request,'Something went wrong!')
            return render(request,'products/categories.html')

def delete_multiple_categories(request):
    pass
def add_multiple_categories(request):
    if request.method == 'POST':
        category_name = request.POST.getlist('category_name[]')
        category_image = request.POST.getlist('category_image[]')
        category_dict = {category_name[i]: category_image[i] for i in range(len(category_name))}
        categories = []
        for category in category_dict:
            name=category
            image = category_dict[category]
            categories.append(Category(
            name=name,
            image=image,
             ))
        print("*****************")
        print(categories)
        Category.objects.bulk_create(categories)
        messages.success(request,'Successfuly')
        return JsonResponse({'status':"Sucessfuly"})

#sub_categories routes
def get_all_sub_categories(request):
    sub_categories = SubCategory.objects.all()
    context={'sub_categories':sub_categories}
    return render(request,'products/sub_category.html',context)
def get_categories(request):
    categories = Category.objects.all().values('id','name')
    return JsonResponse(list(categories),safe = False)
    
def add_sub_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('sub_category_name')
        image = request.POST.get('sub_category_image')
        category = Category.objects.get(id = category_id)
        if category:
            SubCategory.objects.create(name = name,image = image,categories = category)
            messages.success(request,'Operation succesful',)
            return JsonResponse(json.dumps({'status':'successful'}))
        else:
            messages.error(request,'Something went wrong!')
            return render(request,'products/sub_category.html')

def delete_sub_category_ajax(request):
    if request.method == 'POST':
        id  = request.POST.get('id')
        try:
            SubCategory.objects.filter(id = id).delete()
            messages.success(request,'Operation successful')
            return JsonResponse({'status','sucess'},safe = False)
        except:
            messages.error(request,'Something went wrong')
            return render(request,'products/sub_category.html')
    else:
        return render(request,'products/sub_category.html')

def edit_sub_category(request):
    if request.method == 'POST':
        id = request.POST.get('sub_category_id')
        try:
            sub_category = SubCategory.objects.get(id = id)
            categories = Category.objects.all().values('id','name')
            data = {'category_id':sub_category.categories.id,'name':sub_category.name,
            'image':sub_category.image.url,'category_name':sub_category.categories.name,'categories':list(categories)}

            return JsonResponse(data,safe = False)
        except:
            return render(request,'products/sub_category.html')    
    else:
        return render(request,'products/sub_category.html')
def edit_sub_category_ajax(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('sub_category_name')
        image = request.POST.get('sub_category_image')
        category_id = request.POST.get('category')
        id = request.POST.get('id')
        try:
            category = Category.objects.get(id = category_id)
            SubCategory.objects.filter(id = id).update(name = name,image = image,categories = category)
            messages.success(request,'Operation succesful')
            return JsonResponse(json.dumps({'status':'Success!'}),safe = False)
        except:
            messages.error(request,'Something went wrong')
            return render(request,'products/sub_category.html')
    else:
        return render(request,'products/sub_category.html')

def delete_multiple_sub_categories(request):
    pass
def add_multiple_sub_categories(request):
    if request.method == 'POST':
        names = request.POST.getlist('sub_category_name[]')
        images = request.POST.getlist('sub_category_image[]')
        category_id = request.POST.getlist('category[]')
        
    else:
        return render(request,'products/sub_category.html')

    
        
#Brabd views
def add_brand(request):
    if request.method == 'POST':
        name = request.POST.get('brand_name')
        image = request.POST.get('brand_image')
        Brand.objects.create(name = name,image = image)
        messages.success(request,'Operation succesful')
        return JsonResponse({'status':'success'},safe = False)
    else:
        return render(request,'products/brand.html')


def update_brand(request):
    if request.method == 'POST':
        id = request.POST.get('brand_id')
        try:
            brand = Brand.objects.get(id = id)
            data = {'name':brand.name,'image':brand.image.url,'id':brand.id}
            return JsonResponse(data,safe=False)
        except:
            return render(request,'products/brand.html')

def edit_brand_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('brand_name')
        image = request.POST.get('brand_image')
        id = request.POST.get('id')
        try:
            Brand.objects.filter(id = id).update(name = name, image = image,id = id)
            messages.success(request,'Operation succesful')
            return JsonResponse({'status':'success'}, safe = False)
        except:
            messages.error(request,'Something went wrong')
            return render(request,'products/brand.html')
def get_all_brands(request):
    brands = Brand.objects.all()
    context = {'brands':brands}
    return render(request,'products/brand.html',context=context)
def delete_brand(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            Brand.objects.filter(id = id).delete()
            messages.success(request,'Operation succesful')
            return JsonResponse({'status':'success'},safe = False)
        except:
            messages.error(request,'Something went wrong!')
            return render(request,'products/brand.html')

def delete_multiple_brands(request):
    pass
def brand_view_ajax(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        brand = Brand.objects.get(id = id)
        products = brand.products.all()
        data={'brand':brand.name,'items':list(products.values('name','id'))}
        return JsonResponse(data)
    else:
        return render(request,'products/brand.html')


def add_multiple_brands(request):
    if request.method == 'POST':
        brand_name = request.POST.getlist('brand_name[]')
        brand_image = request.POST.getlist('brand_image[]')
        brand_dict = {brand_name[i]: brand_image[i] for i in range(len(brand_name))}
        brands = []
        try:
            for brand in brand_dict:
                name=brand
                image = brand_dict[brand]
                brands.append(Brand(
                name=name,
                image=image,
                ))
            Brand.objects.bulk_create(brands)
            messages.success(request,'Operation Successful')
            return JsonResponse({'status':"Sucessfuly"})
        except:
            messages.error(request,'Something went wrong')
            return render(request,'products/brand.html')
    else:
        return render(request,'products/brand.html')

#item views
def get_all_items(request):
    items = Item.objects.all()
    context = {'items':items}
    return render(request,'products/item.html',context=context)
def get_brands_subcategories(request):
    sub_categories = SubCategory.objects.all().values('id','name')
    brands = Brand.objects.all().values('id','name')
    data = {'brands':list(brands),'sub_categories':list(sub_categories)}
    return JsonResponse(data,safe = False)
def add_item(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('item_name')
        image = request.POST.get('item_image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discounted_price =request.POST.get('discounted_price')
        brand_id = request.POST.get('brand_id')
        sub_category_id = request.POST.get('sub_category_id')
        brand = Brand.objects.get(id = brand_id)
        sub_category = SubCategory.objects.get(id = sub_category_id)
        Item.objects.create(name = name,image = image,description=description,price = price,
        discounted_price = discounted_price,brands = brand,subcategories=sub_category)
        messages.success(request,'Operation successful!')
        return JsonResponse({'status':'success'},safe=False)
    else:
        return render(request,'products/item.html')

def edit_item(request):
    if request.method == 'POST':
        id = request.POST.get('item_id')
        try:
            item = Item.objects.get(id = id)
            sub_categories = SubCategory.objects.all().values('id','name')
            brands = Brand.objects.all().values('id','name')
            data = {'sub_category_id':item.subcategories.id,'sub_category_name':item.subcategories.name,
            'brand_id':item.brands.id,'brand_name':item.brands.name,'image':item.image.url,
            'description':item.description,'price':item.price,'discounted_price':
            item.discounted_price,'name':item.name,'sub_categories':list(sub_categories),'brands':list(brands)}

            return JsonResponse(data,safe = False)
        except:
            return render(request,'products/sub_category.html')    
    else:
        return render(request,'products/sub_category.html')
    
def edit_item_ajax(request):
    pass
def delete_item(request):
    pass
def delete_multiple_items(request):
    pass
def item_view_ajax(request):
    pass
def add_multiple_items(request):
    pass
