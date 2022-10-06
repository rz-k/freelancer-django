from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.db import models


class Payment(models.Model):
    User = get_user_model()

    user = models.ForeignKey(
        to=User,
        related_name="account_payer",
        on_delete=models.CASCADE,
        verbose_name="پرداخت کننده")

    payment_type = models.ForeignKey(
        to=ContentType,
        related_name="payment_type",
        on_delete=models.CASCADE,
        verbose_name="پرداختی برای")

    payment_object = GenericForeignKey(
        ct_field="payment_type",
        fk_field="object_id")

    authority = models.CharField(
        max_length=120,
        verbose_name="توکن خرید")

    card_pan = models.CharField(
        max_length=30,
        verbose_name="شماره کارت")

    paid = models.BooleanField(
        default=False,
        verbose_name="وضعیت پرداخت")

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ پرداخت")

    object_id = models.PositiveIntegerField(
        null=True,
        verbose_name="ایدی پرداختی مرتبط")

    price = models.IntegerField(verbose_name="مبلغ(ریال)")
    ref_id = models.IntegerField(verbose_name="شماره تراکنش")
    fee = models.IntegerField(verbose_name="کارمزد")

    class Meta:
        verbose_name = "Payments"
        verbose_name_plural = "Payments"

    def __str__(self) -> str:
        return f"{self.payment_type} | {self.user.username}"
