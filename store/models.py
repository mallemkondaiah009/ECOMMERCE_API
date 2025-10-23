from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    product_add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name



