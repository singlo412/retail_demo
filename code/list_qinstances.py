import boto3
# import botocore.session
import json

credentials = json.load(open('credentials.json', 'r'))

def show_identity(creds=None):
    if creds is None:
        creds = credentials

    stsclient = boto3.client('sts',
                        aws_access_key_id=creds['accessKey'],
                        aws_secret_access_key=creds['secretKey'],
                        aws_session_token = creds['sessionToken'],
                       )
    print(stsclient.get_caller_identity())

def get_qbiz_client(creds=None):
    if creds is None:
        creds = credentials
    qclient = boto3.client('qbusiness')
    return qclient

def get_qapps_client(creds=None):
    if creds is None:
        creds = credentials['identityAwareCredentials']
    qclient = boto3.client('qapps',
                        aws_access_key_id=creds['accessKey'],
                        aws_secret_access_key=creds['secretKey'],
                        aws_session_token = creds['sessionToken'],
                        )
    return qclient

def list_qbiz_applications(c=None):
    if c is None:
        c = credentials

    qclient = get_qbiz_client(c)

    resp = qclient.list_applications()
    for app in resp['applications']:
        print(f"QBiz Application: {app['displayName']}")

def qbiz_search_relevant_content(query):
    qclient = get_qbiz_client()

    response = qclient.search_relevant_content(
        applicationId=credentials['webAppInfo']['applicationId'],
        queryText=query,
        contentSource={
            'retriever': {
                'retrieverId': 'bbe726aa-65ec-4a9b-a9b9-e0f1c54629f7'
            }
        },

        )
    print(f"response: {response}")


def list_categories(q_application_id):
    print("List categories for Q application id:", q_application_id)

    qclient = get_qapps_client()

    try:
        resp = qclient.list_categories(instanceId=q_application_id)
        print(f"resp: {resp}")
        for category in resp['categories']:
            print(f"QApps category: {category}")
    except Exception as e:
        print("Failed to get categories")
        import traceback
        traceback.print_exc()

def delete_qapps(q_application_id):
    qclient = get_qapps_client()

    # 1. List all Q Apps
    paginator = qclient.get_paginator('list_q_apps')
    # print(paginator.paginate(instanceId=instanceId))
    for page in paginator.paginate(instanceId=instanceId):
        for app in page['apps']:
            print(f"Deleting Q App: {app['title']}")
            app_id = app['appId']
            try:
                # 2. Delete each Q App
                qclient.delete_q_app(instanceId=instanceId, appId=app_id)
                print(f"Deleted Q App: {app_id}")
            except Exception as e:
                print(f"Failed to delete Q App {app_id}: {e}")


def list_qapps(q_application_id):
    qclient = get_qapps_client()

    # 1. List all Q Apps
    print("List of QApps")
    paginator = qclient.get_paginator('list_q_apps')
    # print(paginator.paginate(instanceId=instanceId))
    for page in paginator.paginate(instanceId=instanceId):
        for app in page['apps']:
            print(f"  {app['appId']}: {app['title']}")


def create_qapp(appinfo):
    print(f'creating Q App: {appinfo['title']}')
    qclient = get_qapps_client()
    app_config = {
        'title': appinfo['title'],
        'description': appinfo['description'],
        'appDefinition': appinfo['appDefinition']
    }

    try:
        response = qclient.create_q_app(
            # instanceId=env['awsAccountId'],  # Replace with your Q Business instance ID
            title=app_config['title'],
            description=app_config['description'],
            appDefinition=app_config['appDefinition']
        )
        print("Q App created successfully")
        # print(response)
    except qclient.exceptions.ConflictException:
        print("Error: Q App with this title already exists")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error creating Q App: {str(e)}")

def create_qapps(fname):
    qclient = get_qapps_client()

    # Your JSON configuration
    # Read the JSON file
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
                instanceId=instanceId,  # Replace with your Q Business instance ID
                title=app_config['title'],
                description=app_config['description'],
                appDefinition=app_config['appDefinition']
            )
            print("Q App created successfully")
            # print(response)
        except qclient.exceptions.ConflictException:
            print("Error: Q App with this title already exists")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error creating Q App: {str(e)}")

instanceId = credentials['webAppInfo']['applicationId']
print(f"instanceId: {instanceId}")

show_identity()
list_qbiz_applications()

exit(0)
