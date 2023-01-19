from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from .models import *

@receiver(post_save, sender=CustomUser)
def send_email(sender, instance , **kwargs):
    print(instance)
    # print(instance.first_name)
    # print(instance.is_recruiter)
    
    # email = instance
    
    # user = CustomUser.objects.filter(email=email)
    
    # print(user.first_name)
    
    
    
    
    
    
    
    
    
 
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance , created, **kwargs):
    user = instance
    if created :
        
        profile = UserProfile(user=user)
        
        profile.save()
    
    
    
