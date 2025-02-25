import json
import boto3
import os

ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
S3_BUCKET = os.environ['S3_BUCKET']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Extract input from the event
    user_id = event['user_id']
    input_text = event['input_text']
    recording = event['recording']  # Assuming the recording is passed as a base64-encoded string
    
    # Upload the recording to S3
    upload_to_s3(user_id, recording)
    
    # Call GPT-4 model (assuming you have an endpoint set up)
    response = call_gpt4_model(input_text)
    
    # Save the outline to DynamoDB
    save_outline_to_dynamodb(user_id, response['outline'])
    
    # Send confirmation notification via SNS
    send_confirmation_sns(user_id)
    
    # Process the response and return
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def upload_to_s3(user_id, recording):
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f'recordings/{user_id}.wav',
        Body=recording
    )

def call_gpt4_model(input_text):
    client = boto3.client('sagemaker-runtime')
    try:
        response = client.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps({'input_text': input_text})
        )
        result = json.loads(response['Body'].read().decode())
        return result
    except Exception as e:
        return {"error": str(e)}

def save_outline_to_dynamodb(user_id, outline):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.put_item(
        Item={
            'UserId': user_id,
            'Outline': outline
        }
    )

def send_confirmation_sns(user_id):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f'Outline for user {user_id} has been successfully stored in DynamoDB.'
    )