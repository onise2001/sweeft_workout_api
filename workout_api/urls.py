from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutSessionViewSet, ProgressTrackerViewSet, ProgressEntryViewSet, ExerciseViewSet, WorkoutExerciseViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')
router.register(r'progress-trackers', ProgressTrackerViewSet, basename='progresstracker')
router.register(r'progress-entries', ProgressEntryViewSet, basename='progressentry')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workout-exercises', WorkoutExerciseViewSet, basename='workoutexercise')

urlpatterns = [
    path('', include(router.urls)),

]