from django.test import TestCase,Client
from django.urls import reverse
from django.utils import timezone
import django
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_backend.settings.travis")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_backend.settings.dev")
django.setup()

from products.models import Brand, Category, Item, ItemVariation, ProductUtil, SubCategory, Variation

# Create your model tests here.

class ProductUtilTest(TestCase):
    
    def setUp(self):
        self.client=Client()
        self.productUtil= ProductUtil.objects.create(created_at=timezone.now,updated_at=timezone.now)
    
    def test_productUtil_creation(self):
        self.assertTrue(isinstance(self.productUtil, ProductUtil))
       
        #testing how many times the database is called
        # with self.assertNumQueries(6):
        #         response = self.client.get(reverse("trucks:list_trucks"))

        # self.assertEqual(response.context["trucks_list"], 1)


class CategoryTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Electronicssss")
    
    def test_category_creation(self):
        self.assertTrue(isinstance(self.category,Category))
        self.assertEqual(self.category.__str__(),self.category.name)
        self.assertEqual(self.category.slug,"electronicssss")

class SubCategoryTest(TestCase):

    def setUp(self):
        self.category =Category.objects.create(name="Electroni")
        self.subcategory = SubCategory.objects.create(name="Phones",categories=self.category)
    
    def test_subcategory_creation(self):
        self.assertTrue(isinstance(self.subcategory,SubCategory))
        self.assertEqual(self.subcategory.__str__(),self.subcategory.name)

class BrandTest(TestCase):
    
    def setUp(self):
        self.brand=Brand.objects.create(name="Samsung",image="Heye")
    
    def test_brand_creation(self):
        self.assertTrue(isinstance(self.brand,Brand))
        self.assertEqual(self.brand.__str__(),self.brand.name)

class ItemTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.category=Category.objects.create(name="Elecronics")
        cls.subcategory=SubCategory.objects.create(name="Sasung",categories=cls.category)
        cls.brand = Brand.objects.create(name="Sasun")
        cls.item = Item.objects.create(name="Galaxy 5",subcategories=cls.subcategory,brands=cls.brand,price=10000,discounted_price=5000)
    
    def test_item_creation(self):
        self.assertTrue(isinstance(self.item,Item))
        self.assertEqual(self.item.__str__(),self.item.name)


class VariationTest(TestCase):
    @classmethod
    def setUp(cls):
        
        cls.category=Category.objects.create(name="Electnics")
        cls.subcategory=SubCategory.objects.create(name="Samsung",categories=cls.category)
        cls.brand = Brand.objects.create(name="Samsun")
        cls.item = Item.objects.create(name="Galaxy 5",subcategories=cls.subcategory,brands=cls.brand,price=10000,discounted_price=5000)
        cls.variation = Variation.objects.create(name="Color",items=cls.item)
        cls.item_variation = ItemVariation.objects.create(value="red",variations=cls.variation)
        cls.item_variation1 = ItemVariation.objects.create(value="blue",variations=cls.variation)
        cls.item_variation2 = ItemVariation.objects.create(value="black",variations=cls.variation)
        cls.item_variation3 = ItemVariation.objects.create(value="yellow",variations=cls.variation)
        
    def test_variation_creation(self):
        self.assertTrue(isinstance(self.variation,Variation))
        self.assertEqual(self.variation.__str__(),self.variation.name)
    
    def test_total_variations(self):
        self.assertEqual(self.variation.get_item_variations,4)



class ItemVariationTest(TestCase):
    
    @classmethod
    def setUp(cls):
        
        cls.category=Category.objects.create(name="Electonics")
        cls.subcategory=SubCategory.objects.create(name="Samsungss",categories=cls.category)
        cls.brand = Brand.objects.create(name="Samsuns")
        cls.item = Item.objects.create(name="Galaxy 5",subcategories=cls.subcategory,brands=cls.brand,price=10000,discounted_price=5000)
        cls.variation = Variation.objects.create(name="Color",items=cls.item)
        cls.item_variation = ItemVariation.objects.create(value="red",variations=cls.variation)
        cls.item_variation1 = ItemVariation.objects.create(value="blue",variations=cls.variation)
        cls.item_variation2 = ItemVariation.objects.create(value="black",variations=cls.variation)
        cls.item_variation3 = ItemVariation.objects.create(value="yellow",variations=cls.variation)

    
    def test_item_vation_creation(self):
        self.assertTrue(isinstance(self.item_variation,ItemVariation))
    
class CategoryTe(TestCase):
    
    def setUp(self):
        self.category = Category(name="Eectronicssss")
    
    def test_category_creation(self):
        self.assertEqual(self.category.name,"Eectronicssss")
        self.assertTrue(isinstance(self.category,Category))
        self.assertEqual(self.category.__str__(),self.category.name)
        # self.assertEqual(self.category.slug,"Eectronicssss")
        
    
