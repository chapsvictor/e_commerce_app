from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.dispatch import receiver
from e_commerce.generator import id_generator



class  Category(models.Model):

    """
    Category model to allow all products take a single category at a time
    """
    name=models.CharField(max_length=200, blank=False, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)


    def save(self,*args, **kwargs):
        if self.slug is None:
            self.category.slug = slugify(self.name)
        super().save(*args, **kwargs)


   

    def __str__(self):
        return '%s category'%(self.name)


class Colour(models.Model):

    name=models.CharField(max_length=200, blank=True, unique=True)


    def save(self, *args, **kwargs):
        self.name=self.name.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        return 'colour %s '%(self.name)


class Product(models.Model):

    """
    Product model for all items 
    """
    name=models.CharField(max_length=200, blank=False)
    description=models.TextField(max_length=200, blank=False)
    price=models.IntegerField()
    is_instock = models.BooleanField(_('in stock?'), default=True)
    product_in_stock_count=models.IntegerField(_('stock count'),default=0)
    category=models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, blank=False, null=False, default='')
    image = models.ImageField(upload_to='media/products/', blank=True , null=True)
    date_created=models.DateField(auto_now_add=True)
    product_id=models.CharField(max_length=50, blank=True, null=True)
    colour=models.ForeignKey(Colour, related_name='colour', on_delete=models.CASCADE, default='')
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    


    def save(self,*args, **kwargs):
        if self.product_id is None:
            self.product_id = '%s_%s'%(self.name, id_generator(instance = self))
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s  id: %s'%(self.name, self.product_id)
          


    def product_still_instock(self):

        """
        Check if product is still in stock
        """
        return self.product_in_stock_count >=1


    def has_object_permission(self, request, obj ):
            return obj.owner == request.user
  

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering=['-date_created']







# @receiver(pre_save, sender=Category)
# def slug_creator(sender, **kwargs):
#     category=kwargs['instance']
#     slug = category.slug
#     category.name = category.name.lower()
#     name=category.name
#     if slug is None:
#         category.slug = slugify(name)



# @receiver(pre_save, sender=Product)
# def product_id_setter(sender, **kwargs):
#     product = kwargs['instance']
#     product_id = product.product_id
#     name = product.name

#     if product_id is None:
#         product.product_id = '%s_%s'%(name, id_generator(instance = product))
        