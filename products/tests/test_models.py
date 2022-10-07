from django.utils.text import slugify
import unittest
from django.test import TestCase
from userapp.models import User
from ..models import *


class TestCategory(TestCase):
    def setUp(self):

        self.name="testecommerce category"
        self.slug= slugify(self.name)
        self.category=Category.objects.create(name=self.name, slug=self.slug)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "testecommerce category")
        self.assertEqual(self.category.slug, "testecommerce-category")
        
        
class TestColour(TestCase):
    def setUp(self):

        self.name="testcolour"
       

    def test_colour_creation(self):
        colour=Colour.objects.create(name=self.name)

        self.assertEqual(colour.name, "testcolour")
            

class TestProduct(TestCase):

    def setUp(self):

        self.email = 'testemail@yahoo.com'
        self.username = 'testemail'
        self.first_name = 'testfirstname'
        self.address = "testaddress"
        self.contact = "0903249609"
        self.password ='12345'

        self.category_name = "testecommerce category"
        self.colour = "testcolour"


    
    def test_product_creation(self):
        test_user = User.objects.create(email=self.email,    
                                    username=self.username, 
                                    first_name=self.first_name, 
                                    address=self.address, 
                                    contact=self.contact, 
                                    password=self.password
        )
        slug= slugify(self.category_name)
        category=Category.objects.create(name=self.category_name, slug=slug)
        colour=Colour.objects.create(name=self.colour)

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
                                    product_in_stock_count=product_in_stock_count,
                                    colour=colour
        )

        self.assertEquals(product.name, "testproduct")
        self.assertEquals(product.category.name, "testecommerce category")
        self.assertEquals(product.description, "testproductdescription")
        self.assertEquals(product.price, 12000)
        self.assertEquals(product.owner.email, "testemail@yahoo.com")
        self.assertEquals(product.product_in_stock_count, 4)
        self.assertEquals(product.colour, colour)



   