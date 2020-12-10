import os

from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return 'Id: ' + str(self.pk) + ' - ' + self.name

class Certificate(models.Model):
    certificateTitle = models.CharField(max_length=254)
    certificate = models.FileField(upload_to='certificates', max_length=254)
    date = models.DateField()
    update_date = models.DateField(auto_now=True)
    person = models.ForeignKey("Person", on_delete=models.CASCADE,related_name="certificates")

    def __str__(self):
        return str(self.certificate)

    def _delete_file(path):
        """ Deletes file from filesystem. """
        if os.path.isfile(path):
            os.remove(path)

