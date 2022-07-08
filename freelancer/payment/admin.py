from django.contrib import admin
from .models import PaymentAccount, PaymentJob, PaymentProject

admin.site.register(PaymentJob)

admin.site.register(PaymentProject)

admin.site.register(PaymentAccount)
# Register your models here.
