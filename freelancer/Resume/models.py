from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()





class CV(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_cv')

    country = models.CharField(
        max_length=50, 
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=50, 
        null=True,
        blank=True
    )

    birthday = models.DateField(
        verbose_name='تاریخ تولد',
        blank=True,
        null=True,
)

    GENDER = (
        ('مرد','man'),
        ('زن','Female'),
    )
    gender = models.CharField(
        choices=GENDER,
        blank=True,
        null=True,

    )

    MARITAL = (
        ('مرد','man'),
        ('زن','Female'),
    )

    marital_status = models.CharField(
        choices=MARITAL,
        blank=True,
        null=True,
    )

    languages = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="زبان ها")

    skills = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="مهارت ها")


    