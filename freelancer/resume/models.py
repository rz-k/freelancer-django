import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()



def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class CV(models.Model):
    GENDER = (
        ("مرد","man"),
        ("زن","female"),
    )

    MARITAL = (
        ("متاهل","married"),
        ("مجرد","single"),
    )

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_cv")

    title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="عنوان و سمت")

    skills = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="مهارت ها")

    country = models.CharField(
        max_length=50, 
        null=True,
        blank=True,
        verbose_name="کشور")

    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="شهر")

    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاریخ تولد")
    
    gender = models.CharField(
        max_length=50,
        choices=GENDER,
        blank=True,
        null=True,
        verbose_name="جنسیت")

    marital_status = models.CharField(
        max_length=50,
        choices=MARITAL,
        blank=True,
        null=True,
        verbose_name="وضعیت تاهل",)

    languages = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="زبان ها")
    
    def __str__(self):
        return self.user.email


class WorkExperience(models.Model):
    cv = models.ForeignKey(
        to=CV,
        on_delete=models.CASCADE,
        related_name="cv_experience"
    )

    position = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="پست یا سمت شما")

    location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="ادرس")

    start_year = models.IntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
        verbose_name="تاریخ شروع به کار")

    end_year = models.PositiveIntegerField(
        default=current_year(), 
        validators=[MinValueValidator(1984), max_value_current_year],
        verbose_name="تاریخ پایان کار")


class Education(models.Model):
    cv = models.ForeignKey(
        to=CV,
        on_delete=models.CASCADE,
        related_name="cv_education")

    evidence = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="مدارک")

    location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="مکان")

    start_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
        verbose_name="تاریخ شروع آموزش")

    end_year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1984), max_value_current_year],
        verbose_name="تاریخ پایان آموزش")


class Contact(models.Model):
    cv = models.ForeignKey(
        to=CV,
        on_delete=models.CASCADE,
        related_name="cv_contact")

    image = models.CharField(
        blank=True,
        null=True,
        max_length=150,
        verbose_name="لینک ایکن")

    link = models.CharField(
        max_length=150,
        verbose_name="لینک پروفایل کاربری در شبکه اجتماعی")