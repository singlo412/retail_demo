import boto3
import json
import logging

import qbiz

# Configure logging with basic settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

creds = qbiz.get_credentials()
instanceId = creds['webAppInfo']['applicationId']
qclient = qbiz.get_qapps_client()
# 1. Go through all Q Apps
paginator = qclient.get_paginator('list_q_apps')
for page in paginator.paginate(instanceId=instanceId):
    for app in page['apps']:
        logger.info(f"Found Q App: {app['title']}")
        app_id = app['appId']
        try:
            # 2. Delete each Q App
            qclient.delete_q_app(instanceId=instanceId, appId=app_id)
            logger.info(f"  Deleted Q App: {app_id}")
        except Exception as e:
            logger.info(f"  Failed to delete Q App {app_id}: {e}")

# Your JSON configuration
# Read the JSON file
with open('code/q_app_details.json', 'r') as file:
    data = json.load(file)

for item in data:
    logger.info(f'creating Q App: {item['title']}')
    app_config = {
        'title': item['title'],
        'description': item['description'],
        'appDefinition': item['appDefinition']
    }

    try:
        response = qclient.create_q_app(
            instanceId=instanceId,  # Replace with your Q Business instance ID
            title=app_config['title'],
            description=app_config['description'],
            appDefinition=app_config['appDefinition']
        )
        logger.info(f"  Q App created successfully (id: {response['appId']})")
    except qclient.exceptions.ConflictException:
        logger.info("  Error: Q App with this title already exists")
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.info(f"  Error creating Q App: {str(e)}")
