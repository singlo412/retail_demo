import qbiz
import json
import sys

creds = qbiz.get_credentials()
instance_id = creds['webAppInfo']['applicationId']
qclient = qbiz.get_qapps_client()

app_id = sys.argv[1] if len(sys.argv) > 1 else None

if app_id:
    details = qclient.get_q_app(instanceId=instance_id, appId=app_id)
    print(f"App: {details['title']}")
    print(f"Description: {details['description']}")
    print("\nCards:")
    for card in details['appDefinition']['cards']:
        print(json.dumps(card, indent=2, default=str))
else:
    print("Usage: python get_qapp_details.py <app_id>")
