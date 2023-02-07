from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.core.mail import EmailMessage
from .models import *

@receiver(post_save, sender=CandidatesApplied)
def send_email(sender, instance , **kwargs):
    if instance.is_Approved:
        print(" signal msg: resume approved ")
        # mail_subject = "New job application "
        # message = "your resume is approved please wait for the call"
        # to_email = instance.user
        # send_mail = EmailMessage(mail_subject, message, to=[to_email])
        # # send_mail.content_subtype = "html"
        # send_mail.send()
    
    
#     print(instance, "sjdfksdfjskd")
#     print(instance.job.user)
#     print("applied")
#     employer_email = instance.job.user
#     user_email = instance.user
    
#     mail_subject = "New job application "
#     message = str(user_email) + "is applied for your job post"
#     to_email = employer_email
#     send_mail = EmailMessage(mail_subject, message, to=[to_email])
#     # send_mail.content_subtype = "html"
#     send_mail.send()
    
    