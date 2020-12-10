from django.db import models

# Create your models here.
class TesteModel(models.Model):
    fileTest = models.FileField(upload_to='certificates', max_length=254)