from django.db import models
from accounts.models import users

class Notes(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Untitled")
    timeStamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Pages(models.Model):
    noteBook = models.ForeignKey(Notes, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Untitled")

    def __str__(self):
        return self.title

class Block(models.Model): 
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.page.title