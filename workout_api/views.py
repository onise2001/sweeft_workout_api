from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Excercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry
from .serializers import ExcerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, ProgressTrackerSerializer, ProgressEntrySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfTracker
# Create your views here.



class WorkoutSessionViewSet(ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)



class ProgressTrackerViewSet(ModelViewSet):
    serializer_class = ProgressTrackerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProgressTracker.objects.filter(user=self.request.user)





class ProgressEntryViewSet(ModelViewSet):
    serializer_class = ProgressEntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOfTracker]


    def get_queryset(self):
        return ProgressEntry.objects.filter(tracker__user=self.request.user)
