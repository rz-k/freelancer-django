from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
    

class UserLevelApplay():
    User = get_user_model()
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_level_applay'
        )
    
    LEVEL = (
        ('عادی','normal'),
        ('برنزی', 'tanned'),
        ('نقرای','silvered'),
        ('طلایی','golded')
    )
    
    level = models.CharField(
        max_length=30, 
        choices=LEVEL,
        verbose_name='level',
        default='normal'
        )
    
    count_normal = models.IntegerField(
        verbose_name='تعداد عادی ماهانه',
        default=5
    )
    
    
    count_pro = models.IntegerField(
        verbose_name='تعداد در صورت خرید',
        default=0
    )
        
        
    time = models.DateTimeField(default=timezone.now, verbose_name='ویژه تا ')
    
    def is_time(self):
        if self.time > timezone.now():
            return True
        return False
        
