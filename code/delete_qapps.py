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
logger.info(f"Deleting all QApps for instanceId: {instanceId}")

qbiz.delete_qapps(instanceId)

exit(0)
