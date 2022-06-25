from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):

#     email = models.EmailField(
#         max_length=100,
#         unique=True,
#         verbose_name="ایمیل")

#     privilege = models.IntegerField(
#         default=0,
#         verbose_name='امتیاز کاربر')

#     user_pro = models.BooleanField(
#         default=False,
#         verbose_name='کاربر ویژه')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['last_name', 'username']