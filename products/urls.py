from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  CategoryViewSet, ProductViewSet



app_name= 'products'


router=DefaultRouter()
router.register('category',  CategoryViewSet, basename='category_view')
router.register('product', ProductViewSet, basename='product_view')

urlpatterns = [
    path('',include(router.urls)),
   
]