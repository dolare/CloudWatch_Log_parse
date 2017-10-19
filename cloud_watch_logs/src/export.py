#aws logs create-export-task --task-name "my-log-group-09-10-2015" --log-group-name "my-log-group" --from 1441490400000 --to 1441494000000 --destination "my-exported-logs" --destination-prefix "export-task-output"
import boto3
import time

def export(startTime, endTime):
    client = boto3.client('logs',region_name='us-east-2')
    time1 = startTime
    time2 = endTime

    #logStreamNamePrefix = 'i-0cb550a382a606172'

    response = client.create_export_task(
        taskName = 'logs-export-task-from {} to {}'.format(time1, time2),
        logGroupName = '/aws/elasticbeanstalk/upgrid-web/var/log/app/service.log',
        #logStreamNamePrefix = logStreamNamePrefix,
        fromTime = time1,
        to = time2,
        destination = 'gridet-logs.us-east-2',
        destinationPrefix = 'export_logs'
    )

    export_task = {}
    export_task['taskId'] = response['taskId']
    #export_task['logStreamNamePrefix'] = logStreamNamePrefix

    return export_task
