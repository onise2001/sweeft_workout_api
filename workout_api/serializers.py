from rest_framework import serializers
from .models import Excercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry


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



class ProgressEntrySerializer(serializers.ModelSerializer):
    tracker = serializers.PrimaryKeyRelatedField(read_only=True)
    tracker_id = serializers.PrimaryKeyRelatedField(
        queryset=ProgressTracker.objects.all(),
        write_only=True,
        source='tracker'
    )

    class Meta:
        model = ProgressEntry
        fields = '__all__'

    
    def create(self, validated_data):
        ...
    



class ProgressTrackerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    exercise = ExcerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Excercise.objects.all(),
        write_only=True,
        source='exercise',
        required=False,
        allow_null=True
    )

    entries = ProgressEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = ProgressTracker
        fields = '__all__'
    

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data.get('current_value') is None:
            validated_data['current_value'] = validated_data['start_value'] 
        progress_tracker = ProgressTracker.objects.create(user=user, **validated_data)
        return progress_tracker
    



