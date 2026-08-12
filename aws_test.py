import boto3

REGION = "ap-south-2"

ec2 = boto3.client(
    "ec2",
    region_name=REGION
)

response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(f"Instance ID   : {instance['InstanceId']}")
        print(f"Instance Type : {instance['InstanceType']}")
        print(f"State         : {instance['State']['Name']}")
        print("-" * 50)
