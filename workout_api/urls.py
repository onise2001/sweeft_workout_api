from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutSessionViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')


urlpatterns = [
    path('', include(router.urls)),

]