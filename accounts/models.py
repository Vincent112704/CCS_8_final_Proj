from django.db import models

class userAccount(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
