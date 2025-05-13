import boto3
import json
import os
from datetime import datetime

# Initialize AWS clients
sns = boto3.client('sns')
ec2 = boto3.client('ec2')

# Environment variable for SNS Topic ARN
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def get_instance_name(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances(InstanceIds=[instance_id])
        tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
        return "No Name Tag"
    except Exception as e:
        print(f"Error fetching Name tag for {instance_id}: {str(e)}")
        return "Error Fetching Name Tag"


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event, indent=2))

        instance_details = []
        region = event["region"]
        items = event["detail"]["responseElements"]["instancesSet"]["items"]

        for item in items:
            instance_id = item["instanceId"]
            name_tag = get_instance_name(instance_id, region)
            instance_details.append(f"Instance: {instance_id}\nName: {name_tag}")

        user = event["detail"]["userIdentity"].get("userName", "Unknown")
        time = event["time"]

        message = (
            f"New EC2 Instance(s) Launched\n\n"
            f"{chr(10).join(instance_details)}\n\n"
            f"Launched By: {user}\n"
            f"Region: {region}\n"
            f"Time: {time} UTC"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Alert: EC2 Instance Launched",
            Message=message
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification sent", "instances": instance_details})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
