from django.contrib import admin
from .models import RazorpayPayment
class AdminRazorpayPayment(admin.ModelAdmin):
    list_display = ['id', 'product', 'user','amount', 'status']

admin.site.register(RazorpayPayment, AdminRazorpayPayment)