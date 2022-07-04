import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import PaymentAccount, PaymentJob


class ZarinpalInfo:
    amount = "1000"
    mobile = "phone"
    description = "description"

    zarinpal_merchant = settings.MERCHANT
    zarinpal_api_request = "https://api.zarinpal.com/pg/v4/payment/request.json"
    zarinpal_api_verify = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    zarinpal_api_startpay = "https://www.zarinpal.com/pg/StartPay/{authority}"
    zarinpal_callback = 'https://ce96-154-6-16-197.ngrok.io/pay/verify/'
    zarinpal_headers = {
        "accept": "application/json",
        "content-type": "application/json'"}

    zarinpal_send_data = {
        "merchant_id": zarinpal_merchant,
        "description": description,
        "callback_url": zarinpal_callback,
        "amount": "",
        "metadata": {"mobile": mobile, "email": ""}}


class ZarinpalSendPayRequest(View, ZarinpalInfo):
    def get(self, request, id):
        job = get_object_or_404(klass=Job, user=request.user, id=id)
        
        #=> Pack the data.
        data = self.zarinpal_send_data
        data["amount"] = self.amount
        data["metadata"]["email"] = request.user.email

        #=> send information
        response = self.send_information(data=data)

        #=> validate response
        if response['errors']:
            return JsonResponse({
                "error_status_code": response['errors']['code'],
                "error_message": response['errors']['message']})
        else:
            #=> Create a successful payment for the job.
            authority = response['data']['authority']
            success_url = self.zarinpal_api_startpay.format(authority=authority)
            payment = PaymentJob(
                user=request.user,
                job=job,
                price=self.amount,
                authority=authority).save()

            return redirect(success_url)


    def send_information(self, data):
        """Send ``zarinpal`` information and return the response.
        """
        data = json.dumps(data)
        response = requests.post(
            url=self.zarinpal_api_request,
            data=data,
            headers=self.zarinpal_headers
        ).json()

        return response


    def post(self, request, id, success_url="job:home"):
        return redirect(success_url)



class ZarinpalVerify(View, ZarinpalInfo):
    error_template_name = "payment/error.html"
    success_template_name = "payment/success.html"

    def get(self , request):
        status = request.GET.get("Status").lower()
        authority = request.GET["Authority"]
        payment = PaymentJob.objects.get(authority=authority)

        if status == 'ok':
            data = {
                "merchant_id": self.zarinpal_merchant,
                "amount": payment.price,
                "authority": authority
            }
            response = requests.post(
                url=self.zarinpal_api_verify,
                data=json.dumps(data),
                headers=self.zarinpal_headers
            ).json()
            self.handel_verify_response(response=response, payment=payment, authority=authority)

        else:
            context = {
                "message": "تراکنش با خطا مواجه شده است",
                "authority": authority
            }
            return render(request=request,
                template_name=self.error_template_name, context={"result": context})


    def handel_verify_response(self, response: "json", payment: [PaymentAccount, PaymentJob], authority: str):
        """Handel the success verification responses and errors.
        
        Response Status Code:
            100:
                Code 100 that means the transaction is successful.

            101 and *:
                Code 101 that means the transaction was successful and
                was verified once before, and this is the second time.
        """
        if response['errors']:
            error_code = response['errors']['code']
            error_message = response['errors']['message']
            context = {
                'message': error_message,
                'authority': authority
            }
            return render(request=request,
                template_name=self.error_template_name, context={"result": context})

        else:
            status_code = response['data']['code']
            if status_code == 100:
                payment.payed = True
                payment.job.payed = True
                payment.job.save()
                payment.save()

                context = {
                    'authority': authority,
                    'price' : payment.price,
                    'email': payment.user.email
                }
                return render(request=request,
                    template_name=self.success_template_name, context={"result": context})

            elif status_code == 101:
                context = {
                    'message': response['data']['message'],
                    'authority': authority
                }
                return render(request=request,
                    template_name=self.error_template_name, context={"result": context})

            else:
                context = {
                    'message': response['data']['message'],
                    'authority': authority
                }
                return render(request=request,
                    template_name=self.error_template_name, context={"result": context})
