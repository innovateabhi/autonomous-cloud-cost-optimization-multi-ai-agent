import boto3


def get_rds_instances(region="ap-south-2"):
    """
    Retrieve RDS database information.
    """

    rds = boto3.client(
        "rds",
        region_name=region
    )

    response = rds.describe_db_instances()

    databases = []

    for db in response["DBInstances"]:

        database_data = {
            "identifier": db["DBInstanceIdentifier"],
            "engine": db["Engine"],
            "engine_version": db["EngineVersion"],
            "instance_class": db["DBInstanceClass"],
            "status": db["DBInstanceStatus"],
            "storage_gb": db["AllocatedStorage"],
            "multi_az": db["MultiAZ"],
            "region": region
        }

        databases.append(database_data)

    return databases
