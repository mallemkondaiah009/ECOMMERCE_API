from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10)
    email = models.EmailField(max_length=15)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username
