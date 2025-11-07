from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username
