from django.db import models
from django.contrib.auth import get_user_model
from freelancer.project.models import Project


class PaymentAccount(models.Model):
    User = get_user_model()

    user = models.ForeignKey(
        to=User,
        related_name='user_account_pay',
        on_delete=models.CASCADE,
        verbose_name='پرداخت کننده')

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ پرداخت')

    authority = models.CharField(
        max_length=120,
        verbose_name='توکن خرید')

    payed = models.BooleanField(
        default=False,
        verbose_name='پرداخت شده ؟')

    price = models.IntegerField(verbose_name='مبلغ(ریال)')


    class Meta:
        verbose_name = 'User Payment'
        verbose_name_plural = 'User Payments'

    def __str__(self) -> str:
        return str(self.user)


class PaymentProject(models.Model):
    User = get_user_model()

    user = models.ForeignKey(
        to=User,
        related_name='user_project_pay',
        on_delete=models.CASCADE,
        verbose_name='پرداخت کننده')

    project = models.ForeignKey(
        to=Project,
        related_name='project_pay',
        on_delete=models.CASCADE,
        verbose_name='پروژه')

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ پرداخت')

    authority = models.CharField(
        max_length=120,
        verbose_name='توکن خرید')

    paid = models.BooleanField(
        default=False,
        verbose_name='پرداخت شده ؟')

    price = models.IntegerField(verbose_name='مبلغ(ریال)')


    class Meta:
        verbose_name = 'Project Payment'
        verbose_name_plural = "Projects Payments"

    def __str__(self) -> str:
        return str(self.project)
