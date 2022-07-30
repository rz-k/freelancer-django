# Generated by Django 4.0.5 on 2022-07-30 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_alter_applyproject_project_alter_applyproject_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='متن پیام')),
                ('created', models.DateTimeField(auto_now=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('apply_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation', to='project.applyproject', verbose_name='پروژه مربوط به پیام')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_conversation', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده پیام')),
            ],
        ),
        migrations.DeleteModel(
            name='ConversationMessage',
        ),
    ]
