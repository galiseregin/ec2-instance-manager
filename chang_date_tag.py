import boto3
import botocore
from datetime import datetime, timedelta

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2')


def update_date_tags(instance_ids, new_date_value):

    updated_instances = []

    try:
        for instance_id in instance_ids:
            tags = [{'Key': 'date', 'Value': new_date_value}]

            ec2.create_tags(Resources=[instance_id], Tags=tags)
            updated_instances.append(instance_id)
            print(f"Updated 'date' tag for instance ID: {instance_id}")

    except botocore.exceptions.ClientError as e:
        print(f"An error occurred: {e}")

    return updated_instances


if __name__ == '__main__':
    # List of instance IDs to update
    instance_ids = [
        'i-004c284389ffff1b0',
        'i-063a84c67471fbb8e',
        # Add more instance IDs as needed
    ]

    # Calculate the date 3 years ago from today
    three_years_ago = datetime.now() - timedelta(days=3 * 365)
    new_date_value = three_years_ago.strftime('%Y-%m-%d')

    # Update the 'date' tag for the specified instances
    updated_instances = update_date_tags(instance_ids, new_date_value)
    print("Updated instances:", updated_instances)
