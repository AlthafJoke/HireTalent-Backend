from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['admin'] = user.is_admin
        token['is_staff'] = user.is_staff
        token['is_recruiter'] = user.is_recruiter
        token['is_premium'] = user.is_premium
        token['username'] = user.username
        
       
        
        return token




class SignUpSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required = True,
    #     validators = [UniqueValidator(queryset=CustomUser.objects.all())]
    # )
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')
        
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 6},
             
        }
        

class UserSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source='userprofile.resume', read_only=True)
    company = serializers.CharField(source='employerprofile.company', read_only=True)
    designation = serializers.CharField(source='employerprofile.designation', read_only=True)
    is_recruiter = serializers.CharField(source='employerprofile.is_recruiter', read_only=True)
    is_approved = serializers.CharField(source='employerprofile.is_approved', read_only=True) 
    class Meta:
        model = CustomUser
        fields = "__all__"