from .views import use_coupon
from django.urls import path
from rest_framework.routers import Router



app_name= 'coupon'


urlpatterns = [
    path('use_coupon/<order_id>/<coupon_id>/',use_coupon, name='use_coupon')
]


