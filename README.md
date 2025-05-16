# AWS EC2 State Change Alerts

This project monitors EC2 instance state changes (such as launch, reboot, stop, start, and terminate) and triggers alerts via **SNS** using **AWS Lambda** and **CloudTrail**.

---

## Architecture Diagram

Below are the architecture diagrams for the EC2 state change alert system:

### Single Account Architecture

![Single Account Architecture](images/Architecture1.png)

*Note: This sample implementation focuses on the single-account architecture.*

### Multi-Account Architecture

![Multi-Account Architecture](images/Architecture2.png)

---

## Features

- Monitors EC2 state changes (launch, reboot, stop, start, terminate).
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
Name: Test\_Server

Launched By: cloud\_user
Region: us-east-1
Time: 2025-05-13T19:40:38Z

```

---

## Why These AWS Services?

- **CloudTrail** captures API activity and changes in your AWS account, making it ideal for detecting EC2 state changes.
- **EventBridge** filters and routes specific events (like EC2 state changes) in near real-time to trigger actions.
- **AWS Lambda** provides serverless compute to process events and execute custom logic without managing servers.
- **SNS** enables flexible and scalable notification delivery to multiple subscribers through various protocols like email and SMS.

---

## Cost Considerations

This solution leverages multiple AWS services that have their own pricing models. Below are the general cost considerations for each service used:

### 1. **CloudTrail**

- **Pricing**:  
  - Management events (such as EC2 API calls) are free for the first copy per region.  
  - Additional copies and data events incur charges.  
- **Recommendation**:  
  For typical EC2 state change monitoring, the default management events logging is sufficient and usually free.

### 2. **EventBridge**

- **Pricing**:  
  - Charged per million events published or matched.  
- **Recommendation**:  
  EventBridge is cost-efficient for most workloads. Since this setup filters only specific EC2 state change events, the volume remains low and affordable.

### 3. **AWS Lambda**

- **Pricing**:  
  - Charged based on the number of requests and compute time (duration in milliseconds).  
- **Recommendation**:  
  Lambda functions triggered by EC2 state changes typically have low execution time and frequency, resulting in minimal cost.

### 4. **Amazon SNS**

- **Pricing**:  
  - Charged per million publish requests and per delivery (depending on protocol: email is generally free, SMS may incur charges).  
- **Recommendation**:  
  Costs depend on the number of notifications sent and subscriber type. Email notifications are usually free, but SMS or mobile push may add cost.

---

### Summary

Overall, this architecture is designed to be cost-effective for small to medium environments with occasional EC2 state changes. For very large-scale environments or heavy usage, monitoring your AWS billing and adjusting accordingly is recommended.

---

## Enhancements (Future Improvements)

- **Detailed Notifications**: Include additional metadata, such as instance tags or cost estimation.
- **Infrastructure as Code**: Provide CloudFormation or Terraform templates for automated setup.

---