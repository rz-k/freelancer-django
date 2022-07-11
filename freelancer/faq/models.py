from django.db import models
from django_quill.fields import QuillField


class Faq(models.Model):

    question = models.CharField(
        max_length=100,   
        verbose_name='سوال متداول'      
    )
    answer = QuillField(
        max_length=20000,
        verbose_name='جواب سوال متداول')

    position = models.IntegerField(
        unique=True,
        verbose_name='موقعیت سوال'
    )

    def __str__(self) -> str:
        return self.question

