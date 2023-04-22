from wtforms import Form, StringField, SelectField, DateField, DecimalField, TextAreaField, IntegerField, PasswordField, BooleanField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class ViewMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(
        min=5, max=25), validators.DataRequired()])
    submit = SubmitField('Submit')


class AddMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(
        min=5, max=25), validators.DataRequired()])
    DocName = StringField('Doctor Name', [validators.Length(
        min=5, max=25), validators.DataRequired()])
    medicalReport = TextAreaField('Medical Report', [validators.length(
        min=10, max=200), validators.DataRequired()])
    pulse = IntegerField('Pulse (in bpm)', [
        validators.NumberRange(
            min=20, max=300, message='Pulse must be between 20 and 300 bpm'), validators.DataRequired()])
    bloodPressure = DecimalField('Blood Pressure (in mmHg)', [
        validators.NumberRange(
            min=60, max=250, message='Blood pressure must be between 60 and 250 mmHg'), validators.DataRequired()])
    temperature = DecimalField('Temperature (in Fahrenheit)', [
        validators.NumberRange(
            min=70, max=110, message='Temperature must be between 70 and 110 Fahrenheit'), validators.DataRequired()])
    bloodSugar = DecimalField('Blood Sugar (in mg/dL)', [
        validators.NumberRange(
            min=20, max=600, message='Blood sugar must be between 20 and 600 mg/dL'), validators.DataRequired()])
    weight = DecimalField('Weight (in kg)', [
        validators.NumberRange(min=0, max=500, message='Weight must be between 10 and 500 kg'), validators.DataRequired()])
    Prescription = TextAreaField(
        'Prescription', [validators.length(min=10, max=200), validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], validators=[validators.DataRequired(message='Please select a role')])
    submit = SubmitField('Create Account')


class PatientProfileForm(Form):
    name = StringField('Name', [
        validators.Length(
            min=1, max=50, message='Name must be between 1 and 50 characters'),
        validators.DataRequired(message='Name is required')
    ])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], validators=[
                         validators.DataRequired(message='Gender is required')])
    dob = StringField('Date of Birth', [validators.length(min=1, max=10, message='Date of birth must be between 1 and 10 characters'), validators.DataRequired(message='Date of birth is required')]
                      )
    bloodGroup = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), (
        'AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[validators.DataRequired(message='Blood group is required')])
    address = StringField('Address', [
        validators.Length(
            min=1, max=200, message='Address must be between 1 and 200 characters'),
        validators.DataRequired(message='Address is required')
    ])
    phoneNumber = StringField('Phone Number', [
        validators.Regexp(
            regex=r'^\d{10}$', message='Phone number must be a 10-digit number'),
        validators.DataRequired(message='Phone number is required')
    ])
    submit = SubmitField('Submit')
