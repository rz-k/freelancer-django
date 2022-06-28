from django.db import models
from account.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


def image_job_directory_path(instance, filename: str) -> "File Path":
    """
    File location to store user Job.
    
    Returns:
        file-path: str
    """
    path = 'users/{0}/job/{1}'
    return path.format(instance.user.id, filename)

class Category(models.Model):
    parrent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True,verbose_name='زیردسته', related_name='childernt')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته')
    slug = models.CharField(max_length=200, unique=True, verbose_name='آدرس دسته')
    status = models.BooleanField(default=True, verbose_name='فعال شود ؟')
    position = models.IntegerField(verbose_name='پوزیشن',unique=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['position']

    def __str__(self) -> str:
        return self.title





class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_job")
    title = models.CharField(max_length=100, verbose_name="تایتل")
    slug = models.SlugField(max_length=120,default="no-slug",blank=True, null=True, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='job_category')
    tag = ArrayField( models.CharField(max_length=20,blank=True,null=True),
            blank=True,
            null=True,
            size=3,
            verbose_name="تگ های پروژه")
    description = models.TextField(verbose_name='توضیحات پروژه', max_length=250)
    price = models.BigIntegerField(verbose_name="بودجه")
    image = models.ImageField(verbose_name="عکس پروژه", upload_to=image_job_directory_path, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="انجام شده ؟")


    def save(self, *args, **kwargs):
        self.slug = slugify(self.job_title, allow_unicode=True)
        super(Job, self).save(*args, **kwargs)


class ApplayJob(models.Model):
    HHOISES = (
        ('accept', 'پذیرفته شد ✅'),
        ('reject', 'رد شد ❌'),
        ('wait', 'در حال انتظار ⌛️')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_applay")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_applay")
    created = models.DateTimeField(auto_now=True)
    finish_time = models.IntegerField(verbose_name="زمان انجام پروژه")
    status = models.CharField(choices=HHOISES, verbose_name='وضعیت درخواست', default='wait')