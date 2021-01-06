import os

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return 'Id: ' + str(self.pk) + ' - ' + self.name




class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Override this method to save with titlecase and lowercase
        self.email = self.email.lower()
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        return super(CustomUser, self).save(*args, **kwargs)


class Certificate(models.Model):
    certificateTitle = models.CharField(max_length=254)
    certificate = models.FileField(upload_to='certificates', max_length=254)
    date = models.DateField()
    update_date = models.DateField(auto_now=True)
    #person = models.ForeignKey("Person", on_delete=models.CASCADE,related_name="certificates")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="user")

    def __str__(self):
        return str(self.certificate)

    def _delete_file(path):
        """ Deletes file from filesystem. """
        if os.path.isfile(path):
            os.remove(path)

    @property
    def fullName(self):
        return 'Stringteste' + self.certificateTitle

