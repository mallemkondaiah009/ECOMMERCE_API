from django.contrib import admin
from .models import Category, Product, Cart

admin.site.register(Category)

class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price', 'product_add_date']
admin.site.register(Product, AdminProduct)


class AdminCart(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'quantity', 'added_at']
admin.site.register(Cart,AdminCart)



