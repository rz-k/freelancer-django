# Generated by Django 4.0.5 on 2022-07-02 10:49

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='experience',
            field=models.CharField(blank=True, default='مهم نیست', max_length=30, null=True, verbose_name='سابقه کار'),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=django_quill.fields.QuillField(max_length=10000, verbose_name='توضیحات پروژه'),
        ),
        migrations.AlterField(
            model_name='job',
            name='price',
            field=models.CharField(max_length=100, verbose_name='بودجه'),
        ),
    ]
