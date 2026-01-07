import json
import boto3
import os
from botocore.exceptions import ClientError

quicksight = boto3.client('quicksight')

def handler(event, context):
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': os.environ['ALLOWED_DOMAIN'],
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }
    
    # Handle preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        body = json.loads(event.get('body', '{}'))
        user_arn = body.get('userArn')
        topic_id = body.get('topicId')  # Q Topic ID for GenerativeQnA
        account_id = context.invoked_function_arn.split(':')[4]
        allowed_domain = os.environ['ALLOWED_DOMAIN']
        
        if not user_arn:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'userArn is required'})
            }
        
        if not topic_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'topicId is required'})
            }
        
        # Build experience configuration for GenerativeQnA
        experience_config = {
            'GenerativeQnA': {
                'InitialTopicId': topic_id
            }
        }
        
        # Generate embed URL for registered user with GenerativeQnA experience
        response = quicksight.generate_embed_url_for_registered_user(
            AwsAccountId=account_id,
            UserArn=user_arn,
            ExperienceConfiguration=experience_config,
            AllowedDomains=[allowed_domain],
            SessionLifetimeInMinutes=600
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'embedUrl': response['EmbedUrl']
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
