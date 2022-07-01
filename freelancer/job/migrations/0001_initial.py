# Generated by Django 4.0.5 on 2022-07-01 00:53

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields
import freelancer.job.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='عنوان دسته')),
                ('slug', models.CharField(max_length=200, unique=True, verbose_name='آدرس دسته')),
                ('status', models.BooleanField(default=True, verbose_name='فعال شود ؟')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='job.category', verbose_name='زیردسته')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان پروژه')),
                ('company_name', models.CharField(blank=True, default='شخصی', max_length=100, null=True, verbose_name='اسم شرکت')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, default=None, max_length=120, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=15, null=True), blank=True, null=True, size=4, verbose_name='تگ های پروژه')),
                ('description', django_quill.fields.QuillField(max_length=3000, verbose_name='توضیحات پروژه')),
                ('place', models.CharField(max_length=30, verbose_name='مکان')),
                ('work_type', models.CharField(choices=[('تمام وقت', 'full_time'), ('پاره وقت', 'part_time'), ('دور کاری', 'teleworking'), ('کاراموز', 'internship'), ('موقت', 'temporary')], max_length=30, verbose_name='نوع همکاری')),
                ('image', models.ImageField(blank=True, null=True, upload_to=freelancer.job.models.image_job_directory_path, verbose_name='عکس پروژه یا لوگو شرکت')),
                ('status', models.BooleanField(default=False, verbose_name='وضعیت پروژه')),
                ('price', models.BigIntegerField(verbose_name='بودجه')),
                ('created', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_category', to='job.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_job', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accept', 'پذیرفته شد'), ('reject', 'رد شد'), ('wait', 'در حال انتظار')], default='wait', max_length=20, verbose_name='وضعیت درخواست')),
                ('finish_time', models.IntegerField(verbose_name='زمان انجام پروژه')),
                ('created', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applay', to='job.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_applay', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]