from app.services.ec2_cost_service import (
    estimate_cost_for_all_ec2_instances
)


print(
    "\n========================================"
)

print(
    "       EC2 COST SERVICE TEST"
)

print(
    "========================================\n"
)


results = (
    estimate_cost_for_all_ec2_instances()
)


print(
    "\n========================================"
)

print(
    "           RESULTS"
)

print(
    "========================================\n"
)


for result in results:

    print(
        f"Resource: "
        f"{result['resource_id']}"
    )

    print(
        f"Instance Type: "
        f"{result['instance_type']}"
    )

    print(
        f"Region: "
        f"{result['region']}"
    )

    print(
        f"State: "
        f"{result['state']}"
    )

    print(
        f"Hourly Cost: "
        f"${result['hourly_cost']}"
    )

    print(
        f"Monthly Cost: "
        f"${result['monthly_cost']}"
    )

    print(
        f"Source: "
        f"{result['cost_source']}"
    )

    print()
