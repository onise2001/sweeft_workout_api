from rest_framework import serializers
from .models import Exercise, WorkoutSession, WorkoutExercise, ProgressTracker, ProgressEntry, ExerciseStep




class ExerciseStepSerializer(serializers.ModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ExerciseStep
        fields = '__all__'



class ExcerciseSerializer(serializers.ModelSerializer):
    exercise_steps = ExerciseStepSerializer(many=True)

    class Meta:
        model = Exercise
        fields = '__all__'

    def create(self,validated_data):
        steps = validated_data.pop('exercise_steps')
        exercise = Exercise.objects.create(**validated_data)
        for step in steps:
            ExerciseStep.objects.create(exercise=exercise, **step)
        return exercise
    
    def validate(self, data):
        steps = data.get('exercise_steps', [])
        step_numbers = [step['step_number'] for step in steps]
        if len(step_numbers) != len(set(step_numbers)):
            raise serializers.ValidationError("Step numbers must be unique.")
        if sorted(step_numbers) != list(range(1, len(step_numbers) + 1)):
            raise serializers.ValidationError("Step numbers must be sequential starting from 1.")
        return data


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExcerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        write_only=True,
        source='exercise'
    )

    workout = serializers.PrimaryKeyRelatedField(read_only=True)
    workout_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.none(),
        write_only=True,
        source='workout',
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
        extra_kwargs = {
            "workout": {"required": False},
            "workout_id": {"required": False},
        }
    

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.hasattr(request, 'user'):
            self.fields['workout_id'].queryset = WorkoutSession.objects.filter(user=request.user)

        

    

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
            if 'workout_id' in exercise_data:
                del exercise_data['workout_id']
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

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.fields['tracker_id'].queryset = ProgressTracker.objects.filter(user=request.user)   

    
    def create(self, validated_data):
        entry = ProgressEntry.objects.create(**validated_data)
        tracker = entry.tracker
        tracker.current_value = entry.value
        tracker.save()
        
        return entry


class ProgressTrackerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    exercise = ExcerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
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
    



