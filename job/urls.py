from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name='jobs'),
    path('job/new-job/', views.addNewJob, name = 'new_job'),
    path('job/<str:pk>/', views.getJob, name='job'),
    path('job/<int:pk>/update/', views.updateJob, name='update_job'),
    path('job/<int:pk>/delete/', views.DeleteJob, name='delete_job'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats'),
    path('job/<str:pk>/apply/', views.applyJob, name='apply_to_job'),
    path('me/jobs/applied/', views.getCurrentUserAppliedJobs, name="current_user_applied_jobs"),
    path('job/<str:pk>/check/', views.isApplied, name='is_applied_to_job'),
    path('me/jobs/', views.getCurrentUserJobs, name='get_current_user_jobs'), #get all jobs posted by current user
    path('job/<str:pk>/candidates/' , views.getCandidatesApplied, name='get_candidates_applied'),
    path('candidate/<str:pk>/approve/', views.approveResume, name='approveResume'),
    path('candidate/<str:pk/reject/', views.rejectResume, name='rejectResume'),
    
   
    
]


