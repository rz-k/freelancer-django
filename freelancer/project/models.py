from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from freelancer.job.models import Category


class Project(models.Model):
    User = get_user_model()

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_project")
    
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='category_project')

    title = models.CharField(
        max_length=60,
        verbose_name="عنوان پروژه")
        
    slug = models.SlugField(
        max_length=120,
        blank=True,
        null=True,
        default=None,
        allow_unicode=True)

    tags = ArrayField(
        models.CharField(
            max_length=30,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=5,
        verbose_name="تگ های پروژه")

    description = models.TextField(
        max_length=500,
        verbose_name='توضیحات برای کارفرما')

    status = models.BooleanField(
        default=False,
        verbose_name="وضعیت تموم شدن پروژه")

    budget = models.CharField(
        max_length=100,
        verbose_name="بودجه")

    urgent = models.BooleanField(
        default=False,
        verbose_name="فوری")

    highlight = models.BooleanField(
        default=False,
        verbose_name="برجسته")
    
    private = models.BooleanField(
        default=False,
        verbose_name="محرمانه")

    paid = models.BooleanField(
        default=False,
        verbose_name="پرداخت شده؟")

    created = models.DateTimeField(auto_now=True)


    def str(self) -> str:
        return self.title



class ApplyProject(models.Model):

    APPLY_STATUS_CHOICES = (
        ('accept', 'پذیرفته شد'),
        ('reject', 'رد شد'),
        ('wait', 'در حال انتظار')
    )

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_project_applay")

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project_applay")

    status = models.CharField(
        max_length=20,
        choices=APPLY_STATUS_CHOICES,
        verbose_name='وضعیت درخواست',
        default='wait')

    description = models.TextField(
        max_length=500,
        verbose_name='توضیحات برای کارفرما')

    bid_amount = models.CharField(
        max_length=100,
        default=0,
        verbose_name="مبلغ پیشنهادی")

    bid_date = models.IntegerField(
        default=0,
        verbose_name="زمان انجام پروژه")

    created = models.DateTimeField(auto_now=True)
