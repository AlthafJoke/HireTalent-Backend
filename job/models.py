from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from datetime import *
from django.contrib.auth.models import User




# Create your models here.

class JobType(models.TextChoices):
    Permenent = 'Permenent'
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
    NO_EXPIRIENCE = 'No Expirence'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2 years'
    THREE_YEAR_PLUS = '3 Year above'
    

def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)
    
    
    
    

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    jobType = models.CharField(max_length=10, choices=JobType.choices, default=JobType.permenent)
    education = models.CharField(max_length=10, choices=Education.choices, default=Education.Bachelors)
    industry = models.CharField(max_length=30, choices=Industry.choices, default=Industry.Business)
    experience = models.CharField(max_length=20, choices=Experience.choices, default=Experience.NO_EXPIRIENCE)
    salary = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10000000)])
    positions = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=True)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    lastDate = models.DateTimeField(default=return_date_time)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
