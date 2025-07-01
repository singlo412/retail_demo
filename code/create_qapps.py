import boto3
import qbiz

creds = qbiz.get_credentials()
instanceId = creds['webAppInfo']['applicationId']
qbiz.create_qapps('code/q_app_details.json')

exit(0)
