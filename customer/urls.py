from django.contrib import admin
from django.urls import path, include
from .views import add_to_cart, approve_order, decline_order, check_out_cart, quatity_manipulator, clear_cart, remove_order, CartDetail,OrderItemDetail



app_name= 'customer'


urlpatterns = [
    path('add-to-cart/<product_id>/', add_to_cart, name='add-to-cart'),
    path('approve_order/<order_id>/', approve_order, name='approve_order'),
    path('decline_order/<order_id>/', decline_order, name='decline_order'),
    path('check_out_cart/', check_out_cart, name='check_out_cart'),
    path('quatity_manipulator/<order_id>/<qty>/', quatity_manipulator, name='quatity_manipulator'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('remove_order/<order_id>/', remove_order, name='remove_order'),
    path('Cart-detail/<user_id>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart/<user_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', CartDetail.as_view(), name='cart_details'),
    path('order_item/<order_id>', OrderItemDetail.as_view(), name='order_details'),
]