import boto3
import datetime


def read_configuration(file_path='configuration.txt'):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Split each line into key and value based on the first occurrence of ': '
            key, value = line.strip().split(': ')
            config[key] = value
    return config


def read_user_data(file_path='user-data.sh'):
    with open(file_path, 'r') as f:
        return f.read()


def create_instances(number_of_instances):
    # Initialize the EC2 resource
    ec2 = boto3.resource('ec2')

    # Read configuration from the file
    config = read_configuration()

    # Extract configuration values
    instance_type = config['instance-type']
    key_name = config['key-name']
    image_id = config['image-id']
    security_group = config['security-group']
    subnet_id = config.get('subnet-id')  # Optional: Retrieve the subnet ID if provided
    user_data = read_user_data()

    instances = []

    for i in range(number_of_instances):
        # Create a unique name for each instance
        instance_name = f"web{i + 1}-gali"

        # Create the EC2 instance
        instance = ec2.create_instances(
            ImageId=image_id,  # AMI ID for the instance
            InstanceType=instance_type,  # Type of instance
            MinCount=1,  # Minimum number of instances to launch
            MaxCount=1,  # Maximum number of instances to launch
            KeyName=key_name,  # Key pair for SSH access
            SecurityGroupIds=[security_group],  # Security group(s) to associate with the instance
            SubnetId=subnet_id,  # Subnet in which to launch the instance
            UserData=user_data,  # User data script to run on instance startup
            TagSpecifications=[  # Tags to apply to the instance
                {
                    'ResourceType': 'instance',  # Resource type is 'instance'
                    'Tags': [
                        {'Key': 'Name', 'Value': instance_name},  # Name tag for identifying the instance
                        {'Key': 'date', 'Value': datetime.datetime.now().strftime('%Y-%m-%d')}  # Date tag
                    ]
                }
            ]
        )[0]  # Get the first instance from the list returned

        # Wait for the instance to be in the running state
        instance.wait_until_running()

        # Reload the instance attributes to get the latest data
        instance.reload()

        # Print instance ID and private IP address
        print(f"Instance {instance.id} with Private IP: {instance.private_ip_address}")

        # Append the instance to the list of created instances
        instances.append(instance)

    return instances


if __name__ == "__main__":
    # Prompt the user to enter the number of instances to create
    number_of_instances = int(input("Enter the number of instances to create: "))

    # Call the function to create the instances
    create_instances(number_of_instances)
