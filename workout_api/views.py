from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Excercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry
from .serializers import ExcerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, ProgressTrackerSerializer, ProgressEntrySerializer


# Create your views here.



class WorkoutSessionViewSet(ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer



class ProgressTrackerViewSet(ModelViewSet):
    queryset = ProgressTracker.objects.all()
    serializer_class = ProgressTrackerSerializer




class ProgressEntryViewSet(ModelViewSet):
    queryset = ProgressEntry.objects.all()
    serializer_class = ProgressEntrySerializer
