from django.db import models
from django.contrib.auth import get_user_model
from e_commerce.generator import id_generator
from django.utils.translation import gettext as _

User=get_user_model()

class  Category(models.Model):
    name=models.CharField(max_length=200, blank=False, unique=True)


    def save(self,*args, **kwargs):
            self.name= self.name.lower()
            super().save(*args, **kwargs)


    def __str__(self):
        return '%s category'%(self.name)


    @staticmethod
    def get_all_categories():
        return Category.objects.all()



class Product(models.Model):
    name=models.CharField(max_length=200, blank=False)
    description=models.TextField(max_length=200, blank=False)
    price=models.IntegerField()
    is_instock = models.BooleanField(_('in stock?'), default=True)
    product_in_stock_count=models.IntegerField(_('stock count'),default=0)
    category=models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='media/products/', blank=True , null=True)
    date_created=models.DateField(auto_now_add=True)
    product_id=models.CharField(max_length=50, blank=True)
    owner=models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    


    def save(self,*args, **kwargs):
        if not self.product_id:
            self.product_id = '%s_%s'%(self.name,id_generator(instance=self))
            
        super().save(*args, **kwargs)




    @staticmethod
    def get_products_by_id(product_id):
        return Product.objects.filter(id=product_id)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
    
    @staticmethod
    def get_products_by_category_name(category_name):
        if category_name:
            return Product.objects.filter(category=category_name)
        else:
            return Product.get_all_products()


    def get_image_url(self):
            if self.image:
                return self.image.url
            else:
                return ''



    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering=['-date_created']


    def __str__(self):
        return '%s  id: %s'%(self.name, self.product_id)
        