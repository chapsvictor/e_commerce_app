from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields=['id', 'name', 'slug']
        model = Category
       

class ColourSerializer(serializers.ModelSerializer):

    class Meta:
        fields=['id', 'name']
        model = Colour
       
    
class ProductsSerializer(serializers.ModelSerializer):
    # category=CategorySerializer()

    class Meta:
        model = Product
        fields=['id', 'name', 'description', 'price', 'category','product_in_stock_count', 'image', 'colour']
        

        depth = 1
   