from app.services.analysis_service import (
    analyze_all_resources
)


print("\n========================================")
print("       ANALYSIS SERVICE TEST")
print("========================================\n")


results = analyze_all_resources(
    hours=24
)


print("\n========================================")
print("       FINAL ANALYSIS RESULTS")
print("========================================\n")


if not results:

    print(
        "No resources were analyzed."
    )

else:

    for result in results:

        print(
            "\n----------------------------------------"
        )

        resource = result.get(
            "resource",
            {}
        )

        utilization = result.get(
            "utilization",
            {}
        )

        cost = result.get(
            "cost",
            {}
        )

        optimization = result.get(
            "optimization",
            {}
        )

        print(
            f"Resource: "
            f"{resource.get('resource_id')}"
        )

        print(
            f"Instance Type: "
            f"{resource.get('instance_type')}"
        )

        print(
            f"Region: "
            f"{resource.get('region')}"
        )

        print(
            f"CPU Status: "
            f"{utilization.get('status')}"
        )

        print(
            f"Average CPU: "
            f"{utilization.get('average_cpu')}"
        )

        print(
            f"Monthly Cost: "
            f"${cost.get('monthly_cost')}"
        )

        print(
            f"Recommendation: "
            f"{optimization.get('recommendation')}"
        )

        print(
            f"Priority: "
            f"{optimization.get('priority')}"
        )

        print(
            f"Estimated Savings: "
            f"${optimization.get('estimated_savings', 0)}"
        )


print("\n========================================")
print("       TEST COMPLETED")
print("========================================\n")
