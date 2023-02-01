from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer, MyTokenObtainPairSerializer
from .models import CustomUser, UserProfile, employerProfile
from rest_framework.permissions import IsAuthenticated
from .validators import validate_file_extension
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
import stripe
from decouple import config
import razorpay


# Create your views here.






def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)
    confirm_password = data['confirm_password']
    
    
    
    if CustomUser.objects.filter(email=data['email']):
            return Response({'error': 'email id already exist'}, status=status.HTTP_400_BAD_REQUEST)
    

    if user.is_valid():
        
        if not CustomUser.objects.filter(email=data['email']).exists():
            email = data['email']
            username = email.split('@')[0]
            password = data['password']
            
            if password != confirm_password:
                return Response({'error': 'password does not match!'}, status=status.HTTP_400_BAD_REQUEST)

            
            user = CustomUser.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'].lower(),
                username=username,
            )
            
            user.set_password(data['password'])
            user.save()
            
            
            
            if len(data) > 6:
                print("its employer")
                employerprofile = employerProfile()
                user.is_recruiter = True
                user.save()
                
                employerprofile.user = user
                employerprofile.company = data['company']
                employerprofile.designation = data['designation']
                employerprofile.is_recruiter = True
                
                # employerprofile.is_recruiter = True
                employerprofile.uniqueCode = get_random_string(length=25) + get_random_string(length=15)
                employerprofile.save()
            
            
                return Response({'success': 'You Account has been created please wait for admin approvals','username': user.username,}, status=status.HTTP_201_CREATED)
            
            else:
                print("its normal user")
                userprofile = UserProfile()
                userprofile.user = user
                userprofile.save()
                
        
        return Response({
            'success': 'user created successfully'},
            status=status.HTTP_200_OK)
        
@api_view(['POST'])
def VerifyRec(request, id):

    
    rec= get_object_or_404(CustomUser, employerprofile__uniqueCode=id)
    # rec = get_object_or_404
    rec.employerprofile.is_approved = True
    rec.employerprofile.save()  
    

    #mail data to admin for approval
    mail_subject = (f"{{0}} {{1}},Your Recruiter application has been approved").format(rec.first_name, rec.last_name)
    message = render_to_string(
                "account_verification_email.html",
                
            )
    to_email = rec.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.content_subtype = "html"
    send_mail.send()

    rec = UserSerializer(rec, many=False)
 
    return Response(rec.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user)

    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):

    try:
        user = request.user


        data = request.data
        email = data['email']
        username = email.split("@")[0]

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = username
        user.email = email

        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    
    except ValidationError as e:
        return JsonResponse({'error': e.message}, status=400)
    
    



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def uploadResume(request):

    user = request.user

    resume = request.FILES['resume']

    if resume == '':
        return Response({'error': 'please upload your resume'})

    isValidFile = validate_file_extension(resume.name)

    if not isValidFile:
        return Response({'error': 'please upload only pdf file'}, status=status.HTTP_400_BAD_REQUEST)

    user.userprofile.resume = resume
    user.userprofile.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


class GoogleAuthAPIView(APIView):
    def post(self, request):
        print("hello google")
        
        token = request.data['token']
        
        print("this is google token", token)
        
        
            
        
        googleUser = id_token.verify_token(token, GoogleRequest())
        
        
        
        # print(googleUser, "djsfsjd")
        
        
        if not googleUser:
            raise exceptions.AuthenticationFailed('unauthenticated')
        
        user = CustomUser.objects.filter(email = googleUser['email']).first()
        
        if not user:
            email = googleUser['email']
            username = email[0].split('@')[0]
        
            user = CustomUser.objects.create(
                first_name = googleUser['given_name'],
                # last_name = googleUser['family_name'],
                email = googleUser['email'],
                username = username
            )
            
            user.set_password(token)
            user.save()
            
            userprofile = UserProfile.objects.create(
                user = user
            )
            
            userprofile.save()
        token = get_tokens_for_user(user)
        
            
    
        return Response(token)
        
        
    
    
    
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        print(email, "this is email")
        from_email = settings.EMAIL_HOST_USER
        print(from_email)
        
        try:
            user = CustomUser.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Password change request'
            message = render_to_string('forgot-password-email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_mail(mail_subject, message, from_email, [to_email], fail_silently=False)

            return Response(email, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'No account is registered with email id you entered!'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ForgotPasswordVerifyView(APIView):

    def post(self, request):
        print("hello")

        uidb64 = request.data['uid']
        token = request.data['token']
        # print(request.data)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            print("None is working")
            

        if user is not None and default_token_generator.check_token(user, token):
            print("user is working")
            
            # return Response(uid, status=status.HTTP_200_OK)
            return Response(uid, status=status.HTTP_200_OK)
            
        else:
            print("else is working")
            return Response('Verification failed', status=status.HTTP_401_UNAUTHORIZED)
        
        
        
class ResetPasswordAPIView(APIView):
    def post(self, request):
        
        
        uid = request.data['uid']
        password = request.data['password']
        confim_password = request.data['confirmPassword']
        
        
        try:
            if password == confim_password:
                user = CustomUser.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                
                return Response({"success": "Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Password doesnot match"}, status=status.HTTP_400_BAD_REQUEST)
                
                
        except:
            return Response({'error':'Request failed'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        



        
