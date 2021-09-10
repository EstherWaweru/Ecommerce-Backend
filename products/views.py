from django.shortcuts import render
from django.contrib import messages
from products.models import Brand, Category, Item, ItemVariation, ProductUtil, SubCategory, Variation
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
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
                data={'status':message}
        return JsonResponse(data)
    else:
       return render(request,'products/categories.html')

        


def edit_category(request):
    pass
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
    pass
def edit_category_ajax(request):
    pass
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
