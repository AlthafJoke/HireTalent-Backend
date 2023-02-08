from rest_framework import serializers
from . models import Job, CandidatesApplied


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        
class CandidatesAppliedSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    class Meta:
        model = CandidatesApplied
        fields = ('id','user', 'resume', 'appliedAt', 'job', 'is_Approved', 'status')
        

class CandidatesAllSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',read_only=True)
    job = serializers.CharField(read_only=True)
    
    class Meta:
        model = CandidatesApplied
        fields = "__all__"

    
    