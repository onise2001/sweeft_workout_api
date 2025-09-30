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

    workout = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
    

        

    

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = WorkoutSession
        fields = '__all__'
    
    def create(self,validated_data):
        print(validated_data)
        exercises_data = validated_data.pop('exercises')
        user = self.context['request'].user
        workout_session = WorkoutSession.objects.create(user=user,**validated_data)
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout=workout_session, **exercise_data)
        return workout_session


