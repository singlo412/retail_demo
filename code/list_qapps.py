import boto3
# import botocore.session
import json

import qbiz

creds = qbiz.get_credentials()
instanceId = creds['webAppInfo']['applicationId']
qbiz.list_qapps(instanceId)

exit(0)
