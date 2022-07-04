import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views import View
from freelancer.job.models import Job
from freelancer.payment.models import PaymentAccount, PaymentJob
import json

class ZarinpalInfo:
    MERCHANT = settings.MERCHANT
    ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
    # ZP_CALLBACK = f'https://gray-city.ir/pay/verify/'
    ZP_CALLBACK = f'https://ce96-154-6-16-197.ngrok.io/pay/verify/'
    HEADERS = {
            "accept": "application/json",
            "content-type": "application/json'"
            }


class ZarinpalRequest(View, ZarinpalInfo):

    def get(self, request, id):
        job = get_object_or_404(Job, user=request.user, id=id)
        self.amount = "1000"
        self.description = "description"
        self.email = request.user.email
        self.mobile = "phone"
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": self.amount,
            "callback_url": ZarinpalInfo.ZP_CALLBACK,
            "description": self.description,
            "metadata": {"mobile": self.mobile, "email": self.email}
        }
        req = requests.post(url=ZarinpalInfo.ZP_API_REQUEST, data=json.dumps(
            req_data), headers=ZarinpalInfo.HEADERS)
        
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            pay = PaymentJob(user=request.user,job=job, price=self.amount, authority=authority)
            pay.save()
            return redirect(ZarinpalInfo.ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"ارور کد: {e_code}, ارور مسیج: {e_message}")

    def post(self, request, id):
        return redirect('job:home')


class ZarinpalVerifi(View, ZarinpalInfo):

    def get(self , request):       
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        pay = PaymentJob.objects.get(authority=t_authority)
        
        if request.GET.get('Status') == 'OK':
            req_data = {
                "merchant_id": ZarinpalInfo.MERCHANT,
                "amount": pay.price,
                "authority": t_authority
            }

            req = requests.post(url=ZarinpalInfo.ZP_API_VERIFY, data=json.dumps(req_data), headers=ZarinpalInfo.HEADERS)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    pay.payed =True
                    pay.job.payed=True
                    pay.job.save()
                    pay.save()
                    
                    res = {
                        'authority':t_authority,
                        'price' : pay.price,
                        'email':pay.user.email
                    }

                    return render(request, 'payment/success.html', {'result':res})

                elif t_status == 101:
                    res = {
                        'message': str(req.json()['data']['message']) ,
                        "authority": t_authority
                    }

                    return render(request, 'payment/error.html', {'result':res})
                else:
                    res = {
                        'message': str(req.json()['data']['message']),
                        "authority": t_authority
                     }
                    return render(request, 'payment/error.html', {'result':res})
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                res = {
                    'message': str(e_message),
                    "authority": t_authority
                    }
                return render(request, 'payment/error.html', {'result':res})
        else:
            res = {
                    'message': "تراکنش با خطا مواجه شده است",
                    "authority": t_authority
                    }
            return render(request, 'payment/error.html', {'result':res})


# def sh(request):
#     return render(request , 'zarinpal/success.html')
