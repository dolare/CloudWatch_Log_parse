import boto3
import botocore
import gzip


def download(export_task,target):
    
    BUCKET_NAME = 'gridet-logs.us-east-2'
    #OBJECT_KEY = 'export_logs/a848a91f-0e87-46d5-a87c-43e2e9ab7b5a/i-0b46b860b08425190/000000.gz'
    OBJECT_KEY = 'export_logs/' + export_task['taskId'] + '/' + export_task['logStreamNamePrefix']  + '/000000.gz'

    print(OBJECT_KEY)
    client = boto3.client('s3')
    s3 = boto3.resource('s3')

    response = client.list_objects_v2(
        Bucket = BUCKET_NAME
    )


    try:
        s3.meta.client.download_file(BUCKET_NAME,OBJECT_KEY,'.tmp/service.gz')
        print('download successful')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('the object does not exist')
            return 
        else:
            raise

    file_content = ''
    with gzip.open('.tmp/service.gz', 'rb') as f:
        file_content = f.read()

    #print(file_content)
    file_name = target
    with open(file_name, 'wb+') as f:
        f.write(file_content)
    f.close()

    return file_name

