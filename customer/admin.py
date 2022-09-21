from django.contrib import admin
from .models import Cart, OrderItem 


admin.site.register(Cart)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    save user as logged-in user that is making the order from admin panel
    """

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
