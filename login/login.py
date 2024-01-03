import boto3
from flask import Blueprint,redirect,jsonify,url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from utils import *
import aws_config
import pickle
from database import *

login_bp = Blueprint('login_bp', __name__,
    template_folder='templates',
    static_folder='static')

aws_session = boto3.session.Session()
dynamodb = aws_session.resource('dynamodb', region_name=aws_config.AWS_config['region'])
user_table = dynamodb.Table('MSDUserTable')
# data_table = dynamodb.Table('MSDDataTable')


class LoginForm(FlaskForm):
    text_input = StringField('Enter user id', [validators.DataRequired()])
    submit_button = SubmitField('Submit')
    
@login_bp.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_id = form.text_input.data
        if "@" in user_id:
            user_id = user_id.split('@')[0]
        session['user_id'] = user_id
        try:
            existing_users = query_dynamodb_table(user_table, 'user_id', user_id)
            if len(existing_users)!=0:            
                return redirect(url_for('mytasks_bp.list_tasks'))
        except:
            return render_template('login/login.html', form=form, login_failed=True)
    return render_template('login/login.html', form=form, login_failed=False)


@login_bp.route("/welcome", methods=('GET', 'POST'))
def home():
  # user_id = request.remote_user
  user_data = pickle.load(session.get('user_data'))
  first_name = user_data.first_name
  if first_name==None:
      first_name = session.get('user_id')
  return render_template("home.html",
                         first_name = first_name
                         )


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_bp.login'))


# use flask-wtf and flask-login?
