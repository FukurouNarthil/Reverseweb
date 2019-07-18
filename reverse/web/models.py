from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)

class document(models.Model):
    filename = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField()
    document = models.FileField(upload_to='documents/')