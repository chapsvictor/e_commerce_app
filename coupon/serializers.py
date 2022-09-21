from django.contrib.auth import get_user_model
from products.serializers import CategorySerializer , ProductsSerializer 
from rest_framework import serializers
from userapp.serializers import UserDetailSerializer
from .models import Coupon


User=get_user_model()


class CouponSerializer(serializers.ModelSerializer):

    """
    Coupon Detail serializer
    """
    coupon_product= ProductsSerializer(read_only=True)
    coupon_category= CategorySerializer(read_only=True)
    coupon_owner = UserDetailSerializer(read_only=True)


    class Meta:
        model=Coupon
        fields = ['coupon_owner', 'coupon_type', 'rate' , 'coupon_category', 'coupon_product', 'coupon_id', 'value_type', 'coupon_used_status']
        depth = 1
