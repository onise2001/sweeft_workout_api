from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Exercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry, ActiveWorkout,ExerciseCompletion
from .serializers import ExcerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, ProgressTrackerSerializer, ProgressEntrySerializer, ActiveWorkoutSerializer, ExerciseCompletionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOfTracker
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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



class ActiveWorkoutViewSet(ModelViewSet):
    serializer_class = ActiveWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ActiveWorkout.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    
    @action(detail=True, methods=['post'])
    def start_workout(self,request, pk=None):
        workout_session = get_object_or_404(WorkoutSession, pk=pk, user=request.user)
        active_workout = ActiveWorkout.objects.create(workout=workout_session, user=request.user)
        serializer = self.get_serializer(active_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['post'])
    def complete_exercise(self, request, pk=None):
        active_workout = self.get_object()
        serializer = ExerciseCompletionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(active_workout=active_workout)
            active_workout.current_exercise_index += 1
            
            if active_workout.current_exercise_index >= active_workout.workout.exercises.count():
                active_workout.is_active = False
                active_workout.end_time = timezone.now()

            active_workout.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)