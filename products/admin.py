from django.contrib import admin
from .models import Category, Product, Colour


admin.site.register(Category)
admin.site.register(Colour)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    save owner as loggedin user from admin panel
    """

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
