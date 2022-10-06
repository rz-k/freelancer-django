from django.db import models
from django_quill.fields import QuillField


class Faq(models.Model):
    question = models.CharField(
        max_length=2000,
        verbose_name="متن سوال")

    answer = QuillField(
        max_length=20000,
        verbose_name="جواب سوال")

    position = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="یک عدد صحیح برای مرتب کردن سوال در میان سایر سوالات")

    def __str__(self) -> str:
        return self.question