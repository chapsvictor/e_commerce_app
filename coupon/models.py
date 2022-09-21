from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from e_commerce.generator import id_generator
from products.models import Product, Category


class Coupon(models.Model):

    COUPON_TYPE = [
            ('category', 'Category'), ('product', 'Product'), ('all', 'All')]

    VALUE_TYPE = [
            ('Percentage', 'percentage'), ('cash', 'Cash')]


    coupon_owner =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coupon_user', blank=False, null=False) 
    coupon_type = models.CharField(max_length=50, choices=COUPON_TYPE, null=False, blank=False)
    rate = models.PositiveIntegerField(_('rate'), default=0)
    coupon_category = models.ForeignKey(Category,related_name='category_coupon', on_delete = models.CASCADE, null=True, blank=True)
    coupon_product = models.ForeignKey(Product, related_name='product_coupon', on_delete = models.CASCADE, null=True, blank=True)
    coupon_id=models.CharField(_('Coupon id'), max_length=20, blank=True)
    coupon_used_status = models.BooleanField(_('Coupon used status'), default=False, max_length=100)
    value_type = models.CharField(_('Value Type '), max_length=255,choices=VALUE_TYPE, default='percentage')



    def __str__(self):
        return '%s '%' of  %s  coupon'%(self.rate, self.coupon_type)



    def save(self, *args, **kwargs):
        if self.coupon_type == 'all':
            self.coupon_category= None
            self.coupon_product= None

        elif self.coupon_type == 'category':
            self.coupon_product= None
            if self.coupon_category is None:
                raise ValueError('category field must be set')

        elif self.coupon_type == 'product':
            self.coupon_category= None
            if self.coupon_product is None:
                raise ValueError('product field must be set')
        if str(self.value_type) == 'percentage' and int(self.rate) > 100:
            raise ValueError("100'%' is the maximum percentage rate")

        if self.coupon_id:
            super().save(*args, **kwargs)
        else:
            self.coupon_id = 'COUP%s'%(id_generator(instance=self))
            super().save(*args, **kwargs)
