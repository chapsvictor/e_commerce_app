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
        fields=['id', 'name', 'description', 'price', 'category','product_in_stock_count', 'image', 'colour']
        model = Product

        depth = 1
        