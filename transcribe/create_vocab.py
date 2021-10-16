import boto3
from .basics import create_vocabulary, list_vocabularies, update_vocabulary


def main():
    transcribe_client = boto3.client('transcribe')
    vocab_name = "TestVocab"

    vocabs = list_vocabularies(transcribe_client, vocabulary_filter=vocab_name)
    if vocabs:
        update_vocabulary(vocab_name, "en-US", transcribe_client=transcribe_client,
                          phrases=["capon", "lined", "slippered", "sans"])
    else:
        create_vocabulary(vocab_name, "en-US", transcribe_client=transcribe_client,
                          phrases=["capon", "lined", "slippered", "sans"])


if __name__ == '__main__':
    main()
