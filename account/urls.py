from django.urls import path
from . import views


urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('me/', views.currentUser, name='current_user'),
    path('me/update/', views.updateUser, name='update_user'),
    path('upload/resume/', views.uploadResume, name='upload_resume'),
    path('google-auth/', views.GoogleAuthAPIView.as_view()),
    path('VerifyRec/<str:id>', views.VerifyRec, name="VerifyRec"),
    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('forgot-password/verify/', views.ForgotPasswordVerifyView.as_view(), name='forgot_password-verify'),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    
   

    
]
