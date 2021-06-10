from django.test import TestCase
from django.utils import timezone
from products.models import Category, ProductUtil

# Create your model tests here.

class ProductUtilTest(TestCase):
    
    def setUp(self):
        self.productUtil= ProductUtil.objects.create(created_at=timezone.now,updated_at=timezone.now)
    
    def test_productUtil_creation(self):
        self.assertTrue(isinstance(self.productUtil, ProductUtil))
        # self.assertEqual(self.productUtil.__s__(), self.productUtil.name)

class CategoryTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
    
    def test_category_creation(self):
        self.assertTrue(isinstance(self.category,Category))
        self.assertEqual(self.category.__str__(),self.category.name)
        self.assertEquals(self.category.slug,"electronics")
