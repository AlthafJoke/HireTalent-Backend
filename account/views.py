from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .validators import validate_file_extension
from django.core.exceptions import ValidationError
from django.http import JsonResponse




# Create your views here.



@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():

            
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['first_name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])

            )
            return Response({
                'success': 'user created successfully'},
                status=status.HTTP_200_OK)
        else:

            return Response({
                'error': 'user already exist'},
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


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


# class GoogleAuthAPIView(APIView):
#     def post(self, request):
#         token = request.data['token']
        
#         googleUser = id_token.verify_token(token, GoogleRequest())
        
#         if not googleUser:
#             raise exceptions.AuthenticationFailed('unauthenticated')
        
#         user = User.objects.filter(email=googleUser['email']).first()
        
#         if not user:
#             user = User.objects.create(
#                 first_name = googleUser['given_name'],
#                 last_name = googleUser['family_name'],
#                 email = googleUser['email']
#             )
#             user.set_password(token)
            
#             user.save()
        
#         response = Response()
            
#         access_token = get_tokens_for_user(user)
        
#         print("token is :", access_token)
        
#         response.set_cookie(key='refresh_token', value='access_token', httponly=True)
        
#         response.data = {
#             'token': access_token,
#         }
        
#         return response
        
