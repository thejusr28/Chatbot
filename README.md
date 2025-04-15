# Chatbot

ARCHITECTURE OVERVIEW

 
DEPLOYMENT
This solution implements a serverless, scalable, and intelligent chatbot using AWS services. Below is the detailed architecture and workflow:
1.	Frontend Hosting via CloudFront and S3
The chatbot frontend is hosted on Amazon S3 and delivered securely and globally using Amazon CloudFront. Users access the chatbot interface through this setup.
2.	API Integration
The frontend communicates with a backend API that is integrated with an AWS Lambda function. This API acts as the bridge between the user interface and the underlying AI model.
3.	Lambda Function with Bedrock Integration
The Lambda function contains:
o	Configuration for the Amazon Bedrock Knowledge Base (KB)
o	Details of the foundation model used for generating chatbot responses (e.g., Claude 3 via Bedrock)
o	Logic for invoking the Bedrock API to process user inputs and return relevant responses
4.	Knowledge Base Setup
The Knowledge Base in Amazon Bedrock is created using:
o	Amazon Titan Embeddings for converting documents into vector format
o	Amazon OpenSearch for storing and performing similarity search on vector embeddings
o	Amazon S3 as the primary storage for source documents
5.	Event-Driven Sync with EventBridge
An Amazon EventBridge rule is configured to monitor the S3 bucket. Whenever a new document is uploaded:
o	EventBridge triggers an update
o	The document is automatically embedded using Titan and synced to OpenSearch
o	This ensures the KB remains up to date with the latest documents without manual intervention
