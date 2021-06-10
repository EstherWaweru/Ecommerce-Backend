from django.db import models
from django.db.models.deletion import CASCADE

# Create your product models here.
class ProductUtils(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(ProductUtils):
    name = models.CharField(unique=True,max_length=255)
    image = models.ImageField()
    
    def __str__(self):
        return self.name

class SubCategory(ProductUtils):
    name = models.CharField(unique=True,max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categories')
    image = models.ImageField()

    def __str__(self):
        return self.name

class Brand(ProductUtils):
    name = models.CharField(unique=True,max_length=255)
    image = models.ImageField()

    def __str__(self) -> str:
        return self.name

class Product(ProductUtils):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField()
    review = models.TextField()
    rating = models.CharField(max_length=255)
    price = models.FloatField()
    discounted_price = models.FloatField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products")
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Variation(ProductUtils):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations")

    def __str__(self):
        return self.name

class ProductVariation(ProductUtils):
    value = models.CharField(max_length=250)#black,small
    image = models.ImageField()
    variation = models.ForeignKey(Variation,on_delete=CASCADE,related_name="product_variations")



    
   
