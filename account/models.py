from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class CustomUserManager(BaseUserManager):
    
    def create_user(self,  first_name, last_name, email, mobile_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user_obj = self.model(
            
            email =self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile_number = mobile_number,
            
        )
        
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj
    
    def create_superuser(self,first_name, last_name, email, mobile_number, password=None):
        user_obj = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            password=password,
            
        )
        
        user_obj.is_superuser = True
        user_obj.is_staff = True
        user_obj.is_active = True
        user_obj.save(using=self._db)
        
        return user_obj
        

class CustomUser(AbstractBaseUser):
    # id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    username = models.CharField(max_length=80, null=True)
    email = models.CharField(max_length=50, unique=True)
    mobile_number = models.CharField(max_length=12, blank=True, null=True)
    
    
    # required fields
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','mobile_number']
    
    def __str__(self):
        return self.email
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_all_permissions(user=None):
        if user.is_superuser:
            return set()
    




class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance , created, **kwargs):
    user = instance
    if created :
        profile = UserProfile(user=user)
        
        profile.save()
        
    

