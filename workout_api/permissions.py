from rest_framework.permissions import BasePermission
from .models import ProgressTracker

class IsOwnerOfTracker(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.tracker.user == request.user