from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.contrib import messages
from products.models import Brand, Category, Item, ItemVariation, ProductUtil, SubCategory, Variation
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
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
        if category.name == category_name:
            return JsonResponse(data = {'status_code':400,'detail':'Object Exists!'},safe=False)
        try:
            Category.objects.filter(id = category_id).update(name = category_name,image = category_image)
            data = {'status':200,'detail':'Success'}
            return JsonResponse(json.dumps(data))
        except:
            return JsonResponse(data = {'status_code':500,'detail':'Something went wrong!'},safe=False)


def ajax_edit_category(request):
    pass
def delete_multiple_categories(request):
    pass
def add_multiple_categories(request):
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
