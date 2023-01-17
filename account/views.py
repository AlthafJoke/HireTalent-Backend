from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from .models import CustomUser, UserProfile, reset
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
import random
import string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


# Create your views here.

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)
    confirm_password = data['confirm_password']

    if user.is_valid():
        if not CustomUser.objects.filter(username=data['email']).exists():
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
                #
                user.userprofile.company = data['company']
                user.userprofile.designation = data['designation']
                user.userprofile.is_recruiter = True
                user.userprofile.uniqueCode = get_random_string(
                    length=25) + get_random_string(length=15)
                user.userprofile.save()

                # mail for empl

                mail_subject = "New Recruiter Registered"
                message = 'pls click this to verify http://localhost:3000/verify/' + str(user.userprofile.uniqueCode)
                to_email = "althafav7@gmail.com"
                send_mail = EmailMessage(mail_subject, message, to=[to_email])
                # send_mail.content_subtype = "html"
                send_mail.send()

                return Response({'success': 'You Account has been created please wait for admin approvals', 'username': user.username, }, status=status.HTTP_201_CREATED)

        return Response({
            'success': 'user created successfully'},
            status=status.HTTP_200_OK)


@api_view(['POST'])
def VerifyRec(request, id):

    rec = get_object_or_404(CustomUser, userprofile__uniqueCode=id)
    # rec = get_object_or_404
    rec.userprofile.is_approved = True
    rec.userprofile.save()

    # mail data to admin for approval
    mail_subject = (f"{{0}} {{1}},Your Recruiter application has been approved").format(
        rec.first_name, rec.last_name)
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

        token = request.data['token']

        googleUser = id_token.verify_token(token, GoogleRequest())

        if not googleUser:
            raise exceptions.AuthenticationFailed('unauthenticated')

        user = CustomUser.objects.filter(email=googleUser['email']).first()

        if not user:
            email = googleUser['email']
            username = email[0].split('@')[0]

            user = CustomUser.objects.create(
                first_name=googleUser['given_name'],
                # last_name = googleUser['family_name'],
                email=googleUser['email'],
                username=username
            )

            user.set_password(token)
            user.save()

        token = get_tokens_for_user(user)

        return Response(token)


# class resetPasswordRequestAPIView(APIView):
#     def post(self,request):
#         data = request.data

#         print(data, 'reset pass is working')

#         email = data['email']

#         if not CustomUser.objects.filter(email=data['email']).exists():

#             return Response({"error" : "There is no account with this email address"}, status=status.HTTP_404_NOT_FOUND)

#         user = get_object_or_404(CustomUser,email=email)

#         if user:
#             mail_subject = "Reset your password"
#             current_site = get_current_site(request)
#             # message = 'pls click this to verify http://localhost:3000/resetPassword/' + str(user.id)
#             message = render_to_string('forgot-password-email.html',{
#                 'user' : user,
#                 'domain' : current_site,
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_mail = EmailMessage(mail_subject, message, to=[to_email])
#             # send_mail.content_subtype = "html"
#             send_mail.send()


#         print(user.password, "this is user matching with email")

#         return Response({"success": "email send successfully"})


# class resetPasswordAPIView(APIView):
#     def post(self, request):
#         rec= get_object_or_404(CustomUser, id=id)
#         rec = UserSerializer(rec, many=False)


#         return Response(rec.data)

# class ChangePasswordAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         password = data['password']
#         confirm_password = data['confirmPassword']

#         if password != confirm_password:
#             return Response({"error" : "Password is not matching"}, status=status.HTTP_400_BAD_REQUEST)


#         return Response("hai", status=200)


class ResetAPIView(APIView):
    def post(self, request):
        token = ''.join(random.choice(string.ascii_lowercase +
                        string.digits) for _ in range(10))
        
        email = request.data['email']

        reset.objects.create(
            email=request.data['email'],
            token=token
        )

        url = 'http://localhost:3000/resetPassword/' + token
        

        

        return Response({
            "success": "created"
        })
