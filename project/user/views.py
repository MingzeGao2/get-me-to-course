# project/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, json
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User, Job
# from project.email import send_email
from project import db, bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PickingClassForm
from project.token import generate_confirmation_token, confirm_token
import datetime
from project.email import send_email
from project.decorators import check_confirmed
# from config import basedir
################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        print form.password.data
        user = User(
            email=form.email.data,
            password=form.password.data,
            confirmed = False
       )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url )
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')

        return redirect(url_for("user.unconfirmed"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    print "confirm email"
    try:
        email = confirm_token(token)
        print "email is" + email
    except:
        print "confirm failed"
        flash('The confirmation link is invalid or has expired', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    print "user" , user
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your accound!', 'warning')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/job', methods=['GET', 'POST'])
@login_required
@check_confirmed
def job():
    
    jobs = Job.query.filter_by(user_id=current_user.id) 
    
    form = PickingClassForm(request.form)

    # crn_list = {}
    if form.validate_on_submit():
        for crn in form.crns:
            for field in crn:
                if field.data != '' and field.data != None and field.data != 'None': #and form.validate_crn(field.data):
                    job = Job(field.data, datetime.datetime.now(), current_user.id)
                    db.session.add(job)
        db.session.commit()

    # delroute = basedir + "/deletejob"

    return render_template('user/job.html', jobs=jobs, form=form)#, delroute=delroute)


@user_blueprint.route('/deletejob', methods=['POST'])
@login_required
@check_confirmed
def deljob():
    print request
    print request.json
    print request.json['jobcrn']
    jobcrn = int(str(request.json['jobcrn']))
    print jobcrn
    # try:
    jobs = Job.query.filter_by(user_id=current_user.id, crn=jobcrn)
    for job in jobs:
        db.session.delete(job)
        db.session.commit()
    return json.dumps({'status':'OK'})
    # except:
        # return json.dumps({'status':'NOPE'})


@user_blueprint.route('/populate')
@login_required
def populate():
    job1 = Job(36091, datetime.datetime.now(), current_user.id)
    job2 = Job(43357, datetime.datetime.now(), current_user.id)
    job3 = Job(30128, datetime.datetime.now(), current_user.id)
    job4 = Job(65086, datetime.datetime.now(), current_user.id)
    db.session.add(job1)
    db.session.add(job2)
    db.session.add(job3)
    db.session.add(job4)

    db.session.commit()
    return redirect(url_for('user.job'))


@user_blueprint.route('/clean')
def clean():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.login'))


