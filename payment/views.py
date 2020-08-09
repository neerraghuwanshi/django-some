from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payment import Checksum

from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from payment.models import Betting
from .serializers import BettingSerializer

MERCHANT_KEY = 'Your Key'

# Create your views here.

class BettingListView(ListCreateAPIView):
    queryset = Betting.objects.all()
    serializer_class = BettingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user, checksum="9090")

    # data_dict = {
    #         'MID':'Your Id',
    #         'ORDER_ID':'1',
    #         'TXN_AMOUNT':'500',
    #         'CUST_ID':'acfff@paytm.com',
    #         'INDUSTRY_TYPE_ID':'Retail',
    #         'WEBSITE':'WEBSTAGING',
    #         'CHANNEL_ID':'WEB',
	#         'CALLBACK_URL':'http://127.0.0.1:8000/handlepayment',
    #     }
    # data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict,MERCHANT_KEY)
    # print(data_dict['CHECKSUMHASH'])
    #post this to https://securegw-stage.paytm.in/order/process for development

@csrf_exempt
def handlePayment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order unsuccessful because"+response_dict['RESPMSG'])
    else: 
        print("order unsuccessful because"+response_dict['RESPMSG'])

    return HttpResponse('done')
