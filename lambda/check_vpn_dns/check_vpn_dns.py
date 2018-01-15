from __future__ import print_function

import json
import os
import socket
import traceback
from datetime import datetime
from cStringIO import StringIO

import botocore
import boto3
from botocore.exceptions import ClientError

SITE = os.environ['site']
GROUPS = os.environ['groups']

BUCKET = os.environ['s3_bucket']
KEY = os.getenv('s3_key', 'whitelist_ip')
REGION = os.getenv('region', 'us-east-2')
KEY_CURRENT_IP = 'current_ip'

KEY_IP_PROTOCOL = 'IpProtocol'
KEY_FROM_PORT = 'FromPort'
KEY_TO_PORT = 'ToPort'
KEY_IP_RANGES = 'IpRanges'
KEY_CIDR_IP = 'CidrIp'

IP_PROTOCOL = 'tcp'
PORTS = [80, 443,]
IP_RANGE_TEMPLATE = "{}/32"


def handler(event, context):
    print('Checking at {}...'.format(event['time']))
    current_address = socket.gethostbyname(SITE)

    s3 = boto3.resource('s3')
    s3_obj = s3.Object(BUCKET, KEY)
    try:
        raw_content = s3_obj.get()['Body'].read()
        content = json.loads(raw_content)
        print("Read previous config.")
    except Exception as ex:
        if isinstance(ex, ClientError) and ex.response['Error']['Code'] == 'NoSuchKey':
            print("No previous config.")
        else:
            traceback.print_exc()
            print("Cannot read previous config")
        content = dict()

    group_ids = GROUPS.split(',')
    previous_address = content.get(KEY_CURRENT_IP, None)
    if previous_address != current_address:
        if previous_address:
            # remove old ip
            _adjust_ip(previous_address, group_ids, is_removal=True)

        # add new ip
        _adjust_ip(current_address, group_ids, is_removal=False)

        content[KEY_CURRENT_IP] = current_address
        raw_content = json.dumps(content)
        stream_handle = StringIO(raw_content)
        s3_obj.put(Body=stream_handle)
        print("Uploaded new config.")
    else:
        print("No change detected")

    print('Check complete at {}'.format(str(datetime.now())))
    return event['time']


def _gen_ip_permissions(ip_address):
    ip_permissions = list()
    for port in PORTS:
        rule = dict()
        rule[KEY_IP_PROTOCOL] = IP_PROTOCOL
        rule[KEY_FROM_PORT] = port
        rule[KEY_TO_PORT] = port

        ranges = dict()
        ranges[KEY_CIDR_IP] = IP_RANGE_TEMPLATE.format(ip_address)
        rule[KEY_IP_RANGES] = list()
        rule[KEY_IP_RANGES].append(ranges)

        ip_permissions.append(rule)

    return ip_permissions


def _adjust_ip(ip_address, group_ids, is_removal=False):
    session = botocore.session.get_session()
    client = session.create_client('ec2', region_name=REGION)
    ip_permissions = _gen_ip_permissions(ip_address)
    for group_id in group_ids:
        if is_removal:
            try:
                client.revoke_security_group_ingress(GroupId=group_id,
                                                     IpPermissions=ip_permissions)
                print("Removed old rules from group {}".format(group_id))
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'InvalidPermission.NotFound':
                    print("No existing rule. Skipping removal.")
                else:
                    raise

        else:
            try:
                client.authorize_security_group_ingress(GroupId=group_id,
                                                        IpPermissions=ip_permissions)
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'InvalidPermission.Duplicate':
                    print("Added new rules to group {}".format(group_id))
                else:
                    raise

