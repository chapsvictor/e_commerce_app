from rest_framework import serializers
from .models import Category, Product



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields=['id', 'name']
        model = Category
       

    

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        fields=['id', 'name', 'description', 'price', 'category','product_in_stock_count', 'image' ]
        model = Product

        depth = 1