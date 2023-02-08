from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Job, CandidatesApplied
from account.models import CustomUser
from .serializers import JobSerializer, CandidatesAppliedSerializer,CandidatesAllSerializer
from django.db.models import Avg, Min, Max, Count
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .filters import JobsFilter
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@api_view(['GET'])
def getAllJobs(request):
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    
    count = filterset.qs.count()
    
    #pagination
    resPerPage = 3
    
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
    
    candidates = job.candidatesapplied_set.all().count()
    serializer = JobSerializer(job, many=False)
    
    return Response({'job': serializer.data, 'candidates': candidates})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addNewJob(request):
    request.data['user'] = request.user
    data = request.data
    email = request.data['user']
    user  = CustomUser.objects.filter(email=email).last()
    if not user.is_premium:
        return Response({'error': 'purchase premium for Posting job'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
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
    topics_array = []
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
    
    
    isPremium = user.is_premium
    
    if user.userprofile.resume == '':
        return Response({'error': 'Please upload your resume'}, status=status.HTTP_400_BAD_REQUEST)
    
    if job.lastDate < timezone.now():
        return Response({'error': 'you cannot apply to this job. Date is over'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()
    
    if alreadyApplied:
        return Response({'error': 'you have already applied to this job'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    if not isPremium:
        
        return Response({'error': 'purchase premium to apply to job'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
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
    print(applied)
    
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approveResume(request, pk):
    if not CandidatesApplied.objects.filter(id=pk).exists():
        return Response({"error": "wrong id"}, status=status.HTTP_400_BAD_REQUEST)
    
    candidate = get_object_or_404(CandidatesApplied, id=pk)
    # candidate = CandidatesApplied.objects.filter(id=pk).exists()
    
    candidate.is_Approved = True
    candidate.status = "Approved"
    candidate.is_Rejected = False
    
    candidate.save()
    
    return Response({"success": "resume is approved"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rejectResume(request, pk):
    print("reject wroking")
    # candidate = get_object_or_404(CandidatesApplied, id=pk)
    if not CandidatesApplied.objects.filter(id=pk).exists():
        return Response({"error": "Data doesnot exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    candidate = get_object_or_404(CandidatesApplied, id=pk)
    print(candidate, "this is candidate")

    
       
    candidate.is_Rejected = True
    candidate.is_Approved = False
    candidate.status = "Rejected"
    
    candidate.save()
    
    
    
    return Response({"success": "Resume is rejected"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getApprovedCandidates(request):
    email = request.user
  
    candidates = CandidatesApplied.objects.filter(is_Approved=True, job__user=email)

    
    serializer = CandidatesAllSerializer(candidates, many=True)

    
    
    return Response(serializer.data)
        
    
    
    
    
    
        
    
    
    

