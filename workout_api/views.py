from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Exercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry
from .serializers import ExcerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, ProgressTrackerSerializer, ProgressEntrySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOfTracker
# Create your views here.



class WorkoutSessionViewSet(ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)



class ExerciseViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExcerciseSerializer
    http_method_names = ['get', 'head', 'options']


class WorkoutExerciseViewSet(ModelViewSet):
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutExercise.objects.filter(workout__user=self.request.user)
    
    def perform_create(self,serializer):
        workout = serializer.validated_data['workout']
        if workout.user != self.request.user:
            raise PermissionDenied("You do not have permission to add exercises to this workout.")
        
        serializer.save()


class ProgressTrackerViewSet(ModelViewSet):
    serializer_class = ProgressTrackerSerializer

    def get_queryset(self):
        return ProgressTracker.objects.filter(user=self.request.user)
    

    def get_permissions(self):
        if self.action in ['create', 'head', 'options']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOfTracker]
        return [permission() for permission in permission_classes]

class ProgressEntryViewSet(ModelViewSet):
    serializer_class = ProgressEntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOfTracker]

    def get_queryset(self):
        return ProgressEntry.objects.filter(tracker__user=self.request.user)
