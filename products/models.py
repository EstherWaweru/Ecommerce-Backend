from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import  slugify

# Create your product models here.
class ProductUtil(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(ProductUtil):
    name = models.CharField(unique=True,max_length=255)
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    image = models.ImageField(upload_to='media/products')
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super().save(*args, **kwargs)


class SubCategory(ProductUtil):
    name = models.CharField(unique=True,max_length=255)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categories')
    image = models.ImageField(upload_to='media/products')

    def __str__(self):
        return self.name

class Brand(ProductUtil):
    name = models.CharField(unique=True,max_length=255)
    image = models.ImageField(upload_to='media/products')

    def __str__(self) -> str:
        return self.name

class Item(ProductUtil):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/products')
    description = models.TextField()
    review = models.TextField()
    rating = models.CharField(max_length=255)
    price = models.FloatField()
    discounted_price = models.FloatField()
    brands = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products")
    subcategories = models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    


class Variation(ProductUtil):
    name = models.CharField(max_length=255)
    items = models.ForeignKey(Item,on_delete=models.CASCADE,related_name="variations")

    @property
    def get_item_variations(self):
        total_list=ItemVariation.objects.filter(variations=self)
        return total_list.count()

    def __str__(self):
        return self.name

class ItemVariation(ProductUtil):
    value = models.CharField(max_length=250)#black,small
    image = models.ImageField(upload_to='media/products')
    variations = models.ForeignKey(Variation,on_delete=CASCADE,related_name="item_variations")



    
   
