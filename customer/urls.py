from django.contrib import admin
from django.urls import path, include
from .views import add_to_cart, approve_order, decline_order, check_out_cart, quatity_manipulator, clear_cart, remove_order, CartDetail,OrderItemDetail
from rest_framework.routers import DefaultRouter

app_name= 'customer'


router=DefaultRouter()
router.register('cart-details', CartDetail, basename='cart_detail_view')
router.register('order-item-details', OrderItemDetail, basename='order_item_detail_view')


urlpatterns = [
    path('add-to-cart/<product_id>/', add_to_cart, name='add-to-cart'),
    path('approve_order/<order_id>/', approve_order, name='approve_order'),
    path('decline_order/<order_id>/', decline_order, name='decline_order'),
    path('check_out_cart/', check_out_cart, name='check_out_cart'),
    path('quatity_manipulator/<order_id>/<qty>/', quatity_manipulator, name='quatity_manipulator'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('remove_order/<order_id>/', remove_order, name='remove_order'),
    path('add-to-cart/<user_id>/', add_to_cart, name='add-to-cart'),
    path('',include(router.urls)),

]