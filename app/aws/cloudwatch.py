import boto3

from datetime import datetime, timedelta, timezone

from app.config import AWS_REGION


def get_ec2_cpu_utilization(
    instance_id,
    region=AWS_REGION,
    hours=24
):
    """
    Retrieve EC2 CPU utilization metrics
    from CloudWatch for the specified time period.
    """

    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region
    )

    end_time = datetime.now(timezone.utc)

    start_time = end_time - timedelta(
        hours=hours
    )

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=[
            "Average",
            "Maximum",
            "Minimum"
        ]
    )

    datapoints = response.get(
        "Datapoints",
        []
    )

    datapoints.sort(
        key=lambda x: x["Timestamp"]
    )

    return datapoints


def get_ec2_network_metrics(
    instance_id,
    region=AWS_REGION,
    hours=24
):
    """
    Retrieve EC2 network metrics
    from CloudWatch.
    """

    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region
    )

    end_time = datetime.now(timezone.utc)

    start_time = end_time - timedelta(
        hours=hours
    )

    metrics = {}

    for metric_name in [
        "NetworkIn",
        "NetworkOut"
    ]:

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric_name,
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Average"]
        )

        metrics[metric_name] = response.get(
            "Datapoints",
            []
        )

    return metrics
