import json
import boto3
import urllib.parse
import uuid
import re

bedrock_agent = boto3.client('bedrock-agent')

KB_ID = "Z9BHRGIBXW"
DATA_SOURCE_ID = "FGQXLMKCAP"

def generate_client_token(key):
    base = key.replace("/", "-").replace(".", "-")
    base = re.sub(r'[^a-zA-Z0-9-]', '', base)
    base = re.sub(r'-+', '-', base)
    base = base.strip('-')

    suffix = str(uuid.uuid4()).replace("-", "")
    token = f"{base}-{suffix}"[:256]
    return token

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    try:
        detail = event.get('detail', {})
        bucket = detail.get('bucket', {}).get('name')
        key = detail.get('object', {}).get('key')

        if not bucket or not key:
            raise ValueError("Missing bucket or key in the event")

        key = urllib.parse.unquote_plus(key)
        s3_uri = f"s3://{bucket}/{key}"
        print(f"Processing uploaded file: {s3_uri}")

        client_token = generate_client_token(key)

        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=KB_ID,
            dataSourceId=DATA_SOURCE_ID,
            clientToken=client_token
        )

        print("Ingestion job started:", response['ingestionJob'])
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Ingestion started for {key}",
                'ingestionJobId': response['ingestionJob']['ingestionJobId']
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
