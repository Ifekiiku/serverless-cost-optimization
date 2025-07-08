import boto3
import json
import os
from datetime import datetime, timedelta

ce = boto3.client('ce')
sns = boto3.client('sns')
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
s3 = boto3.client('s3')
bucket_name = 'cost-optimization-logs-ifekiiku'
key = f"report-{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')}.json"

def lambda_handler(event, context):
    report = []

    # 1. Cost Explorer Report (last 7 days)
    today = datetime.utcnow().date()
    start = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    cost_response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    for day in cost_response['ResultsByTime']:
        for group in day['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            if cost > 0.1:
                report.append(f"[Cost] {service} - ${cost:.2f} on {day['TimePeriod']['Start']}")

    # 2. Idle EC2 Instances (low CPU usage for 3 days)
    ec2_instances = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])

    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.utcnow() - timedelta(days=3),
                EndTime=datetime.utcnow(),
                Period=86400,  # 1 day
                Statistics=['Average']
            )

            if metrics['Datapoints']:
                avg_cpu = sum([point['Average'] for point in metrics['Datapoints']]) / len(metrics['Datapoints'])
                if avg_cpu < 5:
                    report.append(f"[Idle EC2] {instance_id} - Avg CPU {avg_cpu:.2f}% (last 3 days)")

    # 3. Unused EBS Volumes (not attached)
    volumes = ec2.describe_volumes(Filters=[
        {'Name': 'status', 'Values': ['available']}
    ])
    for vol in volumes['Volumes']:
        vol_id = vol['VolumeId']
        size_gb = vol['Size']
        report.append(f"[Unused EBS] {vol_id} - {size_gb} GB (unattached)")

    # Send report via SNS
    if report:
        message = "\n".join(report)
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:701785833185:CostAlerts',
            Subject="AWS Cost Optimization Report",
            Message=message
        )
    
    # Save report to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(report))

    return {
        "message": "Scan complete",
        "findings": report or ["No issues found."]
    }
