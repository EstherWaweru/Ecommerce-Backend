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

def get_category(request):
    pass
def get_all_categories(request):
    categories = Category.objects.all()
    context={'categories':categories}
    return render(request,'products/category.html',context)
def delete_categories(request):
    pass
def category_view_ajax(request):
    pass
def create_category_ajax(request):
    pass
def create_category(request):
    pass
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


def ajax_edit_category(request):
    pass
def delete_multiple_categories(request):
    pass
def add_multiple_categories(request):
    if request.method == 'POST':
        category_name = request.POST.getlist('category_name[]')
        print(category_name)
        category_image = request.POST.getlist('category_image[]')
        category_dict = {category_name[i]: category_image[i] for i in range(len(category_name))}
        print(category_dict)
        categories = []
        print("-----------------")
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
    pass
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
        # try:
        category = Category.objects.get(id = category_id)
        sub_category = SubCategory.objects.get(id = id)
        # if sub_category.name != name:
            # if SubCategory.objects.get(name = name):
            #     messages.error(request,'Sub Category Already Exists!')
            #     return render(request,'products/sub_category.html')

        SubCategory.objects.filter(id = id).update(name = name,image = image,categories = category)
        messages.success(request,'Operation succesful')
        return JsonResponse(json.dumps({'status':'Success!'}),safe = False)
        # except:
        #     messages.error(request,'Something went wrong')
        #     return render(request,'products/sub_category.html')
    else:
        return render(request,'products/sub_category.html')

def delete_multiple_sub_categories(request):
    pass
def add_multiple_sub_categories(request):
    pass

    
        





def add_brand(request):
    pass
def update_brand(request):
    pass
def get_brand(request):
    pass
def get_all_brands(request):
    pass
def delete_brand(request):
    pass

# def add_category(request):
#     pass
# def update_category(request):
#     pass
# def get_category(request):
#     pass
# def get_all_categories(request):
#     pass
# def delete_categories(request):
#     pass

# def add_category(request):
#     pass
# def update_category(request):
#     pass
# def get_category(request):
#     pass
# def get_all_categories(request):
#     pass
# def delete_categories(request):
#     pass
