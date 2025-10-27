from django.contrib import admin
from .models import Category, Product, Cart

admin.site.register(Category)
admin.site.register(Product)


class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']
admin.site.register(Cart,AdminCart)
