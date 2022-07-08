from django.contrib.auth import get_user_model
from django.db import models
from freelancer.job.models import Job
from freelancer.project.models import Project


class PaymentAccount(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='پرداخت کننده', related_name='user_account_pay')
    price = models.IntegerField(verbose_name='مبلغ(ریال)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    authority = models.CharField(max_length=120,verbose_name='توکن خرید')
    payed = models.BooleanField(default=False, verbose_name='پرداخت شده ؟')

    class Meta:
        verbose_name = 'User Payment'
        verbose_name_plural = 'User Payments'

    def __str__(self) -> str:
        return str(self.user)


class PaymentJob(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='پرداخت کننده', related_name='user_job_pay')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='جاب', related_name='job_pay')
    price = models.IntegerField(verbose_name='مبلغ(ریال)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    authority = models.CharField(max_length=120,verbose_name='توکن خرید')
    payed = models.BooleanField(default=False, verbose_name='پرداخت شده ؟')
    
    
    class Meta:
        verbose_name = 'Job Payment'
        verbose_name_plural = "Job Payments"

    def __str__(self) -> str:
        return str(self.job)


class PaymentProject(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='پرداخت کننده', related_name='user_project_pay')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='پروژه', related_name='project_pay')
    price = models.IntegerField(verbose_name='مبلغ(ریال)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    authority = models.CharField(max_length=120,verbose_name='توکن خرید')
    payed = models.BooleanField(default=False, verbose_name='پرداخت شده ؟')
    
    
    class Meta:
        verbose_name = 'Project Payment'
        verbose_name_plural = "Projects Payments"

    def __str__(self) -> str:
        return str(self.project)