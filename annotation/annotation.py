from flask import Blueprint, render_template, request,url_for,jsonify, session, flash
from flask import current_app as app
import json
import boto3
from io import StringIO
import pickle
import pandas as pd
from utils import *
from database import *

aws_session = boto3.session.Session()
dynamodb = aws_session.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('MSDUserTable')
# data_table = dynamodb.Table('MSDDataTable')

annotation_bp = Blueprint('annotation_bp', __name__,
    template_folder='templates',
    static_folder='static')

@annotation_bp.route('/<file_name>',methods = ('GET', 'POST'))
def annot(file_name):
    
    annot_url =  url_for('annotation_bp.annot', file_name=file_name)
    review_url = url_for('annotation_bp.review_annot', file_name=file_name)

    user_id = session.get('user_id')
    if user_id==None:
        user_id = 'yuanyg' #for testing

    
    # add segment info
    if request.method == 'POST':       
        try:            
            # Process the request data (can we do this with class?)
            segments = request.get_json()            
            annotation_file.segments = segments            
            data_item = annotation_file.to_dict()    
            update_dynamodb_table(data_table,data_item)
            annotation_file.segments = pd.DataFrame(segments)
            # print(f'after post for {attribute};', annotation_file.segments[attribute].to_list())            
            # If everything is successful, return a JSON response (don't do HTML!)
            return jsonify({"success": True, "message": "Data saved successfully"})
        except ClientError as e:            
            return jsonify({"success": False, "message": "DynamoDB error"}), 500
        except Exception as e:            
            return jsonify({"success": False, "message": "Unexpected error"}), 500


    return render_template('annotation/annot.html',                       
                        file_name = file_name,
                        emotion_attributes=emotion_attributes, 
                        transcript=transcript,
                        audio_path=audio_path,
                        msd_annot_url = msd_annot_url,
                        msd_review_url = msd_review_url
                        )


@annotation_bp.route("/<file_name>/review", methods=('GET', 'POST'))
def msd_review_annot(file_name):
    # page to display all segment labels
    user_id = session.get('user_id')
    if user_id==None:
        user_id = 'yuanyg' #for testing
    # user_data = pickle.loads(session.get('user_data'))
    # access annotated file from database

    annotation_file = check_file_annotation_status(data_table,user_id, file_name)
        
    # annotation_file = check_file_annotation_status(data_table,user_id, file_name)
    segments = annotation_file.segments
    metadata = annotation_file.metadata
    audio_path = access_audio(annotation_file.audio_path)
    msd_annot_url =  url_for('annotation_bp.msd_annot', file_name=file_name)
    msd_review_url = url_for('annotation_bp.msd_review_annot', file_name=file_name)
    my_tasks_url = url_for('mytasks_bp.list_tasks')
    if (request.method == 'POST'):
        try:                           
            annotated_data = request.get_json()                     
            # Process the request data (can we do this with class?)  
            annotation_file.segments = annotated_data['segments']
            annotation_file.metadata['callType'] = annotated_data['metadata']
            annotation_file.status = 'done'
            data_item = annotation_file.to_dict()
            update_dynamodb_table(data_table,data_item)
            annotation_file.segments = pd.DataFrame(segments)            
            # update_dynamodb_table(data_table,input_item)
            # If everything is successful, return a JSON response (don't do HTML!)
            return jsonify({"success": True, "message": "Data saved successfully"})
        except ClientError as e:            
            return jsonify({"success": False, "message": "DynamoDB error"}), 500
        except Exception as e:            
            return jsonify({"success": False, "message": "Unexpected error"}), 500
    
    
    return render_template('annotation/annot_viewall.html',
                           segments = segments,
                           file_name=file_name,
                           metadata = metadata,   
                           audio_path = audio_path,
                           msd_annot_url = msd_annot_url,
                           msd_review_url = msd_review_url,
                           my_tasks_url = my_tasks_url
                           )