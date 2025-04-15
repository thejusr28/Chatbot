import json
import boto3
import os

# Environment Variables in Lambda
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "Z9BHRGIBXW")
MODEL_ARN = os.environ.get("MODEL_ARN", "arn:aws:bedrock:ap-south-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0")

client = boto3.client("bedrock-agent-runtime", region_name="ap-south-1")

def lambda_handler(event, context):
    # Handle preflight request for CORS
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }

    try:
        body = json.loads(event.get("body", "{}"))
        question = body.get("question", "").strip()

        if not question or question.lower() in ["hi", "hello", "hey", "start"]:
            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({
                    "answer": "👋 Welcome to the AWS Customer Support Bot! Ask me anything about AWS services, pricing, or best practices."
                })
            }

        response = client.retrieve_and_generate(
            input={"text": question},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )

        answer = response.get("output", {}).get("text", "🤖 Sorry, I couldn't find an answer.")

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"answer": answer})
        }

    except Exception as e:
        print("❌ Error:", e)
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": str(e)})
        }
