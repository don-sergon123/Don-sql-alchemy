from marshmallow import Schema, fields, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    @validates('category')
    def validate_category(self, value):
        valid_cats = ['Strength', 'Cardio', 'Flexibility', 'Endurance']
        if value not in valid_cats:
            raise ValidationError(
                f"Category must be one of: {', '.join(valid_cats)}")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(load_default="")

    @validates('duration_minutes')
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError(
                "Duration in minutes must be greater than 0.")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(required=True)
    sets = fields.Int(required=True)
    duration_seconds = fields.Int(required=True)

    @validates('sets')
    def validate_sets(self, value):
        if value <= 0:
            raise ValidationError("Sets must be greater than 0.")

    @validates('reps')
    def validate_reps(self, value):
        if value < 0:
            raise ValidationError("Reps cannot be negative.")


# Schema instances for single items and collections
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
