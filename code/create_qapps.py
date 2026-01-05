import boto3
import sys
import qbiz

creds = qbiz.get_credentials()
instanceId = creds['webAppInfo']['applicationId']

# Allow specifying a different JSON file as argument
json_file = sys.argv[1] if len(sys.argv) > 1 else 'code/q_app_details.json'
qbiz.create_qapps(json_file)

exit(0)
