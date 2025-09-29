from django.core.management.base import BaseCommand
from workout_api.models import Excercise


exercises = [
    {
        "name": "Squats",
        "description": "A fundamental lower-body exercise that strengthens the legs and glutes.",
        "target_muscle": "Quadriceps, Glutes",
        "steps": [
            {"step": 1, "instruction": "Stand with feet shoulder-width apart."},
            {"step": 2, "instruction": "Lower your hips down and back as if sitting in a chair."},
            {"step": 3, "instruction": "Keep chest up and knees behind toes."},
            {"step": 4, "instruction": "Push through heels to return to starting position."}
        ]
    },
    {
        "name": "Push-ups",
        "description": "Upper-body pressing exercise that strengthens chest, shoulders, and triceps.",
        "target_muscle": "Chest, Triceps, Shoulders",
        "steps": [
            {"step": 1, "instruction": "Start in a plank position with hands under shoulders."},
            {"step": 2, "instruction": "Lower your body until chest nearly touches the floor."},
            {"step": 3, "instruction": "Push back up to starting position."}
        ]
    },
    {
        "name": "Pull-ups",
        "description": "Pulling exercise that targets back and biceps using body weight.",
        "target_muscle": "Lats, Biceps",
        "steps": [
            {"step": 1, "instruction": "Grab the pull-up bar with palms facing away."},
            {"step": 2, "instruction": "Pull your body upward until chin passes the bar."},
            {"step": 3, "instruction": "Lower slowly back to starting position."}
        ]
    },
    {
        "name": "Lunges",
        "description": "Unilateral leg exercise that strengthens legs and improves balance.",
        "target_muscle": "Quadriceps, Glutes, Hamstrings",
        "steps": [
            {"step": 1, "instruction": "Stand upright, feet together."},
            {"step": 2, "instruction": "Step forward with one leg and lower hips until both knees are bent at 90°."},
            {"step": 3, "instruction": "Push through front heel to return to standing."}
        ]
    },
    {
        "name": "Plank",
        "description": "Core stabilization exercise that strengthens the abs and lower back.",
        "target_muscle": "Core, Abs",
        "steps": [
            {"step": 1, "instruction": "Lie face down and lift body onto forearms and toes."},
            {"step": 2, "instruction": "Keep body in a straight line from head to heels."},
            {"step": 3, "instruction": "Hold the position for desired time."}
        ]
    },
    {
        "name": "Bench Press",
        "description": "Classic chest exercise performed with a barbell or dumbbells on a bench.",
        "target_muscle": "Chest, Triceps, Shoulders",
        "steps": [
            {"step": 1, "instruction": "Lie on a flat bench holding the barbell above chest."},
            {"step": 2, "instruction": "Lower the bar slowly to chest level."},
            {"step": 3, "instruction": "Push the bar back up to the starting position."}
        ]
    },
    {
        "name": "Deadlift",
        "description": "Full-body strength exercise that targets posterior chain muscles.",
        "target_muscle": "Hamstrings, Glutes, Back",
        "steps": [
            {"step": 1, "instruction": "Stand with feet hip-width apart, barbell over midfoot."},
            {"step": 2, "instruction": "Hinge at hips, grab the bar with both hands."},
            {"step": 3, "instruction": "Lift the bar by extending hips and knees, keeping back straight."},
            {"step": 4, "instruction": "Lower bar back to the ground with control."}
        ]
    },
    {
        "name": "Bicep Curls",
        "description": "Isolation exercise for the biceps using dumbbells or a barbell.",
        "target_muscle": "Biceps",
        "steps": [
            {"step": 1, "instruction": "Stand upright holding weights with palms facing forward."},
            {"step": 2, "instruction": "Curl weights up while keeping elbows close to torso."},
            {"step": 3, "instruction": "Lower weights slowly to starting position."}
        ]
    },
    {
        "name": "Tricep Dips",
        "description": "Bodyweight exercise targeting the triceps.",
        "target_muscle": "Triceps",
        "steps": [
            {"step": 1, "instruction": "Sit on a bench with hands next to hips."},
            {"step": 2, "instruction": "Slide off the bench and lower body by bending elbows."},
            {"step": 3, "instruction": "Push back up to starting position."}
        ]
    },
    {
        "name": "Shoulder Press",
        "description": "Overhead pressing movement for deltoids using dumbbells or barbell.",
        "target_muscle": "Shoulders, Triceps",
        "steps": [
            {"step": 1, "instruction": "Sit or stand with weights at shoulder height."},
            {"step": 2, "instruction": "Press weights overhead until arms are fully extended."},
            {"step": 3, "instruction": "Lower weights back to shoulders slowly."}
        ]
    },
    {
        "name": "Russian Twist",
        "description": "Core exercise targeting obliques.",
        "target_muscle": "Obliques, Abs",
        "steps": [
            {"step": 1, "instruction": "Sit on floor with knees bent, feet off the ground."},
            {"step": 2, "instruction": "Twist torso to one side, then the other, holding a weight optionally."}
        ]
    },
    {
        "name": "Mountain Climbers",
        "description": "Full-body dynamic exercise for core and cardiovascular fitness.",
        "target_muscle": "Core, Cardio, Legs",
        "steps": [
            {"step": 1, "instruction": "Start in a plank position."},
            {"step": 2, "instruction": "Drive one knee toward chest, then switch legs quickly."}
        ]
    },
    {
        "name": "Burpees",
        "description": "High-intensity full-body exercise combining push-ups and jumps.",
        "target_muscle": "Full Body, Cardio",
        "steps": [
            {"step": 1, "instruction": "Start standing, then squat and place hands on the floor."},
            {"step": 2, "instruction": "Kick feet back into plank, perform a push-up."},
            {"step": 3, "instruction": "Jump feet back to hands, then explosively jump upward."}
        ]
    },
    {
        "name": "Leg Raises",
        "description": "Abdominal exercise targeting lower abs.",
        "target_muscle": "Abs",
        "steps": [
            {"step": 1, "instruction": "Lie on back, legs extended."},
            {"step": 2, "instruction": "Raise legs until perpendicular to floor."},
            {"step": 3, "instruction": "Lower slowly without touching the ground."}
        ]
    },
    {
        "name": "Glute Bridge",
        "description": "Hip extension exercise targeting glutes and hamstrings.",
        "target_muscle": "Glutes, Hamstrings",
        "steps": [
            {"step": 1, "instruction": "Lie on back with knees bent, feet flat on floor."},
            {"step": 2, "instruction": "Lift hips off the ground until shoulders-knees-hips form a straight line."},
            {"step": 3, "instruction": "Lower hips slowly back to floor."}
        ]
    },
    {
        "name": "Step-Ups",
        "description": "Leg exercise performed by stepping onto a platform.",
        "target_muscle": "Quadriceps, Glutes",
        "steps": [
            {"step": 1, "instruction": "Stand in front of a sturdy bench or step."},
            {"step": 2, "instruction": "Step onto the platform with one foot, push through heel."},
            {"step": 3, "instruction": "Step down and repeat with the other leg."}
        ]
    },
    {
        "name": "Side Plank",
        "description": "Core stabilization exercise targeting obliques.",
        "target_muscle": "Obliques, Core",
        "steps": [
            {"step": 1, "instruction": "Lie on side, supporting body on one forearm."},
            {"step": 2, "instruction": "Lift hips so body forms a straight line."},
            {"step": 3, "instruction": "Hold the position, then switch sides."}
        ]
    },
    {
        "name": "Hip Thrust",
        "description": "Glute-focused hip extension exercise.",
        "target_muscle": "Glutes, Hamstrings",
        "steps": [
            {"step": 1, "instruction": "Sit on the floor with upper back against bench."},
            {"step": 2, "instruction": "Place barbell or weight over hips (optional)."},
            {"step": 3, "instruction": "Thrust hips upward until knees-hips-shoulders align."},
            {"step": 4, "instruction": "Lower back down slowly."}
        ]
    },
    {
        "name": "Dumbbell Rows",
        "description": "Back exercise performed with dumbbells.",
        "target_muscle": "Lats, Rhomboids, Biceps",
        "steps": [
            {"step": 1, "instruction": "Place one knee and hand on a bench for support."},
            {"step": 2, "instruction": "Hold dumbbell in other hand, pull it toward your torso."},
            {"step": 3, "instruction": "Lower dumbbell slowly and repeat."}
        ]
    },
    {
        "name": "Jumping Jacks",
        "description": "Cardio warm-up exercise.",
        "target_muscle": "Full Body, Cardio",
        "steps": [
            {"step": 1, "instruction": "Stand upright with arms at sides."},
            {"step": 2, "instruction": "Jump feet apart while raising arms overhead."},
            {"step": 3, "instruction": "Return to starting position and repeat."}
        ]
    }
]




class Command(BaseCommand):
    help = 'Seed the database with initial exercises'

    def handle(self, *args, **kwargs):
        for exercise_data in exercises:
            Excercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'description': exercise_data['description'],
                    'target_muscle': exercise_data['target_muscle'],
                    'steps': exercise_data['steps']
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded exercises'))