from app.services.decision_service import (
    generate_decisions
)


print("\n========================================")
print("       DECISION SERVICE TEST")
print("========================================\n")


decisions = generate_decisions(
    hours=24
)


print("\n========================================")
print("       FINAL RESULTS")
print("========================================")


for decision in decisions:

    print("\n----------------------------------------")

    print(
        f"Resource: "
        f"{decision.get('resource_id')}"
    )

    print(
        f"Instance Type: "
        f"{decision.get('instance_type')}"
    )

    print(
        f"Region: "
        f"{decision.get('region')}"
    )

    print(
        f"CPU Status: "
        f"{decision.get('cpu_status')}"
    )

    print(
        f"Average CPU: "
        f"{decision.get('average_cpu')}"
    )

    print(
        f"Monthly Cost: "
        f"${decision.get('monthly_cost')}"
    )

    print(
        f"Recommendation: "
        f"{decision.get('recommendation')}"
    )

    print(
        f"Priority: "
        f"{decision.get('priority')}"
    )

    print(
        f"Estimated Savings: "
        f"${decision.get('estimated_savings')}"
    )

    print(
        f"Risk Level: "
        f"{decision.get('risk_level')}"
    )

    print(
        f"Final Decision: "
        f"{decision.get('final_decision')}"
    )

    print(
        f"Execution Allowed: "
        f"{decision.get('execution_allowed')}"
    )

    print(
        f"Reason: "
        f"{decision.get('risk_reason')}"
    )


print("\n========================================")
print("       TEST COMPLETED")
print("========================================\n")
