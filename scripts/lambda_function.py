import boto3
import json
import os
from datetime import datetime

# Initialize AWS clients
sns = boto3.client('sns')
ec2 = boto3.client('ec2')

# Environment variable for SNS Topic ARN
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']


def get_instance_details(instance_id, region):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        tags = instance.get('Tags', [])
        name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'No Name Tag')
        instance_type = instance.get('InstanceType', 'Unknown')
        platform = instance.get('Platform', 'Linux/UNIX')  # Default is Linux if key doesn't exist
        return {
            "instance_id": instance_id,
            "name": name_tag,
            "type": instance_type,
            "platform": platform
        }
    except Exception as e:
        print(f"Error fetching instance details for {instance_id}: {str(e)}")
        return {
            "instance_id": instance_id,
            "name": "Error",
            "type": "Unknown",
            "platform": "Unknown"
        }


def handle_run_instances(event, region, account_id):
    items = event["detail"]["responseElements"]["instancesSet"]["items"]
    instance_ids = [item["instanceId"] for item in items]
    return extract_message(event, region, account_id, instance_ids, "EC2 Instance(s) Launched")


def handle_reboot_instances(event, region, account_id):
    items = event["detail"]["requestParameters"]["instancesSet"]["items"]
    instance_ids = [item["instanceId"] for item in items]
    return extract_message(event, region, account_id, instance_ids, "EC2 Instance(s) Rebooted")


def handle_stop_instances(event, region, account_id):
    items = event["detail"]["requestParameters"]["instancesSet"]["items"]
    instance_ids = [item["instanceId"] for item in items]
    return extract_message(event, region, account_id, instance_ids, "EC2 Instance(s) Stopped")


def handle_start_instances(event, region, account_id):
    items = event["detail"]["requestParameters"]["instancesSet"]["items"]
    instance_ids = [item["instanceId"] for item in items]
    return extract_message(event, region, account_id, instance_ids, "EC2 Instance(s) Started")


def handle_terminate_instances(event, region, account_id):
    items = event["detail"]["requestParameters"]["instancesSet"]["items"]
    instance_ids = [item["instanceId"] for item in items]
    return extract_message(event, region, account_id, instance_ids, "EC2 Instance(s) Terminated")


def extract_message(event, region, account_id, instance_ids, subject):
    instance_details = []
    for instance_id in instance_ids:
        details = get_instance_details(instance_id, region)
        instance_details.append(
            f"Instance: {details['instance_id']}\n"
            f"Name: {details['name']}\n"
            f"Type: {details['type']}\n"
            f"Platform: {details['platform']}"
        )

    user_identity = event["detail"]["userIdentity"]
    user_type = user_identity.get("type", "")
    user = "Unknown"

    if user_type == "IAMUser":
        user = user_identity.get("userName", "Unknown") # e.g., clouduser
    elif user_type == "AssumedRole":
        principal_id = user_identity.get("principalId", "")
        if ":" in principal_id:
            user = principal_id.split(":")[1]  # e.g., clouduser@example.com

    time = event["time"]
    message = (
        f"{subject}\n\n"
        f"{chr(10).join(instance_details)}\n\n"
        f"Initiated By: {user}\n"
        f"AWS Account: {account_id}\n"
        f"Region: {region}\n"
        f"Time: {time} UTC\n\n\n\n\n\n\n\n\n\n"
    )

    return subject, message


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event, indent=2))
        region = event["region"]
        account_id = event["account"]
        event_name = event["detail"]["eventName"]

        if event_name == "RunInstances":
            subject, message = handle_run_instances(event, region, account_id)
        elif event_name == "RebootInstances":
            subject, message = handle_reboot_instances(event, region, account_id)
        elif event_name == "StopInstances":
            subject, message = handle_stop_instances(event, region, account_id)
        elif event_name == "StartInstances":
            subject, message = handle_start_instances(event, region, account_id)
        elif event_name == "TerminateInstances":
            subject, message = handle_terminate_instances(event, region, account_id)
        else:
            print(f"Unhandled event type: {event_name}")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Unhandled event", "eventName": event_name})
            }

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Alert: {subject}",
            Message=message
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification sent", "eventName": event_name})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
