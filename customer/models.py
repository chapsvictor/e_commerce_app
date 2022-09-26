from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from e_commerce.generator import id_generator
from products.models import Product
from products.models import Product



class OrderItem(models.Model):

    """
    Order model for products that are being ordered at a particular time
    """
    STATUS = [
            ('pending', 'Pending Confirmation'), ('approved', 'Approved'), ('declined', 'Declined'), ('customer_cancelled','Customer Cancelled') ]

    ordered_by_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)  
    product = models.ForeignKey(Product, related_name='product_item', on_delete = models.CASCADE)
    order_id=models.CharField(_('order id'), max_length=20, blank=True)
    approval_status = models.CharField(max_length=100, choices=STATUS, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    ordered_status = models.BooleanField(_('status'), default=False, max_length=100)
    total_quantity_price = models.PositiveIntegerField (_('Order Cost'), default=0)
    coupon_discount_amount = models.PositiveIntegerField (_('Coupon Discount  Amount '), default=0)
    payment_price = models.PositiveIntegerField (_('Order Total Amount'), default=0)


    def __str__(self):
        return '%s  of  %s id: %s'%(self.quantity, self.product.name, self.order_id)
    
    
    
    def save(self, *args, **kwargs):
        self.total_quantity_price = float(self.quantity) * float(self.product.price) 
        self.payment_price = float(self.total_quantity_price) - float(self.coupon_discount_amount)
        if self.order_id:
            super().save(*args, **kwargs)
        else:
            self.order_id = 'ORD%s'%(id_generator(instance=self))
            super().save(*args, **kwargs)

    
    def change_order_quantity(self, qty):
        self.quantity = int(qty)
        return self.quantity


    def is_approved(self):
        if self.approval_status == 'approved':
            return True
        else:
            return False

    def approve_order(self):
        self.approval_status == 'approved'
        return self.approval_status

    def is_declined(self):
        if self.approval_status == 'declined':
            return True
        else:
            return False

    def has_object_permission(self, request, obj ):

        if obj.ordered_by_user == request.user:
            return True
    
    @property
    def get_order_items(self):
        return ", ".join([item.product.name for item in self.cart_items.all()])

    
class Cart(models.Model):    

    """
    Individaul user cart model
    """
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_cart') 
    cart_checked_out= models.BooleanField(verbose_name=_('checked_out') , default=False)
    
    orders = models.ManyToManyField(OrderItem, blank=True)
    start_date=models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)
    check_out_total=models.PositiveIntegerField(default=0)
    total_payment_price=models.PositiveIntegerField (_('Cart Total Amount'), default=0)


    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


    def __str__(self):
        return "%s's cart"%(self.user.username)


    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
       

    def total_update(self):
        self.total_payment_price = 0
        for order in self.orders.all():
            self.total_payment_price += order.payment_price
        # super().save()
        return self.total_payment_price


    def has_object_permission(self, request, obj ):

        if obj.user == request.user:
            return True