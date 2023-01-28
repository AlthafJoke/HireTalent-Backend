from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.core.mail import EmailMessage
from .models import *

@receiver(post_save, sender=employerProfile)
def send_email(sender, instance , **kwargs):
    user = instance
    print(user.uniqueCode)
    print("signal for employer")
    #mail for empl
           
    mail_subject = "New Recruiter Registered"
    message = ' pls click this to verify http://localhost:3000/verify/' + str(user.uniqueCode)
    to_email = 'althafav7@gmail.com'
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    # send_mail.content_subtype = "html"
    send_mail.send()
    


    
   



# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance , created, **kwargs):
#     user = instance
#     if created :
        
#         profile = UserProfile(user=user)
        
#         profile.save()
    
    
    
