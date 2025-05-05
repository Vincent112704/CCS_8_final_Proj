from django.db import models


# Create your models here.
class ChatHistory(models.Model):
    user_input = models.TextField()
    llm_output = models.TextField()

    def __str__(self):
        return f"ChatHistory(user_input={self.user_input}, llm_output={self.llm_output})"