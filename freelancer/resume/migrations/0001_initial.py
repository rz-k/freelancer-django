# Generated by Django 4.0.5 on 2022-07-05 13:01

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import freelancer.resume.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, max_length=350, null=True, verbose_name='توصیف خود در چند خط')),
                ('skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, null=True), blank=True, null=True, size=10, verbose_name='مهارت ها')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='کشور')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='شهر')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.CharField(blank=True, choices=[('مرد', 'man'), ('زن', 'female')], max_length=50, null=True, verbose_name='جنسیت')),
                ('marital_status', models.CharField(blank=True, choices=[('متاهل', 'married'), ('مجرد', 'single')], max_length=50, null=True, verbose_name='وضعیت تاهل')),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, null=True), blank=True, null=True, size=10, verbose_name='زبان ها')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_cv', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=50, null=True, verbose_name='پست یا سمت شما')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='ادرس')),
                ('start_year', models.IntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), freelancer.resume.models.max_value_current_year], verbose_name='تاریخ شروع به کار')),
                ('end_year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), freelancer.resume.models.max_value_current_year], verbose_name='تاریخ پایان کار')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cv_experience', to='resume.cv')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidence', models.CharField(blank=True, max_length=50, null=True, verbose_name='مدارک')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='مکان')),
                ('start_year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), freelancer.resume.models.max_value_current_year], verbose_name='تاریخ شروع آموزش')),
                ('end_year', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1984), freelancer.resume.models.max_value_current_year], verbose_name='تاریخ پایان آموزش')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cv_education', to='resume.cv')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=150, null=True, verbose_name='لینک ایکن')),
                ('link', models.CharField(max_length=150, verbose_name='لینک پروفایل کاربری در شبکه اجتماعی')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cv_contact', to='resume.cv')),
            ],
        ),
    ]
