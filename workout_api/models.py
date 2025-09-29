from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Excercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    target_muscle = models.CharField(max_length=100)
    steps = models.JSONField(default=list)

    def __str__(self):
        return self.name
    




class WorkoutSession(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]


    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_duration = models.DurationField(blank=True, null=True)
    workout_days = models.JSONField(default=list)  


    


class WorkoutExercise(models.Model):
    exercise = models.ForeignKey(Excercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  
    rest_period = models.DurationField(blank=True, null=True)
    distance = models.FloatField(null=True, blank=True)  
    weight = models.FloatField(null=True, blank=True)  
    order = models.PositiveIntegerField()

