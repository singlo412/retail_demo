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

def get_quicksuite_chat_embed_url(account_id, user_arn, allowed_domain, agent_arn=None):
    """
    Generate Quick Suite embedded chat URL using GenerateEmbedUrlForRegisteredUser API.
    
    Args:
        account_id (str): AWS Account ID
        user_arn (str): ARN of the registered QuickSight user
        allowed_domain (str): Domain where embedding is allowed (CloudFront URL)
        agent_arn (str, optional): ARN of custom chat agent. If None, uses default system agent.
    
    Returns:
        str: Embed URL for Quick Suite chat, or None if generation fails
    """
    try:
        qs_client = qbiz.get_client('quicksight', "env")
        
        experience_config = {'QuickChat': {}}
        
        response = qs_client.generate_embed_url_for_registered_user(
            AwsAccountId=account_id,
            UserArn=user_arn,
            ExperienceConfiguration=experience_config,
            AllowedDomains=[allowed_domain]
        )
        
        embed_url = response.get('EmbedUrl')
        logger.info(f"Generated Quick Suite chat embed URL successfully")
        return embed_url
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Failed to generate Quick Suite embed URL: {error_code} - {error_message}")
        
        if error_code == 'ResourceNotFoundException':
            logger.error("User not found. Ensure the user is registered in QuickSight.")
        elif error_code == 'AccessDeniedException':
            logger.error("Access denied. Check IAM permissions for quicksight:GenerateEmbedUrlForRegisteredUser")
        
        return None
    except Exception as e:
        logger.error(f"Unexpected error generating Quick Suite embed URL: {str(e)}")
        return None

def get_quicksight_user_arn(account_id, namespace='default'):
    """
    Get the QuickSight user ARN for the current user.
    
    Args:
        account_id (str): AWS Account ID
        namespace (str): QuickSight namespace (default: 'default')
    
    Returns:
        str: User ARN or None if not found
    """
    try:
        qs_client = qbiz.get_client('quicksight', "env")
        
        # List users and find the current one
        response = qs_client.list_users(
            AwsAccountId=account_id,
            Namespace=namespace
        )
        
        if response.get('UserList'):
            # Return the first user's ARN (typically the admin/author)
            user_arn = response['UserList'][0]['Arn']
            logger.info(f"Found QuickSight user: {user_arn}")
            return user_arn
        
        logger.warning("No QuickSight users found")
        return None
        
    except ClientError as e:
        logger.error(f"Failed to list QuickSight users: {e}")
        return None

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

    # Get AWS account ID for Quick Suite embed URL generation
    sts_response = qbiz.get_client('sts', "env").get_caller_identity()
    account_id = sts_response["Account"]
    
    # Get CloudFront domain for allowed domains
    cfclient = get_cfront_client("env")
    cf_response = cfclient.list_distributions()
    cf_fqdn = cf_response['DistributionList']['Items'][0]['DomainName']
    allowed_domain = f"https://{cf_fqdn}"
    
    # Get QuickSight user ARN for embed URL generation
    user_arn = get_quicksight_user_arn(account_id)
    
    # Generate Quick Suite chat embed URL
    quicksuite_chat_url = None
    quicksuite_agent_arn = creds.get("quickSuiteAgentArn")  # Optional: from credentials.json
    
    if user_arn:
        quicksuite_chat_url = get_quicksuite_chat_embed_url(
            account_id=account_id,
            user_arn=user_arn,
            allowed_domain=allowed_domain,
            agent_arn=quicksuite_agent_arn
        )
    
    if not quicksuite_chat_url:
        logger.warning("Quick Suite chat URL not generated. Falling back to Q Business chatbot.")
        quicksuite_chat_url = q_webexp_url

    urls = {
        "embedded": {
            "quicksight_dashboard": qs_dashboard_url,
            "qbusiness_chatbot": q_webexp_url,
            "quicksuite_chat": quicksuite_chat_url,
            "quicksuite_agent_arn": quicksuite_agent_arn
        },
        "qapp": {}
    }

    # Try to get Q Apps, but continue if it fails (e.g., expired credentials)
    try:
        appdata = get_qapp_ids(q_instance_id)
        for a in appdata:
            urls["qapp"][a] = f"{q_webexp_url}#/app/{appdata[a]}"
    except Exception as e:
        logger.warning(f"Failed to get Q Apps (credentials may be expired): {e}")
        logger.warning("Continuing without Q Apps URLs. Other tabs may not work correctly.")

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
