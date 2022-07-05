from random import choice
from tabnanny import verbose
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


class WorkExperience(models.Model):
    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='education_cv'
    )    

    position = models.CharField(
        max_length=50, 
        verbose_name='پست یا سمت شما'
    )
    
    location = models.CharField(
        max_length=50, 
    )

    start_year = models.IntegerChoices(
        choices= [(i, i) for i in range(1330, 1402)],
    )
    end_year = models.IntegerChoices(
        choices= [(i, i) for i in range(1330, 1402)],
    )


class Education(models.Model):
    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='education_cv'
    )    

    evidence = models.CharField(
        max_length=50, 
    )

    location = models.CharField(
        max_length=50, 
    )
    start_year = models.IntegerChoices(
        choices= [(i, i) for i in range(1330, 1402)],
    )
    end_year = models.IntegerChoices(
        choices= [(i, i) for i in range(1330, 1402)],
    )

class Contact(models.Model):
    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='contact_cv'
    )

    image = models.CharField(
        max_length=150,
    )

    link = models.CharField(
        max_length=150,
    )