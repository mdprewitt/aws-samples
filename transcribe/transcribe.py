# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use AWS SDK for Python (Boto3) to call Amazon Transcribe to make a
transcription of an audio file.

This script is intended to be used with the instructions for getting started in the
Amazon Transcribe Developer Guide here:
    https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-python.html.
"""

import time
import boto3
import argparse


def transcribe_file(job_name, file_uri, transcribe_client, redact=False):
    transcribe_client.delete_transcription_job(
        TranscriptionJobName=job_name,
    )
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        ContentRedaction={
            "RedactionType": "PII",
            "RedactionOutput": "redacted",
        },
        Settings={
            "VocabularyName": "TestVocab",
        },
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def main(file_uri, redact=False):
    transcribe_client = boto3.client('transcribe')
    transcribe_file('Example-job', file_uri, transcribe_client, redact)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--redact", action="store_true")
    args = parser.parse_args()

    main(file_uri=args.file, redact=args.redact)
