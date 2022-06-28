from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


def avatar_directory_path(instance, filename: str) -> "File Path":
    """"
    File location to store user avatars.
    
    Returns:
        file_path: str
    """
    path = 'users/{0}/profile/{1}'
    return path.format(instance.user.id, filename)


def cv_directory_path(instance, filename: str) -> "File Path":
    """
    File location to store user CV/Resume.
    
    Returns:
        file-path: str
    """
    path = 'users/{0}/cv/{1}'
    return path.format(instance.user.id, filename)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="ایمیل")
    
    phone = models.IntegerField(
        blank=True, null=True,
        verbose_name='شماره تلفن کاربر')
    
    score = models.IntegerField(
        default=0,
        verbose_name='امتیاز کاربر')
    


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile')
    
    bio = models.TextField(        
        null=True,
        blank=True)
    
    avatar = models.ImageField(
        upload_to=avatar_directory_path,
        null=True,
        blank=True)
    
    skills = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="مهارت ها")
    
    approved = models.BooleanField(
        default=False,
        verbose_name='کاربر تایید شده توسط سایت')
    
    cv = models.FileField(
        upload_to=cv_directory_path,
        null=True,
        blank=True)


    def __str__(self):        
        return self.user.username
