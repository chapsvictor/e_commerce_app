from .models import Coupon
from customer.models import OrderItem, Cart
from rest_framework.response import Response
from rest_framework import status,generics, permissions
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from .serializers import CouponSerializer



def discount_calculator(coupon_id):
    coupon=Coupon.objects.get(coupon_id=coupon_id)
    discount=0
    if coupon.value_type == 'percentage':
        discount=float(coupon.rate)/100
        print(coupon.rate)
        print(f"calculated discuount is {discount}")
    else:
        discount= coupon.rate
        print(f"calculated discuount is {discount}")
    return discount



@api_view(['POST'])
def use_coupon(request, coupon_id, order_id):
    coupon=Coupon.objects.get(coupon_id=coupon_id)
    print(coupon)

    if coupon:
        if coupon.coupon_owner.id == request.user.id:
            order_item=OrderItem.objects.get(order_id=order_id)
            cart_user=Cart.objects.get(user=request.user)

            discount=discount_calculator(coupon_id)
            print(discount)

            if coupon.coupon_type == 'category':
                if coupon.coupon_category.id == order_item.product.category.id:
                    if coupon.value_type == 'percentage':
                                        
                        order_item.coupon_discount_amount = (float(order_item.product.price) * float(order_item.quantity) ) * float(discount)
                        
                        
                        order_item.save()
                        cart_user.save()
                        coupon.delete()
                        return Response(f"You have successfully used this category coupoun {coupon_id}")
                    else:
                        order_item.coupon_discount_amount= float(discount)
                        
                        
                        order_item.save()
                        cart_user.save()
                        coupon.delete()
                        return Response(f"You have successfully used this category coupoun {coupon_id}")
                else:
                    return Response("You cannot use this coupoun for this category")

            
            elif coupon.coupon_type == 'product':
                if coupon.coupon_product.product_id == order_item.product.product_id:
                    if coupon.value_type == 'percentage':
                                        
                        order_item.coupon_discount_amount = (float(order_item.product.price) * float(order_item.quantity)) * float(discount)
                       
                        order_item.save()
                        cart_user.save()
                        coupon.delete()
                        return Response(f"You have successfully used this product coupoun {coupon_id}")

                    else:
                        order_item.coupon_discount_amount= float(discount)
                        
                       
                        order_item.save()
                        cart_user.save()
                        coupon.delete()
                        return Response(f"You have successfully used this coupoun {coupon_id}")
                else:
                    return Response("You cannot use this product coupon for this product")

            else:
                if coupon.value_type == 'percentage':
                                    
                    order_item.coupon_discount_amount = (float(order_item.product.price) * float(order_item.quantity)) * float(discount)
                    
                    
                    order_item.save()
                    cart_user.save()
                    coupon.delete()
                    return Response(f"You have successfully used this coupoun {coupon_id}")

                else:
                    order_item.coupon_discount_amount= float(discount)
                    
                    
                    order_item.save()
                    cart_user.save()
                    coupon.delete()
                    return Response(f"You have successfully used this coupoun {coupon_id}")                
        else:
            return Response('cannot use a coupon that deosn\'t belong to this user')
    else:
        return Response(f'coupon {coupon_id} deosn\'t exist')
        
  

class CouponDetail(ViewSet.ModelViewSet):
    """
    Details of an Coupon
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        coupon = self.queryset.filter(coupon_owner=self.request.user)
        return coupon