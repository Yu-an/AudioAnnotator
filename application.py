from flask import Flask, render_template, request,session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import pandas as pd
import numpy as np
import json
import boto3
from database import *
from aws_config import *
from login.login import login_bp
from annotation.annotation import annotation_bp

# Elastic Beanstalk doesn't accept 'app', switching to 'application'
application = Flask(__name__)
application.debug = False


application.config.from_object('config')
# dynamotable and possibly s3
aws_session = boto3.session.Session()
dynamodb = aws_session.resource('dynamodb', region_name=aws_config.AWS_config['region'])
# user_table = dynamodb.Table('MSDUserTable')
# data_table = dynamodb.Table('MSDDataTable')


application.register_blueprint(login_bp, url_prefix='/')
application.register_blueprint(annotation_bp, url_prefix='/annot')




if __name__ == "__main__":
  application.run()