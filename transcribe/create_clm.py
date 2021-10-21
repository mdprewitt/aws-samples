import argparse
import logging
import os
from pathlib import PurePosixPath as PosixPath, Path

import boto3
from botocore.exceptions import ClientError


def main(clm_dir, bucket, role_arn):
    s3_client = boto3.client('s3')
    model_name = "TestModel2"
    model_prefix = model_name
    for root, dirs, files in os.walk(clm_dir):
        root_path = Path(root)
        for clm_file in files:
            file = str(root_path / clm_file)
            try:
                print(f"upload {file}")
                s3_client.upload_file(file, bucket, f"{model_prefix}/{PosixPath(clm_file).name}")
            except ClientError as e:
                logging.error(e)

    transcribe_client = boto3.client('transcribe')
    s3_uri = "s3://" + str(PosixPath(bucket) / model_prefix)
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
    parser.add_argument("dir")
    parser.add_argument("bucket")
    parser.add_argument("role")
    args = parser.parse_args()
    main(args.dir, args.bucket, args.role)
