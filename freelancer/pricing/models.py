from tkinter.tix import Tree
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class PricingTag(models.Model):
    name = models.CharField(
        max_length=40, 
        verbose_name='اسم تگ',        
    ),
    slug = models.SlugField(
        verbose_name="اسلاگ",
        unique=True
        
    )
    price = models.IntegerField(
        verbose_name='قیمت به ریال',
        default=200000
    )
    
    def __str__(self):
        return self.name
    

class PricingLevel(models.Model):
    
    title = models.CharField(
        max_length=35,
        verbose_name='اسم لول : عادی- برنزی - نقراه ای - طلایی'
    )
    
    count = models.IntegerField(
        default=5,
        verbose_name='تعداد درخواست های این پنل'
    )
    
    day = models.IntegerField(
        verbose_name='تعداد روز های مجاز برای این پنل',
        default=30
    )
    
    discription = models.TextField()
    
    
    price = models.IntegerField(
        verbose_name='قیمت این محصول به ریال'
    )
    
    
class UserLevel(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_level_pricing'
        )
    
    
    level = models.ForeignKey(
        PricingLevel,
        on_delete=models.CASCADE,
        verbose_name='level_pricing'
    ) 
    
    count = models.IntegerField(
        default=0,
        verbose_name='تعداد درخواستای ارسال شده'
    )
     
    
    time_expier = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(30),
        verbose_name='ویژه تا '
        )
    
    
    
    def is_time(self):
        if self.time_expier > timezone.now():
            return True
        return False
        
    def days_left(self):
        #tedad roz baghimande az in pannel
        return (self.time_expier - timezone.now()).days 

    def is_count(self):
        # agar tamom shode darkhastash false mide
        if self.count >= self.level_pricing.count:
            return False
        return True