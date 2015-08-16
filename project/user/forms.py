# project/user/forms.py
from flask_wtf import Form
from wtforms import TextField, PasswordField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

from project.models import User, Job
from flask.ext.login import current_user
import datetime
from project import db
from crn_validator import is_valid_crn
from project import browser
from flask import flash

class LoginForm(Form):
    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

class crnForm(Form):
    crn = TextField('crn', validators=[Length(5), Optional()])    
    def validate_crn(self):
        if self.crn.data != '' and not is_valid_crn(browser, self.crn.data):
            flash(self.crn.data+': Invalid crn. Please check and try again!', 'danger')
            return False
        jobs = Job.query.filter_by(user_id=current_user.id).all()
        for job in jobs:
            if self.crn.data == str(job.crn):
                flash(self.crn.data+': Class already being tracked!', 'danger')
                return False
        return True

    def validate(self):
        return self.validate_crn()

class PickingClassForm(Form):
    crns = FieldList(FormField(crnForm), min_entries=5, max_entries=5)
    
    def validate(self):
        jobs = Job.query.filter_by(user_id=current_user.id).all()
        form_count = 0
        for crn in self.crns:
            if crn.data['crn'] != '':
                form_count+=1
        job_count = len(jobs) + form_count
        if job_count > 5:
            flash('Sorry, You can monitor at most 5 courses!', 'danger')
            return False
        else:
            return all([crn.validate_crn() for crn in self.crns])


