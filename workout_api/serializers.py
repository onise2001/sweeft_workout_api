from rest_framework import serializers
from .models import Excercise, WorkoutSession, WorkoutExercise


class ExcerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excercise
        fields = '__all__'


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExcerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Excercise.objects.all(),
        write_only=True,
        source='exercise'
    )

    class Meta:
        model = WorkoutExercise
        fields = '__all__'

        

    

class WorkoutSessionSerializer(serializers.ModelSerializer):
    excercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = '__all__'


