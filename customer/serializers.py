from products.serializers import ProductsSerializer 
from rest_framework import serializers 
from userapp.serializers import UserDetailSerializer
from .models import Cart, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    """
    OrderItem Detail serializer
    """
    product= ProductsSerializer(read_only=True)
    ordered_by_user = UserDetailSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields = ['id','order_id', 'product','approval_status', 'ordered_status', 'quantity', 'ordered_by_user']

        read_only_fields = ('approval_status', 'ordered_status','ordered_by_user','product' )

        depth = 1


class CartSerializer(serializers.ModelSerializer):

    """
    Cart Detail serializer
    """
    user = UserDetailSerializer(read_only=True)
    orders = OrderItemSerializer(read_only=True)

    class Meta:
        model=Cart
        fields = ['id', 'user', 'cart_checked_out', 'orders', 'start_date', 'updated_date', 'check_out_total']

        read_only_fields = ('cart_checked_out', 'check_out_total','user' )
        depth = 1
