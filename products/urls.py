from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
#crud urls
app_name='products'
urlpatterns=[
    path('category/',views.get_all_categories,name='categories'),
    path('category_view_ajax/',views.category_view_ajax,name="category_view_ajax"),
    path('add_category/',views.add_category,name="add_category"),
    path('add_multiple_categories',views.add_multiple_categories,name="add_multiple_categories"),
    path('delete_category_ajax/',views.delete_category_ajax,name="delete_category_ajax"),
    path('edit_category/',views.edit_category,name="edit_category"),
    path('edit_category_ajax/',views.edit_category_ajax,name="edit_category_ajax"),
    path('delete_multiple_categories/',views.delete_multiple_categories,name="delete_multiple_categories"),
    path('category_view_ajax/',views.category_view_ajax,name = 'category_view_ajax'),
    #sub category urls
    path('sub_categories/', views.get_all_sub_categories, name = 'sub_categories'),
    path('get_categories/',views.get_categories,name = 'get_categories'),
    path('add_sub_category/',views.add_sub_category, name = 'add_sub_category'),
    path('delete_sub_category/',views.delete_sub_category_ajax, name = 'delete_sub_category_ajax'),
    path('edit_sub_category/', views.edit_sub_category, name = 'edit_sub_category'),
    path('edit_sub_category_ajax/', views.edit_sub_category_ajax, name = 'edit_sub_category_ajax'),
    path('delete_multiple_sub_categories/',views.delete_multiple_sub_categories, name ='delete_multiple_sub_categories'),
    path('add_multiple_sub_categories/',views.add_multiple_sub_categories, name = 'add_multiple_sub_categories'),
    #brands
    path('brands/', views.get_all_brands, name = 'brands'),   
    path('add_brand/', views.add_brand, name = 'add_brand'),
    path('delete_brand/', views.delete_brand, name = 'delete_brand_ajax'),
    path('edit_brand/',views.update_brand, name='edit_brand'),
    path('edit_brand_ajax/',views.edit_brand_ajax,name = 'edit_brand_ajax'),
    path('delete_multiple_brands/',views.delete_multiple_brands, name = 'delete_multiple_brands'),
    path('brand_view_ajax/',views.brand_view_ajax, name ='brand_view_ajax'),
    path('add_multiple_brands/',views.add_multiple_brands,name = 'add_multiple_brands'),
    #items
    path('items/',views.get_all_items,name = 'items'),
    path('add_item/',views.add_item, name = 'add_item'),
    path('delete_item/',views.delete_item, name = 'delete_item_ajax'),
    path('edit_item/',views.edit_item,name = 'edit_item'),
    path('edit_item_ajax/', views.edit_item_ajax,name = 'edit_item_ajax'),
    path('delete_multiple_items/',views.delete_multiple_items,name = 'delete_multiple_items'),
    path('item_view_ajax/',views.item_view_ajax,name = 'item_view_ajax'),
    path('add_multiple_items', views.add_multiple_items, name = 'add_multiple_items'),
    path('get_brands_subcategories', views.get_brands_subcategories ,name = 'get_brands_subcategories')
    
    


]



