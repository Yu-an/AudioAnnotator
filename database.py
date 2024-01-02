import boto3


class UserData:
    def __init__(self, user_id,first_name, qualified, roles=None, annotated_files = None,unannotated_filenames = None):
        self.user_id = user_id  # String attribute
        self.first_name = first_name # String
        self.roles = roles if roles is not None else []  # List attribute with default value []
        self.qualified = qualified  # String attribute
        self.annotated_files = annotated_files if annotated_files is not None else []  # List attribute with default value []
        self.unannotated_filenames = unannotated_filenames if unannotated_filenames is not None else []  # List attribute with default value []
    def to_dict(self):
        user_item = {
            'user_id':self.user_id,
            'first_name':self.first_name,
            'roles':self.roles,
            'qualified':self.qualified,
            'annotated_files':self.annotated_files,
            'unannotated_filenames':self.unannotated_filenames
        }
        return user_item

class OutputFile:
    def __init__(self,file_name, user_id, audio_path, meta_data,segments,status='started', csv_path = None):
        self.file_group = 'output_file' #pk
        self.file_id = file_name+'---'+user_id #sk, {file_name}---{user_id}
        self.file_name = file_name # str
        self.annotator = user_id #str
        self.audio_path = audio_path #str
        self.metadata = meta_data #dict
        self.segments = segments #list
        self.status = status
        self.csv_path = csv_path    
    def to_dict(self):
        output_item = {'file_group': self.file_group,
                    # need to add username
                    "file_id":self.file_id,
                    'annotator':self.annotator,
                    "file_name":self.file_name,
                    'status': self.status,
                    'audio_path':self.audio_path,
                    "metadata":self.metadata,
                    "segments": self.segments,
                    "csv_path":self.csv_path
                    }
        return output_item
        
class InputFile:
    def __init__(self,file_name, audio_path, meta_data,segments, target_passes=2,existing_passes=0, csv_path = None):
        self.file_group = 'input_file' #pk
        self.file_id = file_name #sk, begins_with{file_name}
        self.file_name = file_name #str
        self.audio_path = audio_path #str
        self.metadata = meta_data #dict
        self.segments = segments #list
        self.target_passes = target_passes #int
        self.existing_passes = existing_passes #int
        self.csv_path = csv_path
    def to_dict(self):
        input_item = {
            'file_group': self.file_group,
            'file_id': self.file_name,
            'file_name':self.file_name,
            'audio_path':self.audio_path,
            'metadata':self.metadata,
            'segments':self.segments,
            'target_passes': self.target_passes,
            'existing_passes': self.existing_passes,
            'csv_path': self.csv_path
        }
        return input_item


if __name__ == 'main':
    # Initialize a session using Amazon DynamoDB
    session = boto3.session.Session()
    dynamodb = session.resource('dynamodb', region_name='us-east-1')  # Change region if necessary
    s3 = session.client('s3', region_name='us-east-1')


# utils.query_dynamodb_table(table,pk,pk_value,sk=None, sk_value=None)
# utils.update_dynamodb_table(table,item)



# def query_dynamodb_table(table,pk,pk_value,sk=None, sk_value=None):
#     # table = dynamodb.Table('TABLENAME')
#     if sk:
#         try:
#             response = table.query(
#                 KeyConditionExpression=Key(pk).eq(pk_value)&Key(sk).begins_with(sk_value)
#                 )
#             return response['Items']
#         except ClientError as e:
#             print(e.response['Error']['Message'])
#     else:
#         try:
#             response = table.query(
#                 KeyConditionExpression=Key(pk).eq(pk_value)
#                 )
#             return response['Items']
#         except ClientError as e:
#             print(e.response['Error']['Message'])

