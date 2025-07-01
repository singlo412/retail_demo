import boto3
import json
import os

credentials_fname = os.environ.get('QBIZ_CREDENTIALS_FILE', 'credentials.json')
credentials = json.load(open(credentials_fname, 'r'))

def get_credentials():
    """
    Get the active credentials
    
    Args:
        None
    
    Returns:
        credentials dictionary
    """
    return credentials

def show_identity(creds=None):
    """
    Show the identity information making the call.
    
    Args:
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.
    
    Returns:
        None
    """
    if creds is None:
        creds = credentials["credentials"]
    # Allow using the current environment configuration.
    elif creds == "env":
        creds = {
            "accessKey": None,
            "secretKey": None,
            "sessionToken": None
        }

    stsclient = boto3.client('sts',
                        aws_access_key_id=creds['accessKey'],
                        aws_secret_access_key=creds['secretKey'],
                        aws_session_token = creds['sessionToken'],
                       )
    print(stsclient.get_caller_identity())

def get_client(svc, creds=None):
    """
    Creates and returns a boto3 client for any service.
    
    Args:
        svc (string, required): AWS service
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.
    
    Returns:
        boto3.client: A boto3 client configured for the service
    """
    if creds is None:
        creds = credentials["credentials"]
    # Allow using the current environment configuration.
    elif creds == "env":
        creds = {
            "accessKey": None,
            "secretKey": None,
            "sessionToken": None
        }

    qclient = boto3.client(svc,
                           aws_access_key_id=creds['accessKey'],
                           aws_secret_access_key=creds['secretKey'],
                           aws_session_token = creds['sessionToken']
                           )
    return qclient

def get_qbiz_client(creds=None):
    """
    Creates and returns a boto3 client for Amazon Q Business service.
    
    Args:
        creds (dict, optional): AWS credentials dictionary. If None, 
        it uses the default credentials.
    
    Returns:
        boto3.client: A boto3 client configured for Amazon Q Business service
    """
    return get_client("qbusiness", creds)

def get_qapps_client(creds=None):
    """
    Creates and returns a boto3 client for Amazon Q Business QApps service.
    
    Args:
        creds (dict, optional): AWS identity aware credentials dictionary. If None, 
        it uses the default credentials.
    
    Returns:
        boto3.client: A boto3 client configured for Amazon Q Business QApps service
    """
    if creds is None:
        creds = credentials['identityAwareCredentials']
    return get_client('qapps', creds)

def list_qbiz_instances():
    """
    List the Q Business instances.
    
    Args:
        None
    
    Returns:
        None
    """
    qclient = get_qbiz_client()

    resp = qclient.list_applications()
    for app in resp['applications']:
        print(f"  QBiz Application: {app['displayName']}")

def qbiz_search_relevant_content(query, retriever_id):
    """
    Do a search for relevant content using a specific Q Business retriever.
    
    Args:
        query (string, required): Query string
        retriever_id (string, required): Q Business retriever ID
    
    Returns:
        response: Direct response from the API call
    """
    qclient = get_qbiz_client()

    response = qclient.search_relevant_content(
        applicationId=credentials['webAppInfo']['applicationId'],
        queryText=query,
        contentSource={'retriever': {'retrieverId': retriever_id}}
        )
    print(f"response: {json.dumps(indent=2)}")
    return response


def list_categories(q_instance_id):
    """
    List the categories available in a Q Business instance
    
    Args:
        q_instance_id (string, required): Q Business instance ID
    
    Returns:
        response: Array of categories. None if there was an error.
    """
    print("Categories for Q instance id:", q_instance_id)

    qclient = get_qapps_client()

    try:
        resp = qclient.list_categories(instanceId=q_application_id)
        for category in resp['categories']:
            print(f"  category: {category}")
        return resp['categories']
    except Exception as e:
        print("Failed to get categories")
        import traceback
        traceback.print_exc()
    return None

def delete_qapps(q_instance_id):
    """
    Delete all QApps in a Q Business instance
    
    Args:
        q_instance_id (string, required): Q Business instance ID
    
    Returns:
        None
    """
    qclient = get_qapps_client()

    paginator = qclient.get_paginator('list_q_apps')
    for page in paginator.paginate(instanceId=q_instance_id):
        for app in page['apps']:
            print(f"Deleting Q App: {app['title']}", end=None)
            app_id = app['appId']
            try:
                qclient.delete_q_app(instanceId=q_instance_id, appId=app_id)
                print(f"  Deleted Q App: {app_id}")
            except Exception as e:
                print(f"  FAILED to delete Q App {app_id}: {e}")


def list_qapps(q_instance_id):
    """
    Delete all QApps in a Q Business instance
    
    Args:
        q_instance_id (string, required): Q Business instance ID
    
    Returns:
        List of QApps
    """
    qclient = get_qapps_client()

    print("List of QApps for instance: ", q_instance_id)
    result = []
    paginator = qclient.get_paginator('list_q_apps')
    for page in paginator.paginate(instanceId=q_instance_id):
        for app in page['apps']:
            result.append(app)
            print(f"  {app['appId']}: {app['title']}")
    return result

def create_qapp(appinfo):
    """
    Create a QApp.
    
    Args:
        appinfo (dict, required): dictionary containing at least
            title, description and appDefinition.
    
    Returns:
        response: Direct response from the API call if successful, None
            otherwise.
    """
    print(f'creating Q App: {appinfo['title']}')
    qclient = get_qapps_client()
    app_config = {
        'title': appinfo['title'],
        'description': appinfo['description'],
        'appDefinition': appinfo['appDefinition']
    }

    try:
        response = qclient.create_q_app(
            title=app_config['title'],
            description=app_config['description'],
            appDefinition=app_config['appDefinition']
        )
        print("Q App created successfully")
        return response
    except qclient.exceptions.ConflictException:
        print("Error: Q App with this title already exists")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error creating Q App: {str(e)}")
    return None

def create_qapps(fname):
    """
    Create one or more QApp(s) based on a JSON file configuration.
    
    Args:
        fname (string, required): JSON file name containing the QApp
            configuration(s).
    
    Returns:
        response: Direct response from the API call if successful, None
            otherwise.
    """
    qclient = get_qapps_client()
    instance_id = credentials['webAppInfo']['applicationId']

    # Read the JSON configuration file
    with open(fname, 'r') as file:
        data = json.load(file)

    for item in data:
        print(f'creating Q App: {item['title']}')
        app_config = {
            'title': item['title'],
            'description': item['description'],
            'appDefinition': item['appDefinition']
        }

        try:
            response = qclient.create_q_app(
                instanceId=instance_id,  # Replace with your Q Business instance ID
                title=app_config['title'],
                description=app_config['description'],
                appDefinition=app_config['appDefinition']
            )
            print(f"  Q App created successfully (id: {response['appId']})")
        except qclient.exceptions.ConflictException:
            print("  Error: Q App with this title already exists")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"  Error creating Q App: {str(e)}")
