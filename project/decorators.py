from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user
from project.models import User, Job

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user_confirm = User.query.filter_by(id=current_user.id).first().confirmed
        if current_user_confirm is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
