import json
import boto3
import logging
import os
import re
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# get region for the lambda function
region = os.environ['AWS_REGION']

# Create SES client once outside the handler for better performance
ses_client = boto3.client('ses', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    try:
        # Parse request body once
        request_object = json.loads(event['body'])        
        dst_address = os.environ.get('DST_ADDR', None)
        src_address = os.environ.get('SRC_ADDR', None)
        if dst_address is None or src_address is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required email configuration parameters')
            }
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, dst_address):
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid dst email address')
            }

        if not re.fullmatch(regex, src_address):
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid src email address')
            }

        email_content = request_object.get('content')

        # scrub the email_content for malicious content
        email_content = email_content.replace('\r', '')
        #scrub the email_content which can execute any code
        email_content = email_content.replace('eval(', '').replace('exec(', '')
        
        # Validate required fields
        if not all([dst_address, email_content]):
            return {
                'statusCode': 400,
                'body': json.dumps('Missing required email parameters')
            }

        # Use a constant for email configuration
        email_params = {
            'Destination': {
                'ToAddresses': [dst_address]
            },
            'Message': {
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': email_content,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Test email',
                },
            },
            'Source': src_address
        }

        response = ses_client.send_email(**email_params)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Email Sent Successfully',
                'messageId': response['MessageId']
            })
        }
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON in request body')
        }
    except Exception as e:
        logger.error(e)
        logger.error(f"Error sending email: Please contact your admin")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email')
        }
