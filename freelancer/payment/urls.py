from django.urls import path
from .views import  ZarinpalRequest,ZarinpalVerifi


app_name ='payment'
urlpatterns = [
    path('send/<int:id>', ZarinpalRequest.as_view(), name="send_request" ),    
    path('verify/', ZarinpalVerifi.as_view(), name="verify" ),
]