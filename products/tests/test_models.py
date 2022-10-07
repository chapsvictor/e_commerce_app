from django.utils.text import slugify
import unittest
from userapp.models import User
from ..models import *


class TestCategory(unittest.TestCase):
    name="testecommerce category"
    slug= slugify(name)
    category=Category.objects.create(name=name, slug=slug)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "testecommerce category")
        self.assertEqual(self.category.slug, "testecommerce-category")
        
        
    category.delete()


class TestProduct(unittest.TestCase):

    email = 'testemail@yahoo.com'
    username = 'testemail'
    first_name = 'testfirstname'
    address="testaddress"
    contact="0903249609"
    password='12345'


    test_user = User.objects.create(email=email,    
                                    username=username, 
                                    first_name=first_name, 
                                    address=address, 
                                    contact=contact, 
                                    password=password
    )

    category_name="testecommerce category"
    slug= slugify(category_name)
    category=Category.objects.create(name=category_name, slug=slug)



    product_name='testproduct'
    product_description='testproductdescription'
    product_price=12000
    product_in_stock_count=4
    product_owner=test_user
    product=Product.objects.create(name=product_name, 
                                description=product_description, 
                                owner=product_owner, 
                                category=category, 
                                price=product_price, 
                                product_in_stock_count=product_in_stock_count
    )

    def test_product_creation(self):
        self.assertEquals(self.product.name, "testproduct")
        self.assertEquals(self.product.category.name, "testecommerce category")
        self.assertEquals(self.product.description, "testproductdescription")
        self.assertEquals(self.product.price, 12000)
        self.assertEquals(self.product.owner.email, "testemail@yahoo.com")
        self.assertEquals(self.product.product_in_stock_count, 4)



    test_user.delete()
    category.delete()
    product.delete()