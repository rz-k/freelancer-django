from django.contrib import admin
from .models import PaymentAccount, PaymentJob

admin.site.register(PaymentJob)
admin.site.register(PaymentAccount)
# Register your models here.
