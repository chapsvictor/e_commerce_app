from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from e_commerce.generator import id_generator
from products.models import Product
from products.models import Product
from coupon.models import Coupon


class OrderItem(models.Model):
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

    
    
    @property
    def get_order_items(self):
        return ", ".join([item.product.name for item in self.cart_items.all()])

    




class Cart(models.Model):    
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_cart') 
    cart_checked_out= models.BooleanField(verbose_name=_('checked_out') , default=False)
    
    orders = models.ManyToManyField(OrderItem, )
    start_date=models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)
    check_out_total=models.PositiveIntegerField(default=0)
    Total_payment_price=models.PositiveIntegerField (_('Cart Total Amount'), default=0)


    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


    def __str__(self):
        return "%s's cart"%(self.user.username)


    def save(self, *args, **kwargs):
        self.Total_payment_price=0
        for order in self.orders.all():
            self.Total_payment_price += float(order.payment_price)
        super().save(*args, **kwargs)

