from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = b'\x9d\xab\xa1(\xe7.\x8d\x1e)\x90\x84f/\x04\x19\xd9\xb4\xae\x93\xe9\xaa\x03'

# Configure your SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

# Define the FitnessRecord model
class FitnessRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer, nullable=False)
    running_distance = db.Column(db.Float, nullable=False)
    jumping = db.Column(db.Integer, nullable=False)

# Define the FitnessForm
class FitnessForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired()])
    running_distance = FloatField('Running Distance (in miles)', validators=[DataRequired()])
    jumping = IntegerField('Jumping (in inches)', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Route for submitting fitness data
@app.route('/fitness', methods=['GET', 'POST'])
def fitness():
    form = FitnessForm()
    if form.validate_on_submit():
        new_record = FitnessRecord(
            reps=form.reps.data,
            running_distance=form.running_distance.data,
            jumping=form.jumping.data
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('success'))
    return render_template('fitness.html', form=form)



@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/')
def home():
    return render_template('welcome.html')

class Form(FlaskForm):
    set = IntegerField('Reps', validators=[DataRequired()])
    set_running_distance = FloatField('Running Distance (in miles)', validators=[DataRequired()])
    set_jumping = IntegerField('Jumping (in inches)', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/view_records', methods=['GET', 'POST'])
def view_records():
    records = FitnessRecord.query.all()
    form = Form()
    if form.validate_on_submit():
        # If the form is submitted, update the target reps with the user input
        form.set.data = form.set.data
        form.set_running_distance.data = form.set_running_distance.data
        form.set_jumping.data = form.set_jumping.data

    return render_template('view_records.html', records=records,form=form)

class BMIForm(FlaskForm):
    height = FloatField('Enter your height in cm:',validators=[DataRequired()])
    weight = FloatField('Enter your weight in kg:',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/BMI', methods=['GET', 'POST'])
def calculate_bmi():
    form = BMIForm()
    bmi = None

    if form.validate_on_submit():
        height = form.height.data
        height= height/100
        height= height**2
        weight = form.weight.data
        bmi = weight/height

    return render_template('BMI.html', form=form, bmi=bmi)




@app.route('/delete_record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    # Find the record in the database
    record = FitnessRecord.query.get(record_id)
    
    if record:
        db.session.delete(record)
        db.session.commit()
        flash('Record deleted successfully!', 'success')
    else:
        flash('Record not found!', 'error')
    
    return redirect(url_for('view_records'))


@app.route('/avg_records')
def avg_records():

    records = FitnessRecord.query.all()
    total_reps = sum(record.reps for record in records)  # Calculate the total "Reps" values
    total_running_distance = sum(record.running_distance for record in records)
    total_jumping = sum(record.jumping for record in records)
    
    if records:  # Ensure there are records to calculate the average
        average_reps = total_reps / len(records)
        average_running_distance = total_running_distance / len(records)
        average_jumping = total_jumping / len(records)
    else:
        average_reps = 0  # Set the average to 0 if there are no records
        average_running_distance=0
        average_jumping = 0
    return render_template('avg_records.html', average_reps=average_reps,average_running_distance=average_running_distance, average_jumping=average_jumping )

@app.route('/stopwatch')
def stopwatch():
    return render_template('stopwatch.html')

if __name__ == "__main__":
    app.run(debug=True)
