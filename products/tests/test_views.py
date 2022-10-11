from django.utils.text import slugify
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate
from ..models import * 
from ..serializers import *
from ..views import *


class TestProductView(APITestCase):

    def setUp(self):
        self.email = 'testemail@yahoo.com'
        self.username = 'testemail'
        self.first_name = 'testfirstname'
        self.address = "testaddress"
        self.contact = "0903249609"
        self.password ='12345'

        self.category_name = "testecommerce category"
        self.colour = "testcolour"

        self.test_user = User.objects.create(email=self.email,    
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
        product_owner=self.test_user
        self.product=Product.objects.create(name=product_name, 
                                    description=product_description, 
                                    owner=product_owner, 
                                    category=category, 
                                    price=product_price, 
                                    product_in_stock_count=product_in_stock_count,
                                    colour=colour
        )
       

    def test_list_products(self):
        
        response =  self.client.get(reverse('products:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(ProductsSerializer(instance=self.product).data, response.data)
        

    def test_get_specific_product(self):
        response =  self.client.get(reverse('products:product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        
    def test_add_product(self):
        category_name = "testecommerce category2"
        colour_name = "testcolour2"
        slug= slugify(category_name)
        category=Category.objects.create(name=category_name, slug=slug)
       
        colour=Colour.objects.create(name=colour_name)

        product ={
                    'name':'testproduct',
                    'description':'testproductdescription',
                    'price':12000,
                    'product_in_stock_count':4,
                    'owner':self.test_user,
                    'colour':'testcolour2',
                    'category': "testecommerce category2",
                    'image':''
                    
        }
        
        self.client.force_authenticate(user=self.test_user)
        
        response = self.client.post(reverse('products:product-list'), product)
       
        self.assertEqual(response.status_code, 200)
    