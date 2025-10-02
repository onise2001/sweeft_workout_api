from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_muscle = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class ExerciseStep(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_steps')
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()



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
    start_time = models.TimeField(blank=True, null=True)


    


class WorkoutExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workout_exercises')
    workout = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="exercises")
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  
    rest_period = models.DurationField(blank=True, null=True)
    distance = models.FloatField(null=True, blank=True)  
    weight = models.FloatField(null=True, blank=True)  
    order = models.PositiveIntegerField()





class ProgressTracker(models.Model):
    GOAL_TYPES = (
        ('weight', 'Weight'),
        ('exercise', 'Eexercise')
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True)
    start_value = models.FloatField()
    target_value = models.FloatField()
    current_value = models.FloatField(null=True, blank=True)
    value_unit = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)




class ProgressEntry(models.Model):
    tracker = models.ForeignKey(ProgressTracker, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField(auto_now_add=True)
    value = models.FloatField()
    notes = models.TextField(blank=True, null=True)




class ActiveWorkout(models.Model):
    workout = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    current_exercise_index = models.IntegerField(default=0)



class ExerciseCompletion(models.Model):
    active_workout = models.ForeignKey(ActiveWorkout, on_delete=models.CASCADE, related_name='completed_exercises')
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='completions')
    completed_sets = models.IntegerField()
    completed_reps = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

