from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.core.mail import EmailMessage
from .models import *
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from decouple import config

@receiver(post_save, sender=employerProfile)
def send_email(sender, instance , **kwargs):
    user = instance
    
   
    
    #mail for empl
           
    mail_subject = "New Recruiter Registered"
    message = render_to_string('account_verification_email.html', {
        'username': user.user.username,
        'email':user.user,
        'company': user.company,
        'url': 'http://localhost:3000/verify/' + str(user.uniqueCode),
        
    })
    # message = get_template("account_verification_email.html").render(Context({
    #     'user': user
    # }))
    # message = ' pls click this to verify http://localhost:3000/verify/' + str(user.uniqueCode)
    to_email = 'althafav7@gmail.com'
    send_mail = EmailMessage(mail_subject, message, to=[to_email])
    send_mail.content_subtype = "html"
    send_mail.send()
    


    
   



# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance , created, **kwargs):
#     user = instance
#     if created :
        
#         profile = UserProfile(user=user)
        
#         profile.save()
    
    
    
