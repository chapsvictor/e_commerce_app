from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import timezone
from e_commerce.generator import id_generator
from products.models import Product
from products.models import Product


class OrderItem(models.Model):
    STATUS = [
            ('pending', 'Pending Confirmation'), ('approved', 'Approved'), ('declined', 'Declined'), ('customer_cancelled','Customer Cancelled') ]

    ordered_by_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)  
    product = models.ForeignKey(Product, related_name='product_item', on_delete = models.CASCADE)
    order_id=models.CharField(_('order id'), max_length=20, blank=True)
    approval_status = models.CharField(max_length=100, choices=STATUS, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    ordered_status = models.BooleanField(_('status'), default=False, max_length=100)
    total_price = models.PositiveIntegerField (_('Price'), default=0)


    def __str__(self):
        return '%s  of  %s id: %s'%(self.quantity, self.product.name, self.order_id)
    
    
    
    def save(self, *args, **kwargs):
        self.total_price = int(self.quantity) * int(self.product.price) 
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


    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


    def __str__(self):
        return "%s's cart"%(self.user.username)
