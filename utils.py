import pandas as pd
from io import StringIO
import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json
from database import *
import time

class AnnotationFileNotFoundError(Exception):
    pass   
class AccessAWSError(Exception):
    pass
class WrongSessionError(Exception):
    pass

def get_path_info(s3_path):
    path_is_valid = False
    if s3_path.endswith("/"):
        s3_path = s3_path[:-1]
    parts = s3_path.split("/")
    bucket_name = parts[2]
    # rest of the s3 path without bucket name
    file_prefix = os.path.join(*parts[3:])
    bucket = boto3.resource("s3").Bucket(bucket_name)
    try:
        # Need to check if SQA and TQA are both present
        keys = [obj.key for obj in bucket.objects.filter(Prefix=file_prefix)]
        if len(keys) > 0:
            path_is_valid = True
    except:
        path_is_valid = False
    return path_is_valid, bucket_name, file_prefix


def access_audio(s3_path):
    s3_client = boto3.client("s3")
    path_is_valid, bucket_name, file_prefix = get_path_info(s3_path)
    if path_is_valid:        
        audio_path = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": file_prefix},
            ExpiresIn=3600,
        )
        return audio_path
    else:
        raise AccessAWSError("Access s3 failed",s3_path)
    


def update_dynamodb_table(table, item):
    try:
        response = table.put_item(
        Item=item
        )
        return response['ResponseMetadata']['HTTPStatusCode']
    except ClientError as e:
        raise AccessAWSError(e.response['Error']['Message'])

        
def query_dynamodb_table(table,pk,pk_value,sk=None, sk_value=None):
    # table = dynamodb.Table('TABLENAME')
    if sk:
        try:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_value)&Key(sk).begins_with(sk_value)
                )
            return response['Items']
        except ClientError as e:
            raise AccessAWSError(e.response['Error']['Message'])
    else:
        try:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pk_value)
                )
            return response['Items']
        except ClientError as e:
            raise AccessAWSError(e.response['Error']['Message'])
            

def get_input_file_from_db(data_table, file_name):
    # get data from database    
    input_file_in_data_base = query_dynamodb_table(
                        data_table, 'file_group',
                        'input_file', 'file_id', file_name
                    ) 
    if len(input_file_in_data_base)!=0:
        annation_file = InputFile(
            file_name= file_name, 
            meta_data=input_file_in_data_base[0]['metadata'],
            segments = input_file_in_data_base[0]['segments'],
            target_passes= input_file_in_data_base[0]['target_passes'],
            existing_passes=input_file_in_data_base[0]['existing_passes'],
            audio_path = input_file_in_data_base[0]['audio_path']
        )
        return annation_file
    else:        
       raise AnnotationFileNotFoundError(f"{file_name} not in input.")
   
def prep_input_to_be_output(input_file,user_id):    
    segments = pd.read_json(StringIO(input_file.segments))
    for col in ['valence','valence_comment','arousal','arousal_comment',
                'emotion','emotion_comment','raisedVoice','raisedVoice_comment'
                ]:
        segments[col]=''    
    segments['start'] = segments['start'].astype('str')
    segments['end'] = segments['end'].astype('str')
    # segments = segments.to_dict(orient = 'records')
    annotation_file = OutputFile(            
            file_name = input_file.file_name,
            user_id = user_id,
            audio_path = input_file.audio_path,
            csv_path = input_file.csv_path,
            meta_data= {
                'callType':''
                },
            segments= segments,
            status = 'started'
        ) 
        
    return annotation_file

