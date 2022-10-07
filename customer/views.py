from django.contrib import messages
from customer.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from products.models import Product
from .models import OrderItem
from .serializers import *
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import PermissionDenied


class OrderDetailPermissions(BasePermission):

    message = 'You are only allowed access to your personal order items' 

    def has_object_permission(self, request, view, obj):
        
        return obj.ordered_by_user == request.user



class CartDetialPermissions(BasePermission):

    message = 'You are only allowed access to your personal cart' 

    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user

class CartDetail(viewsets.ModelViewSet, CartDetialPermissions):
    """
    Details of an Cart
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CartDetialPermissions]


class OrderItemDetail(viewsets.ModelViewSet, OrderDetailPermissions ):
    """
    Details of an Users Order_items by
    """

    permission_classes = [OrderDetailPermissions]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ProductPermission(BasePermission):

    message = 'You are only allowed to approve an order for your personal product' 

    def has_object_permission(self, request, view, obj):

        if request.methods in SAFE_METHODS:
            return True 

       
        return obj.owner == request.user  


@api_view(['POST'])
def add_to_cart(request, product_id):

    """
    Add an item to user cart/orderitem
    """       
    product = get_object_or_404(Product, product_id=product_id)

    try:
        assert product.product_still_instock() is True
        
        order_item, created=OrderItem.objects.get_or_create(product=product, 
                                                            ordered_by_user=request.user, 
                                                            ordered_status=False)
        
        cart= Cart.objects.filter(user=request.user, cart_checked_out=False).first()
 
        if cart is not None:    
            #checks if the product already exists in the cart
            if cart.orders.filter(product__id=product.id,  ordered_by_user=request.user).first() is not None:
                order_item.quantity += 1
                order_item.save()
                cart.total_update()
                cart.save()  
            else:
                #since product isn't in the cart yet, add it to it 
                print("not yet in cart")
                cart.orders.add(order_item)
                cart.total_update()

                cart.save()                          
        else:
            
            start_date = timezone.now()
            
            cart = Cart(user=request.user, start_date=start_date)
            cart.save()
            cart.orders.add(order_item)
            cart.total_update()
            cart.save()  
        return Response("product %s succesfully added to cart"%(product.product_id))
        
    except AssertionError:
        return Response('%s  is out of stock'%(product.product_id))
    


@api_view(['POST'])
def check_out_cart(request):

    """"
    Checkout  orderif it has been approved for then remove from the cart .
    """
    
    user_cart = Cart.objects.filter(user=request.user.id).first()

    if user_cart is not None:

        if not user_cart.has_object_permission(request, user_cart):
                raise PermissionDenied()
        
        for order_item in user_cart.orders.all():
            
            if order_item.is_approved() is True:
                product=order_item.product
                if  int(order_item.quantity) <  int(product.product_in_stock_count):

                    product.product_in_stock_count -= int(order_item.quantity)
                    product.save()    
                    order_item.delete()    
                    
                else:
                    # for UI
                    # messages.info(request, f"sorry we only have {product.product_in_stock_count} of {product.product_id} available at the moment")
                    pass
            else:
                # for UI 
                # messages.info(request, "%s has not yet been approved for purchase"%(order_item))    
                pass   
            user_cart.total_update()
            user_cart.save()
        return Response("All approved orders were checked out succesfully")
    else:
        return Response('cart does not exist')

 


@api_view(['POST'])
def approve_order(request, order_id):
    
    """
    Approve order by the product owner
    """
    order = OrderItem.objects.get(order_id=order_id)
    if order is not None:
       
        product=order.product
        if not product.has_object_permission(request, product):
            raise PermissionDenied()
           
        if int(product.product_in_stock_count) >= int(order.quantity):
            
            if order.is_approved() is False:
                order.approval_status = 'approved'
                order.save()
                return Response(f"Order {order.order_id} has been approved for purchase ")
            else:
                return Response(f"Order {order.order_id} has already been approved for purchase")
        else:
            return Response(f"Sorry!!! Order {order.order_id} in stock is just {product.product_in_stock_count}  which isn't up to your order quantity")

    else:
        return Response(f'OrderItem with id: {order_id} does not exist currently')


@api_view(['POST'])
def decline_order(request, order_id):
    """
    Decline order by the product owner
    """
    order = OrderItem.objects.filter(order_id=order_id).first() 
    if order is not None:
        product=order.product
        if not product.has_object_permission(request, product):
            raise PermissionDenied()
        
        if order.is_declined() is True:
            
            order.approval_status = 'declined'
            order.save()
            user_cart=Cart.objects.filter(user=order.ordered_by_user.id).first()
            
            user_cart.orders.remove(order)
            
            order.delete()    
        
            return Response(f"Order {order.order_id} was   declined for purchase ")                
        else:
            return Response('order already declined')
    else:
        return Response('order does not exist currently')



@api_view(['POST'])
def quatity_manipulator(request, *args, **kwargs):

    """
    change order quantity
    """
    params=kwargs
    
    order_item=OrderItem.objects.filter(order_id=params['order_id']).first()
    if order_item is not None:

        if not order_item.has_object_permission(request, order_item):
            raise PermissionDenied()

        order_item.change_order_quantity(params['qty'])
        order_item.save()
        return Response('order quantity changed successfully')
     
    return Response('order item does not exist')


@api_view(['POST'])
def clear_cart(request):

    """
    clear all cart items at once
    """
    cart=Cart.objects.filter(user=request.user).first()
    if cart is not None:

        user_orderitem=OrderItem.objects.filter(ordered_by_user=request.user).all()
        if user_orderitem is not None:
            user_orderitem.delete()        
    else:
        return Response("cart does not exist")
    return Response("cart successfully cleared")



@api_view(['POST'])
def remove_order(request, order_id):

    """
    Remove a particular order but only by the product owner
    """ 
    user_orderitem=OrderItem.objects.filter(order_id=order_id).first()
    if user_orderitem is not None: 

        if not user_orderitem.has_object_permission(request, user_orderitem):
                raise PermissionDenied()

        else:
            user_orderitem.delete()
    else:
        return Response(f"This order item does not exist")
    return Response(f"order {user_orderitem.order_id} successfully removed")
    