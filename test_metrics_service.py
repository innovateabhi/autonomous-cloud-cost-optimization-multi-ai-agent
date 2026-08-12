from app.aws.ec2 import get_ec2_instances
from app.services.metrics_service import collect_metrics_for_all_resources


print("\n========================================")
print("       AUTOMATIC METRICS TEST")
print("========================================\n")


# --------------------------------------------------
# FETCH EC2 INSTANCES FROM AWS
# --------------------------------------------------

print("Fetching EC2 instances from AWS...\n")

instances = get_ec2_instances()


print(
    f"Found {len(instances)} EC2 instance(s).\n"
)


# --------------------------------------------------
# DISPLAY DISCOVERED INSTANCES
# --------------------------------------------------

for instance in instances:

    print(
        f"EC2: "
        f"{instance['instance_id']} | "
        f"{instance['instance_type']} | "
        f"{instance['state']} | "
        f"{instance['region']}"
    )


# --------------------------------------------------
# STOP IF NO INSTANCES FOUND
# --------------------------------------------------

if not instances:

    print(
        "\nNo EC2 instances found."
    )

    print(
        "Metrics collection stopped."
    )

    exit(0)


# --------------------------------------------------
# COLLECT METRICS
# --------------------------------------------------

print(
    "\nStarting CloudWatch metrics "
    "collection...\n"
)


try:

    collect_metrics_for_all_resources(
        resources=instances,
        hours=24
    )

except Exception as error:

    print(
        "\nMetrics collection failed:"
    )

    print(error)

    raise


# --------------------------------------------------
# COMPLETE
# --------------------------------------------------

print(
    "\n========================================"
)

print(
    "       TEST COMPLETED"
)

print(
    "========================================\n"
)