def check_file_annotation_status(data_table, user_id, file_name):
    # check if the file is already being annotated
    # output a OutputFile class objects
    # grab query results
    file_id = file_name + '---'+ user_id
    
    output_file_in_database = query_dynamodb_table(data_table,
                                            'file_group',
                                            'output_file',
                                            'file_id',
                                            file_id
                                            )
    if len(output_file_in_database)>0:
        # check if the annotation is done by the current user
        # file_name, user_id, audio_path, meta_data,segments,status='started'
        annotation_file = OutputFile(
            file_name = file_name,
            user_id = user_id,
            audio_path = output_file_in_database[0]['audio_path'],
            csv_path = output_file_in_database[0]['audio_path'],
            meta_data= output_file_in_database[0]['metadata'],
            segments= pd.DataFrame(output_file_in_database[0]['segments']),
            status = output_file_in_database[0]['status']
            
        )        
        return annotation_file
    else:
        raise AnnotationFileNotFoundError(f"No output file for {file_name}.")


def validate_file_passes(data_table):
    input_files = query_dynamodb_table(data_table,'file_group','input_file')
    all_unannoated_files = []
    for input_file in input_files:
        filename = input_file['file_id']
        output_files = query_dynamodb_table(data_table,
                                            'file_group',
                                            'output_file',
                                            'file_id',
                                            filename)
        output_files = [file for file in output_files if file['file_name']== filename]
        
        if input_file['existing_passes'] != len(output_files):
            input_file['existing_passes'] = len(output_files)            
            update_dynamodb_table(data_table,input_file)
                        
        if input_file['existing_passes']<input_file['target_passes']:
            all_unannoated_files.append(filename)            
    return all_unannoated_files

def find_unannotated_input_files(data_table):
    try:
        start_time = time.time()
        input_files = query_dynamodb_table(data_table,'file_group','input_file')
        query_input_time = time.time()
        print('query input files:', query_input_time-start_time)
        all_unannoated_files = [file['file_id'] for file in input_files if file['existing_passes']<file['target_passes']]
        
        return all_unannoated_files
    except:
        raise AccessAWSError("Can't access input files; check aws connection")
    
    

def get_user_data(user_id, user_table,data_table,all_unannoated_files): 
    # access db for all user-related data to be saved with session
    ######
    start = time.time()
    #####
    existing_users = query_dynamodb_table(user_table, 'user_id', user_id)
    #####
    retrieve_user = time.time()    
    print('retrieve user: ',retrieve_user-start)
    #####
    if len(existing_users) != 0:
        if 'annotated_files' in existing_users[0].keys():
            annotated_files = existing_users[0]['annotated_files']
        else:        
            output_file_in_database = query_dynamodb_table(data_table,
                                                    'file_group',
                                                    'output_file'
                                                    )
            #####
            retrieve_output_file = time.time()
            print('retrieve output file: ', retrieve_output_file-retrieve_user)
            #####
            # get user's annotation history; file_id doesn't matter
            user_files = [file for file in output_file_in_database if file['annotator']==user_id]
            if len(user_files)!=0:
                annotated_files = {}
                for file in user_files:
                    filename = file['file_name']
                    fileinfo = {}
                    df_i = pd.DataFrame(file['segments'])
                    df_i['dur']=df_i['end'].astype('float')-df_i['start'].astype('float')
                    # add valence stats
                    fileinfo['metadata']= file['metadata']                
                    fileinfo['status'] = file['status']
                    annotated_files[filename]= fileinfo
                    
                # df_user = pd.concat(dfs)
                # annotated files have the amount of pos/neg/neu valence and status for each file
                
            else:
                annotated_files = {}
        
        unannotated_files = [file for file in all_unannoated_files if file not in annotated_files.keys()]
        #######
        retrieve_unannotated_files = time.time()
        print('retrieve unannotated files,', retrieve_unannotated_files-retrieve_output_file)
        ######
        u = existing_users[0]
        user_data = UserData(user_id = u['user_id'], 
                                first_name = u['first_name'],
                                qualified = u['qualified'],
                                roles = u['roles'],
                                annotated_files= annotated_files,
                                unannotated_filenames=unannotated_files
                                )
        return user_data




if __name__ == "__main__":
    session = boto3.session.Session()
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    
    
