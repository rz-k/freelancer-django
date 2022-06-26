from email.policy import default
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

def avatar_directory_path(instance, filename):
    return 'users/{0}/profile/{1}'.format(instance.user.id, filename)

def cv_directory_path(instance, filename):
    return 'users/{0}/cv/{1}'.format(instance.user.id, filename)

class User(AbstractUser):

    email = models.EmailField(max_length=100,unique=True,verbose_name="ایمیل")
    phone = models.IntegerField(verbose_name='شماره تلفن کاربر')
    score = models.IntegerField(default=0,verbose_name='امتیاز کاربر')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'username']

class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(null=True, blank=True, max_length=155)
    avatar = models.ImageField(upload_to=avatar_directory_path, null=True, blank=True)
    skills = ArrayField(
        ArrayField(
            models.CharField(max_length=20, blank=True, null=True),
            size=10,
        ),
        size=10,
    )
    approved = models.BooleanField(default=False, verbose_name='کاربر تایید شده توسط سایت')
    cv = models.FileField(upload_to=cv_directory_path, )