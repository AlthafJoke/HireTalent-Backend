from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated




# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)
    
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            
            email = data['email']
            username = email.split("@")[0]
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['first_name'],
                username = data['email'],
                email = data['email'],
                password = make_password(data['password'])
               
            )
            return Response({
                'success': 'user created successfully'},
                status= status.HTTP_200_OK)
        else :
            
            return Response({
                'error': 'user already exist'},
                status= status.HTTP_400_BAD_REQUEST)
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
    user = request.user
    
    
    data = request.data
    email = data['email']
    username = email.split("@")[0]
    
    user.first_name = data['first_name']
    user.last_name  = data['last_name']
    user.username   = username
    user.email      = email
    
    if data['password'] != '':
        user.password = make_password(data['password'])
        
    user.save()
    
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
        
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadResume(request):
    
    user = request.user
    
    resume = request.FILES['resume']
    
    if resume == '' :
        return Response({'error': 'please upload your resume'})
    
    
    
    user.userprofile.resume = resume
    user.userprofile.save()
    
    serializer = UserSerializer(user, many=False)
    
    return Response(serializer.data)
    
    
