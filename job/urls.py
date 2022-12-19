from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name='jobs'),
    path('job/<str:pk>/', views.getJob, name='job'),
    path('job/new/', views.addNewJob, name = 'new_job'),
    path('job/<int:pk>/update/', views.updateJob, name='update_job'),
    path('job/<int:pk>/delete/', views.DeleteJob, name='delete_job'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats'),
    path('job/<str:pk>/apply/', views.applyJob, name='apply_to_job'),
   
    
]
