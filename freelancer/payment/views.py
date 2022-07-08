import json
from tkinter.messagebox import NO
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PaymentAccount, PaymentJob, PaymentProject
from freelancer.job.models import Job
from freelancer.project.models import Project
from django.conf import settings


class ZarinpalInfo:
    amount = "1000"
    mobile = "phone"
    description = "description"

    zarinpal_merchant = settings.MERCHANT
    zarinpal_api_request = "https://api.zarinpal.com/pg/v4/payment/request.json"
    zarinpal_api_verify = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    zarinpal_api_startpay = "https://www.zarinpal.com/pg/StartPay/{authority}"
    zarinpal_callback = settings.BASE_SITE_URL+'/pay/verify/'
    zarinpal_headers = {
        "accept": "application/json",
        "content-type": "application/json'"}

    zarinpal_send_data = {
        "merchant_id": zarinpal_merchant,
        "description": description,
        "callback_url": zarinpal_callback,
        "amount": amount,
        "metadata": {"mobile": mobile, "email": ""}}


class ZarinpalSendPayRequest(LoginRequiredMixin,View, ZarinpalInfo):
    def get(self, request, uuid):
        # job , project = None
        print(uuid)
        project = None
        job = Job.objects.filter(user=request.user,uuid=uuid).first()
        if not job:
            project = Project.objects.filter(user=request.user,uuid=uuid).first()
            
        

        print(job)
        print(project)
        print("="*100)

        data = self.zarinpal_send_data
        data["amount"] = self.amount
        data["metadata"]["email"] = request.user.email
        print(data)
        #=> send information
        response = self.send_information(data=data)
        print(response)
        #=> validate response
        if response['errors']:
            return JsonResponse({
                "error_status_code": response['errors']['code'],
                "error_message": response['errors']['message']})
        else:
            #=> Create a successful payment for the job.
            authority = response['data']['authority']
            success_url = self.zarinpal_api_startpay.format(authority=authority)
            print(success_url)
            if project:
                payment = PaymentProject(
                    user=request.user,
                    project=project,
                    price=self.amount,
                    authority=authority).save()
            else:
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

        payjob, payproj = None

        payjob = PaymentJob.objects.filter(authority=authority).first()
        if not payjob:
            payproj = PaymentProject.objects.filter(authority=authority).first()

        if status == 'ok':
            if payjob:
                data = {
                    "merchant_id": self.zarinpal_merchant,
                    "amount": payjob.price,
                    "authority": authority
                }
            else:
                data = {
                    "merchant_id": self.zarinpal_merchant,
                    "amount": payproj.price,
                    "authority": authority
                }




            response = requests.post(
                url=self.zarinpal_api_verify,
                data=json.dumps(data),
                headers=self.zarinpal_headers
            ).json()


            if payjob:
                self.handel_verify_response(request, response=response, payment=payjob, authority=authority)
            else:
                self.handel_verify_response(request,response=response, payment=payproj, authority=authority)
        else:
            context = {
                "message": "تراکنش با خطا مواجه شده است",
                "authority": authority
            }
            return render(request=request,
                template_name=self.error_template_name, context={"result": context})


    def handel_verify_response(self,request,  response: "json", payment, authority: str):
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
