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
            # self.slug = slugify(self.name)
            # self.name= self.name.lower()
            super().save(*args, **kwargs)


   

    def __str__(self):
        return '%s category'%(self.name)


    @staticmethod
    def get_all_categories():
        return Category.objects.all()


@receiver(pre_save, sender=Category)
def slug_creator(sender, **kwargs):
    category=kwargs['instance']
    slug = category.slug
    category.name = category.name.lower()
    name=category.name
    if slug is None:
        category.slug = slugify(name)


class Product(models.Model):

    """
    Product model for all items 
    """
    name=models.CharField(max_length=200, blank=False)
    description=models.TextField(max_length=200, blank=False)
    price=models.IntegerField()
    is_instock = models.BooleanField(_('in stock?'), default=True)
    product_in_stock_count=models.IntegerField(_('stock count'),default=0)
    category=models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='media/products/', blank=True , null=True)
    date_created=models.DateField(auto_now_add=True)
    product_id=models.CharField(max_length=50, blank=True, null=True)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return '%s  id: %s'%(self.name, self.product_id)
          


    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)


    # @staticmethod
    # def get_products_by_id(product_id):
    #     return Product.objects.filter(id=product_id)

    # @staticmethod
    # def get_all_products():
    #     return Product.objects.all()

    # @staticmethod
    # def get_products_by_category_id(category_id):
    #     if category_id:
    #         return Product.objects.filter(category=category_id)
    #     else:
    #         return Product.get_all_products()
    
    # @staticmethod
    # def get_products_by_category_name(category_name):
    #     if category_name:
    #         return Product.objects.filter(category=category_name)
    #     else:
    #         return Product.get_all_products()


    def get_image_url(self):
            if self.image:
                return self.image.url
            else:
                return ''

    def product_still_instock(self):

        """
        Check if product is still in stock
        """

        if self.product_in_stock_count >=1:
            return True
        else:
            return False


    def has_object_permission(self, request, obj ):

        if obj.owner == request.user:
            return True
  

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering=['-date_created']


@receiver(pre_save, sender=Product)
def product_id_setter(sender, **kwargs):
    product = kwargs['instance']
    product_id = product.product_id
    name = product.name

    if product_id is None:
        product.product_id = '%s_%s'%(name, id_generator(instance = product))
        