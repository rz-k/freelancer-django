from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
import uuid

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
    User = get_user_model()

    WORK_TYPE_CHOICES = (
        ('full_time','تمام وقت',),
        ('part_time','پاره وقت'),
        ('teleworking','دور کاری'),
        ('internship','کاراموز'),
        ('temporary','موقت')
    )
    
    MILITARY_SERVICE_STATUS_CHOICES  = (
        ('end_Soldeir','پایان خدمت',),
        ('soldier','در حال انجام'),
        ('exempt','معافیت'),
        ('included','مشمول'),
        ('no_matter','مهم نیست'),
    )

    EDUCATIONAL_LEVEL_CHOICES  = (
        ('no_matter','مهم نیست',),
        ('diploma','دیپلم'),
        ('lisanse','لیسانس'),
        ('mastersdegree','فوق لیسانس'),
        ('phd','دکترا و بالاتر'),
    )

    GENDER_CHOICES  = (
        ('no_matter','مهم نیست'),
        ('man','اقا'),
        ('femail','خانوم'),

    )

    user = models.ForeignKey(
        to=User,
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
            max_length=100,
            blank=True,
            null=True),
        blank=True,
        null=True,
        size=10,
        verbose_name="مهارت های مورد نیاز")
    
    description = QuillField(
        max_length=20000,
        verbose_name='توضیحات جاب')

    place = models.CharField(
        max_length=100,
        verbose_name='مکان')

    work_type = models.CharField(
        max_length=30,
        choices=WORK_TYPE_CHOICES,
        verbose_name='نوع همکاری')

    image = models.ImageField(
        upload_to=image_job_directory_path,
        blank=True,
        null=True,
        verbose_name="عکس پروژه یا لوگو شرکت",)

    experience = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        default="مهم نیست",
        verbose_name="سابقه کار")

    salary = models.CharField(
        max_length=100,
        verbose_name="حقوق در نظر گرفته شده")

    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        verbose_name='جنسیت')

    military_status = models.CharField(
        max_length=30,
        choices=MILITARY_SERVICE_STATUS_CHOICES,
        verbose_name='نظام وظیفه')

    educational_level = models.CharField(
        max_length=30,
        choices=EDUCATIONAL_LEVEL_CHOICES,
        verbose_name='مدرک تحصیلی') 

    status = models.BooleanField(
        default=False,
        verbose_name="وضعیت این اگهی")

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

    uuid = models.UUIDField(default = uuid.uuid4, editable=False, unique=True)

    created = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title

    def get_tags(self):
        return " ,".join(self.tags)


    def save(self, *args, **kwargs):
        """
            Create a new job with a 'Persian' dynamic slug.
        """
        self.slug = slugify(value=self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ApplyJob(models.Model):
    APPLY_STATUS_CHOICES = (
        ('accept', 'پذیرفته شد'),
        ('reject', 'رد شد'),
        ('wait', 'در حال انتظار')
    )

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_job_applay")

    job = models.ForeignKey(
        to=Job,
        on_delete=models.CASCADE,
        related_name="job_applay")

    status = models.CharField(
        max_length=20,
        choices=APPLY_STATUS_CHOICES,
        verbose_name='وضعیت درخواست',
        default='wait')

    created = models.DateTimeField(auto_now=True)
