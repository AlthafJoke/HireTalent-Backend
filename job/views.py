from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Job, CandidatesApplied
from .serializers import JobSerializer, CandidatesAppliedSerializer
from django.db.models import Avg, Min, Max, Count
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .filters import JobsFilter
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Create your views here.

@api_view(['GET'])
def getAllJobs(request):
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    
    count = filterset.qs.count()
    
    #pagination
    resPerPage = 2
    
    paginator = PageNumberPagination()
    
    paginator.page_size = resPerPage
    
    query_set = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = JobSerializer(query_set, many=True)
    return Response({
        'count': count,
        'resPerPage':resPerPage,
        'jobs':serializer.data})

@api_view(['GET'])
def getJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    serializer = JobSerializer(job, many=False)
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNewJob(request):
    request.data['user'] = request.user
    data = request.data
    job = Job.objects.create(**data)
    
    serializer = JobSerializer(job , many=False)
    
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateJob(request, pk):
    data            = request.data
    job             = get_object_or_404(Job, id=pk)
    
    if job.user != request.user:
        return Response({'message': 'you cannot update this job'}, status=status.HTTP_403_FORBIDDEN)
    #else update
    job.title       = data['title']
    job.description = data['description']
    job.email       = data['email']
    job.address     = data['address']
    job.jobType     = data['jobType']
    job.education   = data['education']
    job.industry    = data['industry']
    job.experience  = data['experience']
    job.salary      = data['salary']
    job.positions   = data['positions']
    job.company     = data['company']
    
    job.save()

    serializer = JobSerializer(job , many=False)
    
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    if job.user != request.user:
        return Response({'message': 'you cannot delete this job'}, status=status.HTTP_403_FORBIDDEN)
    
    #else delete job
    job.delete()
    
    return Response({'message': 'job deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTopicStats(request, topic):
    args = {'title__icontains': topic}
    jobs = Job.objects.filter(**args)
    
    if len(jobs) == 0:
        return Response({'message': 'Not stats found for {topic}'.format(topic=topic)})
    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary   = Avg('salary'),
        min_salary   = Min('salary'),
        max_salary   = Max('salary'),
        
    )
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyJob(request, pk):
    
    user = request.user
    job  = get_object_or_404(Job, id=pk)
    
    if user.userprofile.resume == '':
        return Response({'error': 'Please upload your resume'}, status=status.HTTP_400_BAD_REQUEST)
    
    if job.lastDate < timezone.now():
        return Response({'error': 'you cannot apply to this job. Date is over'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()
    
    if alreadyApplied:
        return Response({'error': 'you have already applied to this job'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    jobApplied = CandidatesApplied.objects.create(
        job=job,
        user=user,
        resume=user.userprofile.resume
        )
    
    return Response({
        'applied': True,
        'job_id' : jobApplied.id,
    },status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserAppliedJobs(request):
    
    args = {'user_id': request.user.id}
    
    jobs = CandidatesApplied.objects.filter(**args)
    
    serializer = CandidatesAppliedSerializer(jobs, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isApplied(request, pk):
    
    user = request.user
    job = get_object_or_404(Job, id=pk)
    
    applied = job.candidatesapplied_set.filter(user=user).exists()
    
    return Response(applied)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserJobs(request): # for getting list of  jobs posted by the current user
    
    args = { 'user': request.user.id }
    
    jobs = Job.objects.filter(**args)
    
    serializer = JobSerializer(jobs, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidatesApplied(request, pk):
    
    user = request.user
    job = get_object_or_404(Job, id=pk)
    
    if job.user != user: # for making sure that the user that is accessing is the owner of this job
        return Response({'error': 'you cannot access this job'}, status=status.HTTP_403_FORBIDDEN)
    
    candidates = job.candidatesapplied_set.all()
    
    serialzer = CandidatesAppliedSerializer(candidates, many=True)
    
    return Response(serialzer.data)
    
    
        
    
    
    

