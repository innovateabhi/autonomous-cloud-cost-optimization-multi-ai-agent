from app.services.analysis_service import (
    analyze_all_resources
)

from app.services.risk_service import (
    evaluate_all_risks
)


print("\n========================================")
print("       RISK SERVICE TEST")
print("========================================")


print("\nRunning resource analysis...\n")

analysis_results = analyze_all_resources(
    hours=24
)


print("\nRunning risk evaluation...\n")

risk_results = evaluate_all_risks(
    analysis_results
)


print("\n========================================")
print("       RISK RESULTS")
print("========================================")


for result in risk_results:

    resource = result.get(
        "resource",
        {}
    )

    optimization = result.get(
        "optimization",
        {}
    )

    risk = result.get(
        "risk",
        {}
    )

    print("\n----------------------------------------")

    print(
        f"Resource: "
        f"{resource.get('resource_id')}"
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
        f"Risk Level: "
        f"{risk.get('risk_level')}"
    )

    print(
        f"Approval: "
        f"{risk.get('approval')}"
    )

    print(
        f"Risk Factors: "
        f"{risk.get('risk_factors')}"
    )


print("\n========================================")
print("       TEST COMPLETED")
print("========================================\n")
