from django.contrib import admin
from .models import PaymentAccount, PaymentProject


admin.site.register(PaymentProject)

admin.site.register(PaymentAccount)
# Register your models here.
