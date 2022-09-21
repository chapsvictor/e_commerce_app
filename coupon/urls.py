from .views import use_coupon
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponDetailViewSet


router=DefaultRouter()
router.register('coupon-details', CouponDetailViewSet, basename='coupon_view')


app_name= 'coupon'


urlpatterns = [
    path('use_coupon/<order_id>/<coupon_id>/',use_coupon, name='use_coupon'),
    path('',include(router.urls)),
]


