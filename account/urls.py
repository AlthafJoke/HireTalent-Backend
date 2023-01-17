from django.urls import path
from . import views


urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('me/', views.currentUser, name='current_user'),
    path('me/update/', views.updateUser, name='update_user'),
    path('upload/resume/', views.uploadResume, name='upload_resume'),
    path('google-auth/', views.GoogleAuthAPIView.as_view()),
    path('VerifyRec/<str:id>', views.VerifyRec, name="VerifyRec"),
    # path('resetPasswordRequest/', views.resetPasswordRequestAPIView.as_view(), name='resetPasswordRequest'),
    # path('resetPassword/', views.resetPasswordAPIView.as_view(), name="resetPassword"),
    # path('change_password/', views.ChangePasswordAPIView.as_view(), name="change-password"),
    path('reset/', views.ResetAPIView.as_view()),

    
    
]
