from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Excercise, WorkoutSession, WorkoutExercise
from .serializers import ExcerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer

# Create your views here.



class WorkoutSessionViewSet(ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer




