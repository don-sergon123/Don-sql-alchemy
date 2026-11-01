from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import db, Exercise, Workout, WorkoutExercise
from .schema import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response(exercise_schema.dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    try:
        data = exercise_schema.load(json_data)
        new_exercise = Exercise(**data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)
    except ValueError as err:
        return make_response({"error": str(err)}, 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    return make_response(workout_schema.dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    try:
        data = workout_schema.load(json_data)
        new_workout = Workout(**data)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)
    except ValueError as err:
        return make_response({"error": str(err)}, 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)


@app.route('/workout_exercises', methods=['POST'])
def add_exercise_to_workout():
    json_data = request.get_json()
    try:
        data = workout_exercise_schema.load(json_data)
        new_we = WorkoutExercise(**data)
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)
    except ValueError as err:
        return make_response({"error": str(err)}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
