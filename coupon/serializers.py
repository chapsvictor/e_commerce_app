from rest_framework import serializers
from .models import Coupon
from products.serializers import CategorySerializer , ProductsSerializer 
from userapp.serializers import UserDetailSerializer




class CouponSerializer(serializers.ModelSerializer):
    product= ProductsSerializer(read_only=True, many=True)
    Category= CategorySerializer(read_only=True, many=True)
    coupon_owner = UserDetailSerializer(read_only=True, many=True)


    class Meta:
        model=Coupon
        fields = ['coupon_owner', 'coupon_type', 'rate' , 'coupon_category',  'product' , 'coupon_id', 'value_type','coupon_used_status']
        depth = 1

