from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  CategoryViewSet, ProductViewSet



app_name= 'products'


router=DefaultRouter()
router.register('categorys',  CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('',include(router.urls)),
   
]
