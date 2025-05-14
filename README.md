# AWS EC2 State Change Alerts

This project monitors EC2 instance state changes (such as launch, stop, terminate, and reboot) and triggers alerts via **SNS** using **AWS Lambda** and **CloudTrail**.

---

## Features

- Monitors EC2 state changes (launch, stop, terminate, reboot).
- Sends notifications through **SNS** with details about the state change.
- Configured using **EventBridge** to trigger on EC2 state changes captured by **CloudTrail**.

---

## Prerequisites

- AWS account
- IAM roles with appropriate permissions for Lambda, CloudTrail, EventBridge, and SNS
- AWS CLI or Console for setup

---

## Setup Instructions

### 1. **Configure CloudTrail**

Ensure CloudTrail is logging EC2 instance actions (launch, stop, terminate, reboot):

1. Go to the **CloudTrail** service in the AWS console.
2. Create or update a trail to include **EC2** service events.
3. Enable logging for **Management Events** and ensure **Read/Write events** are logged.
4. Verify the CloudTrail event history includes EC2 instance state change events.

---

### 2. **Create an EventBridge Rule**

Set up an EventBridge rule to capture EC2 state change events from CloudTrail:

1. Go to **EventBridge** in the AWS console.
2. Create a new rule to capture EC2 state changes:
   - Select the **CloudTrail** event source.
   - Filter the event patterns for EC2 state changes (launch, stop, terminate, reboot).
   - Set the rule to trigger the Lambda function that processes the state change event.

---

### 3. **Lambda Function**

Create the Lambda function to process EC2 state changes and send notifications via SNS:

1. Go to **AWS Lambda** and create a new Lambda function.
2. Upload the Lambda code from this repository to handle EC2 state changes.
3. Add appropriate permissions for Lambda to read CloudTrail events, describe EC2 instances, and publish to SNS.
4. Set up the Lambda trigger to be the **EventBridge rule** you created.

---

### 4. **Create an SNS Topic**

Create an SNS topic to send alerts to a distribution list or endpoint:

1. Go to **SNS** in the AWS console.
2. Create a new SNS topic and configure subscriptions (email, SMS, etc.).
3. Ensure the Lambda function has permissions to publish messages to the SNS topic.

---

## Usage

Once the setup is complete, the EventBridge rule will automatically trigger the Lambda function when an EC2 instance's state changes (e.g., launched, stopped, terminated, rebooted). The Lambda function will send a notification via SNS, including the following details:

- Instance ID
- Name tag (if available)
- User who triggered the action
- Region
- Timestamp of the event

### Sample SNS Notification

```
New EC2 Instance(s) Launched

Instance: i-0be3f21f92465c4e7
Name: Test_Server

Launched By: cloud_user
Region: us-east-1
Time: 2025-05-13T19:40:38Z
```

---

## Enhancements (Future Improvements)

- **Multi-Account Support**: Extend the architecture to handle EC2 state changes from multiple AWS accounts.
- **Detailed Notifications**: Include additional metadata, such as instance tags or cost estimation.
- **Infrastructure as Code**: Provide CloudFormation or Terraform templates for automated setup.
- **Error Handling**: Improve the Lambda function with retries and detailed logging for failed notifications.

---

## Architecture Diagram

*(Include an architecture diagram here to visualize the workflow.)*

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
