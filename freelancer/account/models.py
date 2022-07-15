from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_directory_path(instance, filename: str) -> "File Path":
    """"
    File location to store user avatars.
    
    Returns:
        file_path: str
    """
    path = 'users/{0}/profile/{1}'
    return path.format(instance.user.id, "avatar.jpg")


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="ایمیل")
    
    phone = models.CharField(
        max_length=11,
        blank=True, null=True,
        verbose_name='شماره تلفن کاربر')
    
    score = models.IntegerField(
        default=0,
        verbose_name='امتیاز کاربر')
    
    
    balance = models.IntegerField(
        default=0,
        verbose_name='میزان حساب کاربر (ریال)')

    def get_avatar(self):
        """
            This function returns the avatar of the user profile if it exists,
            otherwise return a default avatar.
        """
        avatar = self.user_profile.avatar
        if avatar:
            return avatar.url
        else:
            return "/media/users/default/profile/default-avatar.jpg"


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        primary_key=True)
    
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیحات پروفایل")

    avatar = models.ImageField(
        upload_to=avatar_directory_path,
        null=True,
        blank=True,
        verbose_name="عکس پروفایل")
    
    approved = models.BooleanField(
        default=False,
        verbose_name='کاربر تایید شده توسط سایت')

    def __str__(self):
        return self.user.username
