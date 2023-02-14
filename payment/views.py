from django.shortcuts import render
from decouple import config
from rest_framework.decorators import api_view
import razorpay
from rest_framework.response import Response
from account.models import CustomUser
from .models import Payment
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def createOrder(request):
    # global client
    data = request.data

    amount = int(float(data['amount']))
    key_id = config('RAZOR_KEY_ID')
    key_secret = config('RAZOR_SECRET')

    client = razorpay.Client(auth=(key_id, key_secret))

    data = {"amount" : amount, "currency" : "INR"}
    payment = client.order.create(data=data)

    return Response({'order_id': payment['id'], 'amount': payment['amount'], 'currency':payment['currency']})


@api_view(['POST'])
def verifySignature(request):
    res = request.data
    
    key_id = config('RAZOR_KEY_ID')
    key_secret = config('RAZOR_SECRET')
    
    client = razorpay.Client(auth=(key_id, key_secret))
    
    # print(user.email)

    params_dict = {
        'razorpay_payment_id' : res['razorpay_paymentId'],
        'razorpay_order_id' : res['razorpay_orderId'],
        'razorpay_signature' : res['razorpay_signature']
    }

    # verifying the signature
    res = client.utility.verify_payment_signature(params_dict)

    if res == True:
        
        
        ########activating premium in user model ###############
        email = request.data['currentEmail']
        user = CustomUser.objects.filter(email=email).first()
        user.is_premium = True
        user.save()
        
        ####################################################
        payment = Payment.objects.create(
            user=user,
            payment_id = request.data['razorpay_paymentId'],
            payment_method = 'razor pay',
            amount = request.data['amount'],
            status = 'Payment success',
            
        )
        payment.save()
        
        
        return Response({'status':'Payment Successful'}, status=status.HTTP_200_OK)
    return Response({'status':'Payment Failed'})