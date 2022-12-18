from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from django.db.models import Avg, Min, Max, Count
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .filters import JobsFilter
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
def addNewJob(request):
    data = request.data
    job = Job.objects.create(**data)
    
    serializer = JobSerializer(job , many=False)
    
    return Response(serializer.data)

@api_view(['PUT'])
def updateJob(request, pk):
    data            = request.data
    job             = get_object_or_404(Job, id=pk)
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
def DeleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)
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
    
    
    

