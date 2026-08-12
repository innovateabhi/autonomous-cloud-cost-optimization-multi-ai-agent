from datetime import datetime, timezone

from app.aws.ec2 import get_ec2_instances


# ============================================================
# EC2 COST ESTIMATION
# ============================================================

# Approximate hourly prices for common EC2 instance types.
#
# These are ESTIMATES for project analysis only.
# They should NOT be treated as an AWS billing source.
#
# Add more instance types as required.

EC2_HOURLY_PRICES = {

    # T3
    "t3.nano": 0.0052,
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416,
    "t3.large": 0.0832,
    "t3.xlarge": 0.1664,
    "t3.2xlarge": 0.3328,

    # T2
    "t2.nano": 0.0058,
    "t2.micro": 0.0116,
    "t2.small": 0.023,
    "t2.medium": 0.0464,
    "t2.large": 0.0928,

    # M5
    "m5.large": 0.096,
    "m5.xlarge": 0.192,
    "m5.2xlarge": 0.384,
    "m5.4xlarge": 0.768,

    # C5
    "c5.large": 0.085,
    "c5.xlarge": 0.17,
    "c5.2xlarge": 0.34,

    # R5
    "r5.large": 0.126,
    "r5.xlarge": 0.252,
    "r5.2xlarge": 0.504,
}


# ============================================================
# GET HOURLY PRICE
# ============================================================

def get_ec2_hourly_price(instance_type):
    """
    Return the estimated hourly price for
    an EC2 instance type.

    Returns None when the instance type is
    not present in the local price table.
    """

    if not instance_type:
        return None

    return EC2_HOURLY_PRICES.get(
        instance_type
    )


# ============================================================
# ESTIMATE MONTHLY COST
# ============================================================

def estimate_monthly_cost(
    instance_type,
    hours_per_month=730
):
    """
    Estimate monthly EC2 compute cost.

    Default:
        730 hours/month

    This is an estimate only.
    """

    hourly_price = get_ec2_hourly_price(
        instance_type
    )

    if hourly_price is None:
        return None

    monthly_cost = (
        hourly_price
        * hours_per_month
    )

    return round(
        monthly_cost,
        2
    )


# ============================================================
# ESTIMATE INSTANCE COST
# ============================================================

def estimate_instance_cost(
    instance
):
    """
    Create a cost estimate for one
    automatically discovered EC2 instance.
    """

    instance_id = instance.get(
        "instance_id"
    )

    instance_type = instance.get(
        "instance_type"
    )

    region = instance.get(
        "region"
    )

    state = instance.get(
        "state"
    )

    hourly_price = get_ec2_hourly_price(
        instance_type
    )

    monthly_cost = estimate_monthly_cost(
        instance_type
    )

    return {

        "resource_id":
            instance_id,

        "resource_type":
            "EC2",

        "instance_type":
            instance_type,

        "region":
            region,

        "state":
            state,

        "hourly_cost":
            hourly_price,

        "monthly_cost":
            monthly_cost,

        "currency":
            "USD",

        "cost_source":
            "LOCAL_ESTIMATE",

        "estimated_at":
            datetime.now(
                timezone.utc
            ).isoformat()
    }


# ============================================================
# ESTIMATE COST FOR ALL EC2 INSTANCES
# ============================================================

def estimate_cost_for_all_ec2_instances(
    region=None
):
    """
    Automatically discover EC2 instances from AWS
    and estimate their monthly compute costs.

    No EC2 instance IDs are hard-coded.
    """

    print(
        "\n========================================"
    )

    print(
        "       EC2 COST ESTIMATION"
    )

    print(
        "========================================\n"
    )

    # --------------------------------------------------------
    # FETCH INSTANCES FROM AWS
    # --------------------------------------------------------

    if region:

        instances = get_ec2_instances(
            region=region
        )

    else:

        instances = get_ec2_instances()

    print(
        f"Found {len(instances)} "
        f"EC2 instance(s).\n"
    )

    results = []

    # --------------------------------------------------------
    # PROCESS EVERY INSTANCE
    # --------------------------------------------------------

    for instance in instances:

        instance_id = instance.get(
            "instance_id"
        )

        instance_type = instance.get(
            "instance_type"
        )

        state = instance.get(
            "state"
        )

        result = estimate_instance_cost(
            instance
        )

        results.append(
            result
        )

        print(
            f"EC2: {instance_id}"
        )

        print(
            f"  Type: "
            f"{instance_type}"
        )

        print(
            f"  State: "
            f"{state}"
        )

        print(
            f"  Region: "
            f"{result['region']}"
        )

        if result["monthly_cost"] is not None:

            print(
                f"  Estimated hourly: "
                f"${result['hourly_cost']}"
            )

            print(
                f"  Estimated monthly: "
                f"${result['monthly_cost']}"
            )

        else:

            print(
                "  Estimated monthly: "
                "UNKNOWN"
            )

            print(
                "  Reason: "
                "Instance type is not "
                "in the price table."
            )

        print()

    print(
        "========================================"
    )

    print(
        "     COST ESTIMATION COMPLETE"
    )

    print(
        "========================================"
    )

    return results
