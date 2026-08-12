import boto3

from app.config import AWS_REGION


# ============================================================
# BASIC COST EXPLORER
# ============================================================

def get_cost_and_usage(
    start_date,
    end_date,
    granularity="DAILY"
):
    """
    Retrieve general AWS cost information
    from Cost Explorer.
    """

    ce = boto3.client(
        "ce",
        region_name=AWS_REGION
    )

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date,
            "End": end_date
        },
        Granularity=granularity,
        Metrics=[
            "UnblendedCost"
        ]
    )

    return response


# ============================================================
# COST BY SERVICE
# ============================================================

def get_cost_by_service(
    start_date,
    end_date,
    granularity="DAILY"
):
    """
    Retrieve AWS service-level costs
    from Cost Explorer.
    """

    ce = boto3.client(
        "ce",
        region_name=AWS_REGION
    )

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date,
            "End": end_date
        },
        Granularity=granularity,
        Metrics=[
            "UnblendedCost"
        ],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    return response


# ============================================================
# EC2 RESOURCE-LEVEL COST
# ============================================================

def get_ec2_resource_costs(
    start_date,
    end_date,
    granularity="DAILY"
):
    """
    Retrieve actual AWS EC2 costs at
    individual EC2 instance level.

    Uses Cost Explorer's
    GetCostAndUsageWithResources API.

    IMPORTANT:
    EC2 resource-level data must be enabled
    in AWS Cost Explorer preferences.
    """

    ce = boto3.client(
        "ce",
        region_name=AWS_REGION
    )

    response = ce.get_cost_and_usage_with_resources(

        TimePeriod={
            "Start": start_date,
            "End": end_date
        },

        Granularity=granularity,

        Metrics=[
            "UnblendedCost"
        ],

        Filter={
            "Dimensions": {
                "Key": "SERVICE",
                "Values": [
                    "Amazon Elastic Compute Cloud - Compute"
                ]
            }
        },

        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "RESOURCE_ID"
            }
        ]
    )

    return response


# ============================================================
# PARSE EC2 RESOURCE COSTS
# ============================================================

def summarize_ec2_resource_costs(
    response
):
    """
    Convert the Cost Explorer response
    into:

        {
            "i-xxxxxxxx": 1.23,
            "i-yyyyyyyy": 2.45
        }

    Costs are accumulated across all
    returned days.
    """

    resource_costs = {}

    for result in response.get(
        "ResultsByTime",
        []
    ):

        for group in result.get(
            "Groups",
            []
        ):

            keys = group.get(
                "Keys",
                []
            )

            if not keys:
                continue

            resource_id = keys[0]

            amount = float(
                group
                .get("Metrics", {})
                .get("UnblendedCost", {})
                .get("Amount", 0)
            )

            resource_costs[resource_id] = (
                resource_costs.get(
                    resource_id,
                    0.0
                )
                + amount
            )

    return {
        resource_id: round(
            amount,
            6
        )
        for resource_id, amount
        in resource_costs.items()
    }


# ============================================================
# SERVICE COST SUMMARY
# ============================================================

def summarize_service_costs(
    response
):
    """
    Summarize service-level Cost Explorer
    response.
    """

    service_costs = {}

    total_cost = 0.0

    for result in response.get(
        "ResultsByTime",
        []
    ):

        for group in result.get(
            "Groups",
            []
        ):

            keys = group.get(
                "Keys",
                []
            )

            if not keys:
                continue

            service = keys[0]

            amount = float(
                group
                .get("Metrics", {})
                .get("UnblendedCost", {})
                .get("Amount", 0)
            )

            service_costs[service] = (
                service_costs.get(
                    service,
                    0.0
                )
                + amount
            )

            total_cost += amount

    return {
        "total_cost": round(
            total_cost,
            4
        ),
        "service_costs": service_costs
    }
