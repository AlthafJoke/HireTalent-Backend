from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import *
# from django.contrib.auth.models import User
from account.models import CustomUser


# Create your models here.

class JobType(models.TextChoices):
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Internship = 'Internship'

class Education(models.TextChoices):
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Phd = 'Phd'

class Industry(models.TextChoices):
    Business = 'Business'
    IT = 'IT'
    Banking = 'Banking'
    Education = 'Education/Training'
    Telecommunication = 'Telecommunication'
    Others = 'Others'

class Experience(models.TextChoices):
    NO_EXPIRIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2 Years'
    THREE_YEAR_PLUS = '3 Years above'
    

def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)
    
    
    
    

class Job(models.Model):
    title               = models.CharField(max_length=200, null=True)
    user                = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description         = models.TextField(null=True)
    email               = models.EmailField(null=True)
    address             = models.CharField(max_length=200, null=True)
    jobType             = models.CharField(max_length=10, choices=JobType.choices, default=JobType.Permanent)
    education           = models.CharField(max_length=10, choices=Education.choices, default=Education.Bachelors)
    industry            = models.CharField(max_length=30, choices=Industry.choices, default=Industry.Business)
    experience          = models.CharField(max_length=20, choices=Experience.choices, default=Experience.NO_EXPIRIENCE)
    salary              = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10000000)])
    positions           = models.IntegerField(default=1)
    company             = models.CharField(max_length=100, null=True)
 
    lastDate            = models.DateTimeField(default=return_date_time)
    created_at          = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    

class CandidatesApplied(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True) 
    resume = models.CharField(max_length=200)
    
    status = models.CharField(max_length=255, null=True, blank=True , default="Pending")
    is_Approved = models.BooleanField(default=False)
    is_Rejected = models.BooleanField(default=False)
    appliedAt = models.DateTimeField(auto_now_add=True)
    
    
    

    
    
    
    
