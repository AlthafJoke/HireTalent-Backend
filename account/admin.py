from django.contrib import admin
from .models import UserProfile, CustomUser, reset

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.register(reset)

