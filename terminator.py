import boto3
import datetime


def get_instance_date_tag(instance):
    # Retrieve tags from the instance; if no tags, return an empty list
    tags = instance.tags or []

    # Iterate through the tags to find the 'date' tag
    for tag in tags:
        if tag['Key'] == 'date':
            return tag['Value']

    # Return None if 'date' tag is not found
    return None


def parse_date(date_str):
    # Define possible date formats
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'):
        try:
            # Attempt to parse the date string using the current format
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            # If parsing fails, continue with the next format
            continue

    # Return None if no formats match
    return None


def terminate_old_instances():
    """
    Terminates EC2 instances that have a 'date' tag older than one week.
    """
    # Initialize the EC2 resource
    ec2 = boto3.resource('ec2')

    # Get today's date and the date one week ago
    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(weeks=1)

    # Print today's date and the date one week ago for reference
    print(f"Today's date: {today}")
    print(f"One week ago: {one_week_ago}")

    # Retrieve all EC2 instances
    instances = ec2.instances.all()
    terminated_instance_ids = []

    # Iterate through each instance
    for instance in instances:
        # Get the 'date' tag value for the instance
        date_str = get_instance_date_tag(instance)

        if date_str:
            # Parse the date string into a datetime.date object
            date = parse_date(date_str)

            if date:
                # Compare the parsed date with the date one week ago
                if date < one_week_ago:
                    # Terminate the instance if the date is older than one week
                    print(f"Terminating instance {instance.id} with date tag {date_str}")
                    instance.terminate()
                    terminated_instance_ids.append(instance.id)
                else:
                    # Print a message if the instance is not old enough
                    print(f"Instance {instance.id} is not old enough. Date Tag: {date_str}")
            else:
                # Print a message if the date string could not be parsed
                print(f"Date parsing failed for: {date_str}")
                print(f"Instance {instance.id} has an invalid date format.")
        else:
            # Print a message if the instance does not have a 'date' tag
            print(f"Instance {instance.id} does not have a 'date' tag.")

    # Print the IDs of all terminated instances
    print("Terminated instance IDs:")
    for instance_id in terminated_instance_ids:
        print(instance_id)


if __name__ == "__main__":
    # Run the function to terminate old instances
    terminate_old_instances()
