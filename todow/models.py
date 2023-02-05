from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=150)
    auther = models.TextField(blank=True)
    important = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    date_complated = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'