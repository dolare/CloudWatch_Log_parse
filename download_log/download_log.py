from datetime import datetime
import errno
import grp
import logging
import os
import pwd
import re

import boto3

# boto3.set_stream_logger(level=logging.DEBUG)
# boto3.set_stream_logger(level=logging.DEBUG, name='botocore')

SOURCE_BUCKET_NAME = "elasticbeanstalk-us-east-1-952527030977"
LOG_PREFIX = "resources/environments/logs/publish/"
ENV_PREFIX = LOG_PREFIX + "e-qy2e34tuxh/"

TARGET_BUCKET_NAME = "ceebman"
TARGET_PREFIX = "logs/ceebadmin"

LOG_OWNER = "ark"
LOCAL_LOG_ROOT_DIR = '/home/loguser'
LOCAL_LOG_DIR = LOCAL_LOG_ROOT_DIR + '/ceebadmin'

LOG_FILENAME_REGEX = re.compile("([0-9a-zA-Z\-\_\.]+)([0-9]{10})\.gz")

logger = logging.getLogger("log_mover")


def setup_logger(logger):
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def get_sub_prefix(s3client, bucket_name, prefix, delimiter='/'):
    prefixes = []
    paginator = s3client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket_name, Delimiter=delimiter, Prefix=prefix):
        for prefix in result.get('CommonPrefixes'):
            prefixes.append(prefix.get('Prefix'))
    return prefixes


def main():
    uid = pwd.getpwnam(LOG_OWNER).pw_uid
    gid = grp.getgrnam(LOG_OWNER).gr_gid

    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    instance_prefixes = get_sub_prefix(client, SOURCE_BUCKET_NAME, ENV_PREFIX)

    source_bucket = s3.Bucket(SOURCE_BUCKET_NAME)
    target_bucket = s3.Bucket(TARGET_BUCKET_NAME)
    for instance_prefix in instance_prefixes:
        instance_id = instance_prefix.split('/')[-2]
        logger.info("Processing logs from instance {0}".format(instance_id))

        logfile_objects = source_bucket.objects.filter(Delimiter='/', Prefix=instance_prefix).limit(count=2)

        for logfile_object in logfile_objects:
            source_key = logfile_object.key
            filename = source_key.split('/')[-1]

            match_result = LOG_FILENAME_REGEX.search(filename)
            if match_result:
                logger.info("Processing log of s3://{0}/{1}".format(SOURCE_BUCKET_NAME, source_key))
                log_name = match_result.group(1)
                timestamp = int(match_result.group(2))

                log_datetime = datetime.fromtimestamp(timestamp)
                sub_path = "/".join(
                    [str(log_datetime.year), str(log_datetime.month), str(log_datetime.day), str(log_datetime.hour)])
                target_filename = log_name + "." + instance_id + ".gz"
                logger.info("Target file path name is {0}/{1}".format(sub_path, target_filename))

                target_key = "/".join([TARGET_PREFIX, sub_path, target_filename])
                target_obj = target_bucket.Object(target_key)
                logger.info("Copying log to s3://{0}/{1}".format(TARGET_BUCKET_NAME, target_key))
                target_obj.copy({
                    'Bucket': SOURCE_BUCKET_NAME,
                    'Key': source_key
                })

                source_obj = source_bucket.Object(source_key)

                local_path = "/".join([LOCAL_LOG_DIR, sub_path])
                mkdir_p(local_path)
                local_pathname = "/".join([local_path, target_filename])
                logger.info("Downloading log to {0}".format(local_pathname))
                source_obj.download_file(local_pathname)
                chdirown(LOCAL_LOG_ROOT_DIR, uid, gid)

                current_time = datetime.now()
                retention_time = datetime(current_time.year,
                                          current_time.month,
                                          current_time.day,
                                          current_time.hour - 2,
                                          0,
                                          0,
                                          0,
                                          current_time.tzinfo)
                retention_timestamp = (retention_time - datetime(1970, 1, 1)).total_seconds()
                if retention_timestamp < timestamp:
                    logger.info("Keep source file as it's still young.")
                else:
                    logger.info("Deleted source file.")
                    # source_obj.delete()

            else:
                logger.info("cannot match file name {0}".format(filename))


def mkdir_p(path):
    try:
        os.makedirs(path, 0700)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def chdirown(path, uid, gid):
    os.chown(path, uid, gid)
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isfile(itempath):
            os.chown(itempath, uid, gid)
        elif os.path.isdir(itempath):
            os.chown(itempath, uid, gid)
            chdirown(itempath, uid, gid)


if __name__ == "__main__":
    setup_logger(logger)
    main()
