from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import BasePermission, SAFE_METHODS 


User=get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # def get_queryset(self):
    #     qs= Category.objects.all()
    #     return qs

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


class ProductPermission(BasePermission):

    message = 'You are only allowed to approve an order for your personal product' 

    def has_object_permission(self, request, view, obj):

        if request.methods in SAFE_METHODS:
            return True 
        
        return obj.product.owner == request.user  


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class=ProductsSerializer

    def get_queryset(self, *args, **kwargs):
        category=self.request.query_params.get('category')
        colour=self.request.query_params.get('colour')
        print(colour)
        print(category)

        if category and colour:
            print('category and colour')
            qs=Product.objects.filter(category__name=category, colour__name=colour)
        elif category:
            print('only category')
            qs=Product.objects.filter(category__name=category)
          
        else:
            qs= Product.objects.all()

        return qs


    def retrieve(self, request, *args, **kwargs):
        param=kwargs
        qs = Product.objects.filter(id=param['pk'])
        serializer= ProductsSerializer(qs, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):

        qs=Product.objects.create(category=Category.objects.get(name=request.data['category']),
                    name=request.data['name'],
                    description=request.data['description'],
                    price=request.data['price'],
                    product_in_stock_count=request.data['product_in_stock_count'],
                    image=request.data['image'],
                    owner=User.objects.get(id=request.user.id),
                    colour=Colour.objects.get(name=request.data['colour'])
        )
    
        
        # qs = Product(name=request.data['name'],
        #             description=request.data['description'],
        #             price=request.data['price'],
        #             product_in_stock_count=request.data['product_in_stock_count'],
                    
        #             owner=User.objects.get(id=request.user.id)
        # )
        
        # try:
        #     qs.image=request.data['image']
        # except Exception as e:
        #     pass

        # qs.save()
        # category=Category.objects.get(name=request.data['category'])
        
        # qs.category.add(category)
        # qs.save()      

        serializer = ProductsSerializer(data=request.data, many=True)
        
        if serializer.is_valid():
            serializer.save()
    
            return Response(serializer.data)
            
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
