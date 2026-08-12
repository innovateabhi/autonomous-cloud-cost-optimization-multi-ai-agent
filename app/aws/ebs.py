import boto3


def get_ebs_volumes(region="ap-south-2"):
    """
    Retrieve EBS volume information from AWS.
    """

    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    response = ec2.describe_volumes()

    volumes = []

    for volume in response["Volumes"]:

        attachments = volume.get("Attachments", [])

        attached_instance = None

        if attachments:
            attached_instance = attachments[0].get("InstanceId")

        volume_data = {
            "volume_id": volume["VolumeId"],
            "volume_type": volume["VolumeType"],
            "size_gb": volume["Size"],
            "state": volume["State"],
            "availability_zone": volume["AvailabilityZone"],
            "attached_instance": attached_instance,
            "encrypted": volume["Encrypted"],
            "region": region
        }

        volumes.append(volume_data)

    return volumes
