import boto3

def main():
    transcribe_client = boto3.client('transcribe')
    response = transcribe_client.create_language_model(
        LanguageCode='en-US',
        BaseModelName='WideBand',
        ModelName='TestModel',
        InputDataConfig={
            'S3Uri': 'string',
            'TuningDataS3Uri': 'string',
            'DataAccessRoleArn': 'string'
        },
    )

if __name__ == '__main__':
    main()
