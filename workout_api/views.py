from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Exercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry, ActiveWorkout,ExerciseCompletion
from .serializers import ExerciseSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, ProgressTrackerSerializer, ProgressEntrySerializer, ActiveWorkoutSerializer, ExerciseCompletionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOfTracker
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
# Create your views here.



class WorkoutSessionViewSet(ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)



class ExerciseViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
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

    @swagger_auto_schema(
        operation_description="List all workout sessions for the authenticated user",
        responses={200: WorkoutSessionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new workout session",
        request_body=WorkoutSessionSerializer,
        responses={
            201: WorkoutSessionSerializer,
            400: "Bad Request - Invalid data provided"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific workout session",
        responses={
            200: WorkoutSessionSerializer,
            404: "Not Found - Workout session does not exist"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a workout session",
        request_body=WorkoutSessionSerializer,
        responses={
            200: WorkoutSessionSerializer,
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Workout session does not exist"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a workout session",
        responses={
            204: "No Content - Successfully deleted",
            404: "Not Found - Workout session does not exist"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)



class ActiveWorkoutViewSet(ModelViewSet):
    serializer_class = ActiveWorkoutSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return ActiveWorkout.objects.filter(user=self.request.user, is_active=True)
    
    
    @action(detail=False, methods=['post'])
    def start_workout(self,request):
        if ActiveWorkout.objects.filter(user=request.user, is_active=True).exists():
            return Response({"detail": "You already have an active workout."}, status=status.HTTP_400_BAD_REQUEST)

        workout_session_id = request.data.get('workout_session_id')
        workout_session = get_object_or_404(WorkoutSession, pk=workout_session_id, user=request.user)
        active_workout = ActiveWorkout.objects.create(workout=workout_session, user=request.user)
        serializer = self.get_serializer(active_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['post'])
    def complete_exercise(self, request,pk=None):
        active_workout = self.get_object()
        serializer = ExerciseCompletionSerializer(
            data=request.data,
                context={"request":request, "active_workout": active_workout}
        )

        if serializer.is_valid():
            serializer.save(active_workout=active_workout)
            active_workout.current_exercise_index += 1
            
            if active_workout.current_exercise_index >= active_workout.workout.exercises.count():
                active_workout.is_active = False
                active_workout.end_time = timezone.now()

            active_workout.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, methods=['get'])
    def current_exercise(self, request, pk=None):
        active_workout = self.get_object()
        current_exercise = self.get_serializer(active_workout).get_current_exercise(active_workout)
        next_exercise = self.get_serializer(active_workout).get_next_exercise(active_workout)
        progress = self.get_serializer(active_workout).get_progress(active_workout)
        return Response({
            'current_exercise': current_exercise,
            'next_exercise': next_exercise,
            'progress': progress
        }, status=status.HTTP_200_OK)