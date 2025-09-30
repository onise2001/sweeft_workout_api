from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutSessionViewSet, ProgressTrackerViewSet, ProgressEntryViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')
router.register(r'progress-trackers', ProgressTrackerViewSet, basename='progresstracker')
router.register(r'progress-entries', ProgressEntryViewSet, basename='progressentry')

urlpatterns = [
    path('', include(router.urls)),

]