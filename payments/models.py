# from django.db import models
# from store.models import Product
# from accounts.models import User

# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('paid', 'Paid'),
#         ('failed', 'Failed'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE,)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    
#     # Razorpay details
#     razorpay_order_id = models.CharField(max_length=100, blank=True)
#     razorpay_payment_id = models.CharField(max_length=100, blank=True)
#     razorpay_signature = models.CharField(max_length=200, blank=True)
    
#     # Order details
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.product.name} - {self.status}"
    
#     class Meta:
#         ordering = ['-created_at']
