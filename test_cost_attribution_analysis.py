from app.services.cost_attribution_service import (
    analyze_cost_attribution
)


print("\n========================================")
print("       COST ATTRIBUTION ANALYSIS")
print("========================================\n")


result = analyze_cost_attribution(
    days=30
)


print(
    f"Resources found: "
    f"{result['resource_count']}"
)

print(
    f"Unattributed cost records: "
    f"{result['unattributed_record_count']}"
)

print(
    f"Total unattributed cost: "
    f"${result['total_unattributed_cost']:.6f}"
)


print("\nService totals:")

for service, amount in (
    result["service_totals"].items()
):

    print(
        f"  {service}: "
        f"${amount:.6f}"
    )


print("\nResources:")

for resource in result["resources"]:

    print(
        f"\nResource: "
        f"{resource['resource_id']}"
    )

    print(
        f"Instance Type: "
        f"{resource['instance_type']}"
    )

    print(
        f"State: "
        f"{resource['state']}"
    )

    print(
        f"Attributed Cost: "
        f"${resource['attributed_cost']:.6f}"
    )

    print(
        f"Cost Source: "
        f"{resource['cost_source']}"
    )

    print(
        f"Confidence: "
        f"{resource['confidence']}"
    )


print("\n========================================")
print("       TEST COMPLETED")
print("========================================\n")
