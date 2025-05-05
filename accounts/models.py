from django.db import models

class users(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    school = models.CharField(max_length=20)
    address = models.CharField(max_length=100, default="")

    