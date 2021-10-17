import argparse
import logging
from pathlib import PurePosixPath as Path

import boto3
from botocore.exceptions import ClientError


def main(clm_file, bucket, role_arn):
    s3_client = boto3.client('s3')
    model_name = "TestModel"
    model_prefix = model_name
    try:
        s3_client.upload_file(clm_file, bucket, f"{model_prefix}/{Path(clm_file).name}")
    except ClientError as e:
        logging.error(e)

    transcribe_client = boto3.client('transcribe')
    s3_uri = "s3://" + str(Path(bucket) / model_prefix)
    logging.info("uploading to %s", s3_uri)
    response = transcribe_client.create_language_model(
        LanguageCode='en-US',
        BaseModelName='WideBand',
        ModelName=model_name,
        InputDataConfig={
            'S3Uri': s3_uri,
            # 'TuningDataS3Uri': 'string',
            'DataAccessRoleArn': role_arn
        },
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("bucket")
    parser.add_argument("role")
    args = parser.parse_args()
    main(args.file, args.bucket, args.role)
