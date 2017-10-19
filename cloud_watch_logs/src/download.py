import boto3
import botocore
import gzip
import os

def download(export_task):
    
    BUCKET_NAME = 'gridet-logs.us-east-2'
    #OBJECT_KEY = 'export_logs/a848a91f-0e87-46d5-a87c-43e2e9ab7b5a/i-0b46b860b08425190/000000.gz'
    
    objects = []

    client = boto3.client('s3')
    s3 = boto3.resource('s3')

    response = client.list_objects_v2(
        Bucket = BUCKET_NAME
    )

    for k,v in response.items():
        if k == 'Contents':
            for i in v:
                if i['Key'].find(export_task['taskId']) != -1:
                    dist = {}
                    dist['key'] = i['Key']
                    dist['file'] = i['Key'].replace('/','_')
                    objects.append(dist)
    
    file_names = []

    for obj in objects:
        try:
            s3.meta.client.download_file(BUCKET_NAME,obj['key'],os.path.dirname(__file__) + '/tmp/' + obj['file'])
            print('download successful')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('the object does not exist')
                return 
            else:
                raise

        file_content = ''
        with gzip.open(os.path.dirname(__file__) + '/tmp/' + obj['file'], 'rb') as f:
            file_content = f.read()
        
        #print(file_content)
        with open(os.path.dirname(__file__) + '/tmp/' + obj['file'] + '.log', 'wb+') as f:
            f.write(file_content)
        f.close()

        file_names.append(obj['file'] + '.log')

    return file_names

