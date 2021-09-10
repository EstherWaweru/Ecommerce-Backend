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
    path('edit_category_ajax',views.edit_category_ajax,name="edit_category_ajax"),
    path('delete_multiple_categories',views.delete_multiple_categories,name="delete_multiple_categories"),
    
    
]



