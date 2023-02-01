from django.db import models
from account.models import CustomUser

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    amount = models.CharField(max_length=250)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.payment_id
