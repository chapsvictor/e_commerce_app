from customer.models import OrderItem, Cart
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status,generics, permissions
from products.models import Product
from .models import OrderItem
from .serializers import CartSerializer, OrderItemSerializer


class CartDetail(APIView):
    """
    This endpoint is to view the details of a cart
    """


    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.request.user)
            
        return Response(data={'cart_id':cart.id, 
                                'user': cart.user,
                                'cart_checked_out': cart.cart_checked_out,
                                'orders':cart.orders,
                                'start_date': cart.start_date, 
                                'updated_date': cart.updated_date}, status=status.HTTP_200_OK)


class OrderItemDetail(generics.RetrieveAPIView):
    """
    Details of an Users Order_items by
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        order_items = self.queryset.filter(ordered_by_user=self.request.user)
        return order_items


def product_still_instock(product):

    if product.product_in_stock_count >=1:
        return True
    else:
        return False
   

@api_view(['POST'])
def add_to_cart(request, product_id):

    if request.method == 'POST':
        
        product = get_object_or_404(Product, product_id=product_id)
     
        #check if product is still in stock
        if product_still_instock(product) is True:
           

            #the store owner acceptance or denial of order should come here
            
            order_item, created=OrderItem.objects.get_or_create(product=product, ordered_by_user=request.user, ordered_status=False)
            
            cart_qs= Cart.objects.filter(user=request.user, cart_checked_out=False)
            
            if cart_qs.exists():
                cart = cart_qs.first()
                
                #checks if the product already exists in the cart
                if cart.orders.filter(product__id=product.id).exists():
                    
                    order_item.quantity += 1
                    cart.save()
                    order_item.save()
                else:
                    #since product isn't in the cart yet, add it to it 
                    
                    cart.orders.add(order_item)
                    cart.save()
                    order_item.save()
            else:
                
                ordered_date = timezone.now()
                
                cart = Cart.objects.create(user = request.user, ordered_date = ordered_date)
                cart.orders.add(order_item)
            return Response("product %s succesfully added to cart"%(product.product_id))
        
        else:
            return Response('%s  is out of stock'%(product.product_id))
    
    return Response('only post method is allowed')







""""
at checkout of the order has been approved for purchase it is gottten and removed from the cart .
"""
@api_view(['POST'])
def check_out_cart(request):
    print("e enter here")
    if request.method == 'POST':
        user_cart = Cart.objects.filter(user=request.user.id).first()
        
        for order in user_cart.orders.all():
            
            if order.approval_status == 'approved':
                user_order_item=OrderItem.objects.filter(order_id=order.order_id)     
                user_order_item=user_order_item[0]
               
                if  int(user_order_item.quantity) < int(user_order_item.product.product_in_stock_count):
                    product_id=(user_order_item.product.product_id)  
                    product=Product.objects.filter(product_id=product_id)
                    product=product[0]
                    
                    product.product_in_stock_count -= int(user_order_item.quantity)
                    product.save()    
                    user_order_item.delete()    
                    print("%s checked out succesfully"%(order))
                else:
                    print(f"sorry we only have {product.product_in_stock_count} of {product.product_id} available at the moment")
            else:
                user_order_item=OrderItem.objects.filter(order_id=order.order_id)
               
                print("%s has not yet been approved for purchase"%(order))          
        return Response("only approved orders were checked out succesfully")
    
    else:
        return Response('only post method is allowed')
    

@api_view(['POST'])
def approve_order(request, order_id):
    

    if request.method == 'POST':

        order_qs = OrderItem.objects.filter(order_id=order_id)        
        
        if order_qs.exists():
            order=order_qs[0]
            product=order.product
           

            
            if int(product.product_in_stock_count) >= int(order.quantity):
                
                if order.approval_status != 'approved':
                    order.approval_status = 'approved'
                    order.save()
                    return Response(f"Order {order.order_id} has been approved for purchase ")
                else:
                    return Response(f"Order {order.order_id} has already been approved for purchase")

            else:
                return Response(f"Sorry!!! Order {order.order_id} in stock is just {product.product_in_stock_count}  which isn't up to your order quantity")

        else:
            return Response(f'OrderItem with id: {order_id} does not exist currently')
    else:
        return Response('only post method is allowed')



@api_view(['POST'])
def decline_order(request, order_id):

    if request.method == 'POST':
        order_qs = OrderItem.objects.filter(order_id=order_id)
        
        
        if order_qs.exists():
          
            order=order_qs[0]  
            if order.product.owner.id == request.user.id:
                
                if order.approval_status != 'declined':
                    
                    order.approval_status = 'declined'
                    order.save()
                    user_cart=Cart.objects.filter(user=order.ordered_by_user.id)
                   
                    user_cart=user_cart[0]
                   
                    user_cart.orders.remove(order)
            
                    user_order_item=OrderItem.objects.filter(order_id=order.order_id)
                   
                    user_order_item.delete()    
              
                    return Response(f"Order {order.order_id} was   declined for purchase ")                

                else:
                    return Response('order already declined')

            else:
                return Response(f"you are not autorized to approve or decline {order.order_id} for purchase ")
        else:
            return Response('order does not exist currently')
    else:
        return Response('only post method is allowed')



@api_view(['POST'])
def quatity_manipulator(request, *args, **kwargs):
    if request.method == 'POST': 
        params=kwargs
    
        order_item=OrderItem.objects.filter(order_id=params['order_id']).first()
        if order_item.ordered_by_user.id == request.user.id: 
            order_item.change_order_quantity(params['qty'])
            order_item.save()
            return Response('quantity changed successfully')
        else:
            return Response("your aren't authorized successfull")
    else:
        return Response('only post method is allowed')



@api_view(['POST'])
def clear_cart(request):
    user_orderitem=OrderItem.objects.filter(ordered_by_user=request.user).all()
    print(user_orderitem)
    user_orderitem.delete()
    print(user_orderitem)
    return Response("cart successfully cleared")



@api_view(['POST'])
def remove_order(request, order_id): 
    user_orderitem = get_object_or_404(OrderItem, order_id=order_id)         
    user_orderitem.delete()
    return Response(f"order {user_orderitem.order_id} successfully removed")
    