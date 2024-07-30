# EC2 Instance Manager

## Description

The **EC2 Instance Manager** repository provides Python scripts for efficiently managing AWS EC2 instances using the `boto3` library. This project includes two primary modules:

### `creator.py`

- **Purpose:** Automates the creation and configuration of EC2 instances.
- **Features:**
  - Reads instance configurations from `configuration.txt`.
  - Configures each instance with a Linux 2 AMI and sets up an Apache server using `user-data.sh`.
  - Assigns a unique name and tags each instance with the creation date.
  - Outputs the private IP addresses of the created instances.

### `terminator.py`

- **Purpose:** Identifies and terminates EC2 instances that were created more than a week ago based on their "date" tag.
- **Features:**
  - Handles date format inconsistencies or missing tags gracefully.
  - Prints the IDs of terminated instances.

## Key Features

- **Dynamic Instance Creation:** Create instances based on user input.
- **Automated Configuration:** Automatically sets up Apache server on instances.
- **Date-Based Management:** Terminate instances older than one week based on the "date" tag.
- **Configurable Parameters:** Customize instance settings through the `configuration.txt` file.

## Prerequisites

- **AWS Account:** Ensure you have an AWS account with the necessary permissions.
- **Python 3.x:** This project requires Python 3.x.
- **boto3 Library:** Install the `boto3` library using pip:
  ```bash
  pip install boto3
