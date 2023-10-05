from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dob = models.DateField()
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    file = models.FileField(upload_to='')

    def __str__(self):
        return self.title
  