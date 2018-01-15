
import os
import pprint

import botocore
import botocore.session


REGION = os.getenv('region', 'us-east-2')
ENVIRONMENT_NAME = os.environ['environment_name']
HOSTED_ZONE = os.environ['hosted_zone']
TARGET_DOMAIN = os.environ['target_domain']


def lambda_handler(event, context):
    print('Checking at {} for environment {}...'.format(event['time'], ENVIRONMENT_NAME))

    session = botocore.session.get_session()
    eb_client = session.create_client('elasticbeanstalk', region_name=REGION)
    resources = eb_client.describe_environment_resources(EnvironmentName=ENVIRONMENT_NAME)['EnvironmentResources']
    instance = resources['Instances'][0]['Id']
    print('Found instance {}'.format(instance))

    ec2_client = session.create_client('ec2', region_name=REGION)
    inst_detail = ec2_client.describe_instances(InstanceIds=[instance])['Reservations'][0]['Instances'][0]
    print('Described details of instance {}'.format(instance))

    private_ip = inst_detail['NetworkInterfaces'][0]['PrivateIpAddress']
    print('Private IP is {}'.format(private_ip))

    r53_client = session.create_client('route53')
    record_sets = r53_client.list_resource_record_sets(HostedZoneId=HOSTED_ZONE)['ResourceRecordSets']
    for record in record_sets:
        if record['Name'] == TARGET_DOMAIN:
            value = record['ResourceRecords'][0]['Value']
            if value == private_ip:
                print("Record '{}' has same value {} as current IP address {}".format(TARGET_DOMAIN, value, private_ip))
            else:
                print("Record doesn't match. Changing...")
                r53_client.change_resource_record_sets(
                    HostedZoneId=HOSTED_ZONE,
                    ChangeBatch={
                        'Comment': 'string',
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': {
                                    'Name': 'internal.ceebadmin.',
                                    'Type': 'A',
                                    'ResourceRecords': [
                                        {
                                            'Value': private_ip
                                        },
                                    ],
                                    'TTL': 300,
                                }
                            },
                        ]
                    })
                print("Record changed from {} to {}".format(value, private_ip))
