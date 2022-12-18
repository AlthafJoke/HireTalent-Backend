from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth.models import User




# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)
    
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            email = data['email']
            username = email.strip('@')
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['first_name'],
                username = username,
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
    
