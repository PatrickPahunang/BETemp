from django.contrib.auth.models import AbstractUser, Permission , Group
from django.db import models
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True ,)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='', null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_set', blank=True
    )

    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

