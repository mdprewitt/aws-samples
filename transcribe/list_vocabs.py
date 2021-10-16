import boto3
from .basics import list_vocabularies


def main():
    transcribe_client = boto3.client('transcribe')
    print("Vocabs: ", list_vocabularies(transcribe_client))


if __name__ == '__main__':
    main()
