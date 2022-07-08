from django.urls import path
from .views import  ZarinpalSendPayRequest, ZarinpalVerify


app_name ='payment'

urlpatterns = [
    path('send/<uuid:uuid>', ZarinpalSendPayRequest.as_view(), name="send_request"),
    path('verify/', ZarinpalVerify.as_view(), name="verify"),
]