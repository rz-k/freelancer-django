from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class PricingTag(models.Model):
    """
    The price of the dynamic fields
    that are determined when the project is created,
    such as 'urgent', 'highlight' and 'private'
    """
    name = models.CharField(
        max_length=40, 
        verbose_name="اسم تگ")

    price = models.IntegerField(
        verbose_name='قیمت به ریال',
        default=200000)

    def __str__(self):
        return self.name


class PricingPanel(models.Model):
    panel_type = models.CharField(
        max_length=150,
        verbose_name="نوع پنل(برنزی، نقره ای، طلایی، الماس)")

    price = models.PositiveIntegerField(
        verbose_name="قیمت محصول به ریال")

    count = models.PositiveSmallIntegerField(
        default=5,
        verbose_name="تعداد پیشنهاد های ارسالی در ماه")

    days = models.IntegerField(
        verbose_name="تعداد روز های مجاز",
        default=30)

    position = models.PositiveSmallIntegerField(
        verbose_name="موقعیت و جایگاه این پنل در بین پنل ها",
        unique=True)

    discription = models.TextField()


class ActivePricingPanel(models.Model):
    User = get_user_model()

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="user_pricing_panel")

    active_panel = models.ForeignKey(
        PricingLevel,
        on_delete=models.CASCADE,
        verbose_name="active_pricing_panel")

    count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="تعداد پیشنهاد های ارسال شده")

    expire_time = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(30),
        verbose_name="تاریخ انقضای پنل")


    def is_expire(self) -> bool:
        """
        Check expiration date of the panel,
        return True if panel is available, otherwise False
        """
        if self.expire_time > timezone.now():
            return True
        return False

    def days_left(self) -> int:
        """
        Get the remaining days of the active pricing panel
        """
        return (self.timeex - timezone.now()).days

    def has_apply(self) -> bool:
        """
        Check to see if the user has enough apply count or not.
        """
        if self.count >= self.active_panel.count:
            return False
        return True