import boto3

from app.config import AWS_REGION
from app.services.resource_service import save_resource


def get_ec2_instances(region=AWS_REGION):
    """
    Retrieve EC2 instance information from AWS.
    """

    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            tags = {}

            for tag in instance.get("Tags", []):
                tags[tag["Key"]] = tag["Value"]

            instance_data = {
                "instance_id": instance["InstanceId"],
                "instance_type": instance["InstanceType"],
                "state": instance["State"]["Name"],
                "availability_zone": instance["Placement"]["AvailabilityZone"],
                "private_ip": instance.get("PrivateIpAddress"),
                "public_ip": instance.get("PublicIpAddress"),
                "launch_time": str(
                    instance.get("LaunchTime")
                ),
                "tags": tags,
                "region": region
            }

            instances.append(instance_data)

    return instances


def collect_and_save_ec2_instances():

    print("Starting EC2 collection...")

    instances = get_ec2_instances()

    print(
        f"Found {len(instances)} EC2 instance(s)."
    )

    for instance in instances:

        resource_data = {
            "resource_id": instance["instance_id"],
            "resource_type": "EC2",
            "name": instance["tags"].get(
                "Name"
            ),
            "region": instance["region"],
            "state": instance["state"],
            "instance_type": instance["instance_type"],
            "environment": instance["tags"].get(
                "Environment"
            ),
            "tags": instance["tags"]
        }

        save_resource(resource_data)

        print(
            f"✓ Saved: "
            f"{instance['instance_id']}"
        )

    print("EC2 collection completed.")


if __name__ == "__main__":
    collect_and_save_ec2_instances()
