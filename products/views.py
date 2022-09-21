from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductsSerializer


User=get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        qs= Category.objects.all()
        return qs

    def retrieve(self, request, *args, **kwargs):
        param=kwargs
        qs = Category.objects.filter(id=param['pk'])
        serializer= CategorySerializer(qs, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        if request.user.is_staff:
            qs = self.get_object()
            qs.delete()
            return Response('Category was successfully deleted')
        return Response('only admin can delete Category')



class ProductViewSet(viewsets.ModelViewSet):

    serializer_class=ProductsSerializer

    def get_queryset(self):
        qs= Product.objects.all()
        return qs


    def retrieve(self, request, *args, **kwargs):
        param=kwargs
        qs = Product.objects.filter(id=param['pk'])
        serializer= ProductsSerializer(qs, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        qs = Product.objects.create(category=Category.objects.get(name=request.data['category']),
        name=request.data['name'],
        description=request.data['description'],
        price=request.data['price'],
        product_in_stock_count=request.data['product_in_stock_count'],
        image=request.data['image'],
        owner=User.objects.get(id=request.user.id)
        
        )
        

        serializer = ProductsSerializer(data = qs, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data)
        return Response(serializer.errors)


    def destroy(self, request, *args, **kwargs):

        """
        Overide destroy method to allow only staffs delete products
        """

        if request.user.is_staff:
            qs = self.get_object()
            qs.delete()
            return Response('Product was successfully deleted')
        return Response('only admin can delete Category')
