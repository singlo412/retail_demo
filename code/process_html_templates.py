import os
import logging
import boto3
from botocore.exceptions import ClientError
import json
import random
from jinja2 import Environment, FileSystemLoader

import qbiz

# Configure logging with basic settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_cfront_client(creds="env"):
    """
    Creates and returns a boto3 client for Amazon CloudFront service.
    
    Args:
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.
    
    Returns:
        boto3.client: A boto3 client configured for Amazon CloudFront service
    """
    cfclient = qbiz.get_client('cloudfront', creds)
    return cfclient

def get_qapp_ids(q_instance_id):
    """
    Get the list of QApps for a given Q Business instance    

    Args:
        q_instance_id (string, required): Q Business instance ID
    
    Returns:
        Dictionary of QApps information keyed by the QApp title
    """
    qclient = qbiz.get_qapps_client()
    appdata = {}

    paginator = qclient.get_paginator('list_q_apps')
    for page in paginator.paginate(instanceId=q_instance_id):
        for app in page['apps']:
            logger.info(f"  {app['appId']}: {app['title']}")
            appdata[app['title']] = app['appId']
    return appdata

def get_web_experience(q_instance_id):
    """
    Get the webexperience information for a given Q Business instance
    
    Args:
        q_instance_id (string, required): Q Business instance ID
    
    Returns:
        Dictionary of the webexperience information
    """
    # For the web experience, we want the credentials from the environment
    # rather than the credentials file. This will use the user that is
    # currently logged in within the terminal
    qclient = qbiz.get_qbiz_client(creds="env")

    response = qclient.list_web_experiences(applicationId=q_instance_id)
    logger.info(f"Updating webexperience: {response['webExperiences'][0]['webExperienceId']}")
    logger.info(f"Webexperience URL: {response['webExperiences'][0]['defaultEndpoint']}")

    return response["webExperiences"][0]

def get_quicksight_dashboard():
    """
    Get the QuickSight dashboard information deployed by the project's cloud formation stacks
    
    Args:
        None
    
    Returns:
        Dictionary of the QuickSight dashboard information
    """
    response =  qbiz.get_client('sts', "env").get_caller_identity()
    account_id = response["Account"]

    qsclient = qbiz.get_client('quicksight', "env")
    response = qsclient.list_dashboards(AwsAccountId=account_id)
    for dashboard in response["DashboardSummaryList"]:
        logger.debug(f"Using QuickSight dashboard: {dashboard['DashboardId']}: {dashboard["Name"]}")
        if dashboard["Name"] == "qbiz-application-dashboard":
            tmp = qsclient.describe_dashboard(AwsAccountId=account_id,
                                              DashboardId=dashboard["DashboardId"])
            return tmp["Dashboard"]
    return None

def get_quicksight_dashboard_url(dashboard):
    """
    Get the QuickSight dashboard embedded URL
    
    Args:
        dashboard (dict, required): The QuickSight dashboard information 
    
    Returns:
        URL for embedding the QuickSight dashboard
    """
    (_, _, _, region, account_id, _) = dashboard['Arn'].split(":")
    url = f"https://{region}.quicksight.aws.amazon.com/sn/embed/share/accounts/{account_id}/dashboards/{dashboard['DashboardId']}"
    return url

def process_templates(creds=None):
    """
    Process the HTML templates and uploads all the web files to S3,
    trigering an invalidation in CloudFront

    Args:
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.

    Returns:
        None
    """
    if creds is None:
        creds = qbiz.get_credentials()

    q_instance_id = creds["webAppInfo"]["applicationId"]
    web_experience = get_web_experience(q_instance_id)
    q_webexp_url = web_experience["defaultEndpoint"]

    qs_dashboard = get_quicksight_dashboard()
    qs_dashboard_url = get_quicksight_dashboard_url(qs_dashboard)

    urls = {
        "embedded": {
            "quicksight_dashboard": qs_dashboard_url,
            "qbusiness_chatbot": q_webexp_url
        },
        "qapp": {}
    }

    appdata = get_qapp_ids(q_instance_id)
    for a in appdata:
        urls["qapp"][a] = f"{q_webexp_url}#/app/{appdata[a]}"

    tpl_environment = Environment(loader=FileSystemLoader("html_templates/"), autoescape=True)
    tpl_fname = "retail-qbizapp.html.j2"
    out_fname = "static/"+tpl_fname[:-3]
    css_fname = "static/retail-qbizapp.css"
    template = tpl_environment.get_template(tpl_fname)

    content = template.render(urls=urls)
    with open(out_fname, mode="w", encoding="utf-8") as outf:
        outf.write(content)
        logger.info(f"Saved: {out_fname}")

    dst_bucket = os.environ["QBIZ_CLOUDFRONT_BUCKET_NAME"]
    dst_key = "retail-qbizapp.html"
    s3_client = boto3.client('s3')
    with open(out_fname, "rb") as f:
        s3_client.upload_fileobj(f, dst_bucket, dst_key, ExtraArgs={'ContentType':'text/html'})
        logger.info(f"Uploaded: {dst_key}")
    dst_key = "retail-qbizapp.css"
    with open(css_fname, "rb") as f:
        s3_client.upload_fileobj(f, dst_bucket, dst_key, ExtraArgs={'ContentType':'text/css'})
        logger.info(f"Uploaded: {dst_key}")

    cfclient = get_cfront_client("env")
    response = cfclient.list_distributions()
    if response['DistributionList']['Quantity'] != 1:
        logger.error("Unexpected number of CloudFront distributions. Must be 1.")
        exit(1)
    cf_dist_id = response['DistributionList']['Items'][0]['Id']
    cf_fqdn = response['DistributionList']['Items'][0]['DomainName']
    logger.info(f"Updating CloudFront distribution ID: {cf_dist_id}")
    logger.info(f"CloudFront URL: https://{cf_fqdn}")
    response = cfclient.create_invalidation(
        DistributionId=cf_dist_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ["/*"]
            },
            'CallerReference': f"inv-req-{str(random.randrange(1,1000000))}"
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 201:
        logger.info("CloudFront cache invalidation successfully triggered.")
    else:
        logger.error("CloudFront cache invalidation failed.")
        logger.error(response)

process_templates()
exit(0)
