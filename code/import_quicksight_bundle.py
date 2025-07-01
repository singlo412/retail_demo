import boto3
import time
import uuid
import json

with open('env.json', 'r') as file:
    env = json.load(file)

# Replace with your AWS Account ID and the ARNs of the assets you want to export
AWS_ACCOUNT_ID = env['awsAccountId']

IMPORT_JOB_ID = f'import-{str(uuid.uuid4())}'  # Must be unique for each run

# Initialize QuickSight client
client = boto3.client('quicksight', aws_account_id=AWS_ACCOUNT_ID, 
                    aws_access_key_id=env['awsAccessKey'],
                    aws_secret_access_key=env['awsSecretKey'],
                    region_name=env['awsRegion'])

# Start import job
response = client.start_asset_bundle_import_job(
    AwsAccountId=AWS_ACCOUNT_ID,
    AssetBundleImportJobId=IMPORT_JOB_ID,
    AssetBundleImportSource={
        'S3Uri': 's3://QBIZ_ASSET_BUCKET_NAME/qs-asset/quicksight_asset_bundle.qs'
    },
    OverrideParameters={
        'ResourceIdOverrideConfiguration': {
            'PrefixForAllResources': 'Imported-'
        }
    },
    FailureAction='ROLLBACK'
)
# print(response)
print("Import job started:", response['AssetBundleImportJobId'])
# Poll job status
while True:
    response = client.describe_asset_bundle_import_job(
        AwsAccountId=AWS_ACCOUNT_ID,
        AssetBundleImportJobId=IMPORT_JOB_ID,
    )
    status = response['JobStatus']
    print("Checking job status...")
    print("Job status:", status)
    if status == 'SUCCESSFUL':
        print("Import completed")
        break
    elif status in ['FAILED', 'CANCELLED', 'FAILED_ROLLBACK_COMPLETED']:
        raise Exception(f"Import failed: {status} => {response}")
    time.sleep(10)

