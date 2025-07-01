import boto3
import time
import requests
import uuid
import json

with open('env.json', 'r') as file:
    env = json.load(file)
    
# Replace with your AWS Account ID and the ARNs of the assets you want to export
AWS_ACCOUNT_ID = env['awsAccountId']
ASSET_ARNS = [
    f'arn:aws:quicksight:us-east-1:{AWS_ACCOUNT_ID}:dashboard/86596ebd-a1aa-4598-ae5d-2cd8dfbba9d6'
]
EXPORT_JOB_ID = f'export-{str(uuid.uuid4())}'  # Must be unique for each run

# Initialize QuickSight client
client = boto3.client('quicksight', aws_account_id=AWS_ACCOUNT_ID, 
                    aws_access_key_id=env['awsAccessKey'],
                    aws_secret_access_key=env['awsSecretKey'],
                    region_name=env['awsRegion'])

def start_export_job():
    response = client.start_asset_bundle_export_job(
        AwsAccountId=AWS_ACCOUNT_ID,
        AssetBundleExportJobId=EXPORT_JOB_ID,
        ResourceArns=ASSET_ARNS,
        IncludeAllDependencies=True,
        ExportFormat='CLOUDFORMATION_JSON'
    )
    print("Export job started:", response['AssetBundleExportJobId'])

def poll_for_completion():
    while True:
        response = client.describe_asset_bundle_export_job(
            AwsAccountId=AWS_ACCOUNT_ID,
            AssetBundleExportJobId=EXPORT_JOB_ID
        )
        print("Checking job status...")
        status = response['JobStatus']
        print("Job status:", status)
        if status == 'SUCCESSFUL':
            download_url = response['DownloadUrl']
            print("Download URL:", download_url)
            return download_url
        elif status in ['FAILED', 'CANCELLED']:
            raise Exception(f"Export job failed with status: {response}")
        time.sleep(10)  # Wait before polling again

def download_bundle(url, filename='cloudformation/qs-asset/quicksight_test_asset_bundle.json'):
    response = requests.get(url, timeout=180)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded asset bundle to {filename}")

if __name__ == '__main__':
    start_export_job()
    url = poll_for_completion()
    download_bundle(url)

