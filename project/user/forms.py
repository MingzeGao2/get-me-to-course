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
        print "This is the type of email",type(self.email)
        print "This is the type of email.errors",type(self.email.errors)
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
        print "This is the type of crn", type(self.crn)
        print "This is the type of crn.errors:", type(self.crn.errors)
        # valid = True
        # print mycrn
        if self.crn.data != '' and not is_valid_crn(browser, self.crn.data):
            print type(self.crn.data)
            print self.crn.data
            # print mycrn
            # print crn.value
            # self.crn.errors.append(self.crn.data+': Invalid crn. Please check and try again!')
            flash(self.crn.data+': Invalid crn. Please check and try again!')
            return False
        jobs = Job.query.filter_by(user_id=current_user.id)
        if self.crn.data in [job.crn for job in jobs]:
            # self.crn.errors.append(self.crn.data+': Class already being tracked!')
            flash(self.crn.data+': Class already being tracked!')
            return False
        return True

    def validate(self):
        # print "AHHHHHHHHHH!!!", self.crn.data
        # initial_validation = super(crnForm, self).validate()
        # if not initial_validation:
            # return False
        # print "BBBHHHHHHHHHHH!!!", self.crn.data
        valid = self.validate_crn()
        return valid

class PickingClassForm(Form):
    # crn1 = TextField('crn1', validators=[Length(5)])
    # crn2 = TextField('crn2', validators=[Length(5)])
    # crn3 = TextField('crn2', validators=[Length(5)])
    # crn4 = TextField('crn2', validators=[Length(5)])
    # crn5 = TextField('crn2', validators=[Length(5)])
    crns = FieldList(FormField(crnForm), min_entries=5, max_entries=5)
# Do we need at least one class filled out ???


    # for crn in self.crns:
    #     for field in crn:
    #         valid = valid & self.validate_crn(field.data)
    # return valid





