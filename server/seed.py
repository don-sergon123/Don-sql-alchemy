#!/usr/bin/env python3
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Seeding database...")

    # Clear out existing records to avoid duplication
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # 1. Create Sample Exercises
    ex1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Treadmill Run", category="Cardio",
                   equipment_needed=True)
    ex3 = Exercise(name="Squats", category="Strength", equipment_needed=False)

    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    # 2. Create Sample Workouts
    w1 = Workout(date=date(2026, 10, 1),
                 duration_minutes=45, notes="Upper body day")
    w2 = Workout(date=date(2026, 10, 2),
                 duration_minutes=30, notes="Morning cardio")

    db.session.add_all([w1, w2])
    db.session.commit()

    # 3. Associate Exercises to Workouts via Join Table
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id,
                          reps=20, sets=3, duration_seconds=120)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex3.id,
                          reps=15, sets=4, duration_seconds=180)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex2.id,
                          reps=0, sets=1, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")
