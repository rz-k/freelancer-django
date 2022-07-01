from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField


def image_job_directory_path(instance, filename: str) -> "File Path":
    """
    The file location where the logo or photo of the job should be stored. 
    
    Returns:
        file-path: str
    """
    path = 'users/{0}/job/{1}'
    return path.format(instance.user.id, filename)


class Category(models.Model):
    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        verbose_name='زیردسته',
        related_name='children')
    
    name = models.CharField(
        max_length=200,
        verbose_name='عنوان دسته')
    
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='آدرس دسته')
    
    status = models.BooleanField(
        default=True,
        verbose_name='فعال شود ؟')
    
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name


class Job(models.Model):
    WORK_TYPE = (
        ('تمام وقت', 'full_time'),
        ('پاره وقت','part_time'),
        ('دور کاری','teleworking'),
        ('کاراموز','internship'),
        ('موقت','temporary')
    )
    
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_job")
    
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='job_category')

    title = models.CharField(
        max_length=100,
        verbose_name="عنوان پروژه")

    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="اسم شرکت",
        default="شخصی",)
    
    slug = models.SlugField(
        max_length=120,
        blank=True,
        null=True,
        default=None,
        allow_unicode=True)
    
    tags= ArrayField(
        models.CharField(
            max_length=15,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=4,
        verbose_name="تگ های پروژه")
    
    description = QuillField(
        max_length=3000,
        verbose_name='توضیحات پروژه')

    place = models.CharField(
        max_length=30,
        verbose_name='مکان')

    work_type = models.CharField(
        max_length=30,
        choices=WORK_TYPE,
        verbose_name='نوع همکاری')

    image = models.ImageField(
        upload_to=image_job_directory_path,
        blank=True,
        null=True,
        verbose_name="عکس پروژه یا لوگو شرکت",)

    status = models.BooleanField(
        default=False,
        verbose_name="وضعیت پروژه")

    price = models.BigIntegerField(verbose_name="بودجه")
    created = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title


    def save(self, *args, **kwargs):
        """
            Create a new job with a 'Persian' dynamic slug.
        """
        self.slug = slugify(value=self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Apply(models.Model):
    APPLY_STATUS = (
        ('accept', 'پذیرفته شد'),
        ('reject', 'رد شد'),
        ('wait', 'در حال انتظار')
    )
    
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_applay")
    
    job = models.ForeignKey(
        to=Job,
        on_delete=models.CASCADE,
        related_name="job_applay")
    
    status = models.CharField(
        max_length=20,
        choices=APPLY_STATUS,
        verbose_name='وضعیت درخواست',
        default='wait')
    
    finish_time = models.IntegerField(verbose_name="زمان انجام پروژه")
    created = models.DateTimeField(auto_now=True)


    def get_job_title(self):
        return self.job.slug
